"""
IBPS Clerk Prelims — State Management & SRS Engine
Handles: JSON persistence, block counter, SRS scheduling, task selection.
"""

import json
import os
import copy
from datetime import datetime

from study_data import (
    TOPICS, MODULES, REVIEW_GAPS, STUDY_QUEUE,
    get_topic_modules, get_topic_status, TOTAL_MODULES,
)

# State file lives next to this script
_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(_DIR, "tracker_state.json")

DEFAULT_STATE = {
    "current_block": 0,
    "learn_index": 0,          # index into STUDY_QUEUE
    "completed": {},           # module_id → completion info
    "history": [],             # chronological log
    "created_at": None,
}


# ── Persistence ───────────────────────────────────────────────────────────

def load_state():
    """Load state from JSON file, or create fresh state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    state = copy.deepcopy(DEFAULT_STATE)
    state["created_at"] = datetime.now().isoformat()
    save_state(state)
    return state


def save_state(state):
    """Write state to JSON file."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def reset_state():
    """Wipe all progress and return fresh state."""
    state = copy.deepcopy(DEFAULT_STATE)
    state["created_at"] = datetime.now().isoformat()
    save_state(state)
    return state


# ── SRS Engine ────────────────────────────────────────────────────────────

def get_due_reviews(state):
    """Return list of module_ids with reviews due at or before current block.
    Sorted: highest priority first, then earliest due.
    """
    block = state["current_block"]
    due = []
    priority_order = {"VH": 0, "H": 1, "M": 2, "L": 3}

    for mid, info in state["completed"].items():
        if info.get("all_reviews_done", False):
            continue
        nrb = info.get("next_review_block")
        if nrb is not None and nrb <= block:
            topic_id = MODULES[mid]["topic"]
            pri = TOPICS[topic_id]["priority"]
            due.append((priority_order[pri], nrb, mid))

    due.sort()
    return [d[2] for d in due]


def _find_next_learn_index(state):
    """Scan forward from learn_index to find next uncompleted module in queue."""
    idx = state["learn_index"]
    while idx < len(STUDY_QUEUE):
        if STUDY_QUEUE[idx] not in state["completed"]:
            return idx
        idx += 1
    return None  # all learned


def get_next_task(state):
    """Determine the next task for the user.
    Returns dict: {"type": "learn"|"review", "module_id": str, ...} or None.
    """
    # 1. Check for due reviews first
    due = get_due_reviews(state)
    if due:
        mid = due[0]
        info = state["completed"][mid]
        return {
            "type": "review",
            "module_id": mid,
            "review_number": info["reviews_done"] + 1,
            "total_reviews": len(REVIEW_GAPS[TOPICS[MODULES[mid]["topic"]]["priority"]]),
            "due_reviews_count": len(due),
        }

    # 2. Next learn task
    idx = _find_next_learn_index(state)
    if idx is not None:
        return {
            "type": "learn",
            "module_id": STUDY_QUEUE[idx],
            "queue_index": idx,
        }

    # 3. Check for future reviews (all learns done, reviews pending)
    has_pending = any(
        not info.get("all_reviews_done", False)
        for info in state["completed"].values()
    )
    if has_pending:
        # Find the nearest future review
        nearest = None
        for mid, info in state["completed"].items():
            if info.get("all_reviews_done", False):
                continue
            nrb = info.get("next_review_block")
            if nrb is not None:
                if nearest is None or nrb < nearest:
                    nearest = nrb
        return {
            "type": "waiting",
            "next_review_at_block": nearest,
            "blocks_until": nearest - state["current_block"] if nearest else 0,
        }

    return None  # truly done — all 186 modules learned and fully reviewed


def complete_task(state, module_id, task_type):
    """Mark a task (learn or review) as done. Returns updated state."""
    state["current_block"] += 1
    topic_id = MODULES[module_id]["topic"]
    priority = TOPICS[topic_id]["priority"]
    gaps = REVIEW_GAPS[priority]

    if task_type == "learn":
        # Record completion + schedule first review
        state["completed"][module_id] = {
            "completed_at_block": state["current_block"],
            "reviews_done": 0,
            "next_review_block": state["current_block"] + gaps[0],
            "all_reviews_done": False,
        }
        # Advance learn pointer past this module
        idx = state.get("learn_index", 0)
        while idx < len(STUDY_QUEUE) and STUDY_QUEUE[idx] in state["completed"]:
            idx += 1
        state["learn_index"] = idx

    elif task_type == "review":
        info = state["completed"][module_id]
        info["reviews_done"] += 1
        if info["reviews_done"] >= len(gaps):
            info["all_reviews_done"] = True
            info["next_review_block"] = None
        else:
            # Next review is relative to ORIGINAL completion block
            info["next_review_block"] = (
                info["completed_at_block"] + gaps[info["reviews_done"]]
            )

    # Log entry
    state["history"].append({
        "block": state["current_block"],
        "module": module_id,
        "type": task_type,
        "time": datetime.now().isoformat(),
    })

    save_state(state)
    return state


def restart_module_srs(state, module_id):
    """Fail Rule: restart SRS for a forgotten module from current block."""
    if module_id not in state["completed"]:
        return state

    priority = TOPICS[MODULES[module_id]["topic"]]["priority"]
    gaps = REVIEW_GAPS[priority]

    state["completed"][module_id] = {
        "completed_at_block": state["current_block"],
        "reviews_done": 0,
        "next_review_block": state["current_block"] + gaps[0],
        "all_reviews_done": False,
    }

    state["history"].append({
        "block": state["current_block"],
        "module": module_id,
        "type": "restart",
        "time": datetime.now().isoformat(),
    })

    save_state(state)
    return state


# ── Statistics ────────────────────────────────────────────────────────────

def get_section_stats(state):
    """Compute per-section progress: {section_code: {done, total, pct}}"""
    from study_data import SECTIONS
    completed_set = set(state["completed"].keys())
    stats = {}
    for sec_code in SECTIONS:
        # All modules belonging to topics in this section
        sec_modules = [
            mid for mid, m in MODULES.items()
            if TOPICS[m["topic"]]["section"] == sec_code
        ]
        done = sum(1 for m in sec_modules if m in completed_set)
        total = len(sec_modules)
        pct = (done / total * 100) if total > 0 else 0
        stats[sec_code] = {"done": done, "total": total, "pct": round(pct, 1)}
    return stats


def get_priority_stats(state):
    """Compute per-priority progress: {priority: {done, total, pct}}"""
    completed_set = set(state["completed"].keys())
    stats = {}
    for pri in ["VH", "H", "M", "L"]:
        pri_modules = [
            mid for mid, m in MODULES.items()
            if TOPICS[m["topic"]]["priority"] == pri
        ]
        done = sum(1 for m in pri_modules if m in completed_set)
        total = len(pri_modules)
        pct = (done / total * 100) if total > 0 else 0
        stats[pri] = {"done": done, "total": total, "pct": round(pct, 1)}
    return stats


def get_all_topic_statuses(state):
    """Return list of (topic_id, name, section, priority, status, done/total)."""
    completed_set = set(state["completed"].keys())
    result = []
    for tid, t in TOPICS.items():
        mods = get_topic_modules(tid)
        done = sum(1 for m in mods if m in completed_set)
        status = get_topic_status(tid, completed_set)
        result.append({
            "id": tid,
            "name": t["name"],
            "section": t["section"],
            "priority": t["priority"],
            "status": status,
            "done": done,
            "total": len(mods),
        })
    return result


def get_upcoming_reviews(state, limit=20):
    """Return upcoming reviews sorted by due block."""
    upcoming = []
    for mid, info in state["completed"].items():
        if info.get("all_reviews_done", False):
            continue
        nrb = info.get("next_review_block")
        if nrb is not None:
            topic_id = MODULES[mid]["topic"]
            upcoming.append({
                "module": mid,
                "topic": TOPICS[topic_id]["name"],
                "priority": TOPICS[topic_id]["priority"],
                "due_block": nrb,
                "blocks_away": nrb - state["current_block"],
                "review_num": info["reviews_done"] + 1,
                "pages": f"pp {MODULES[mid]['start']}–{MODULES[mid]['end']}",
            })
    upcoming.sort(key=lambda x: x["due_block"])
    return upcoming[:limit]
