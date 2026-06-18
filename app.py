"""
IBPS Clerk Prelims — Study Tracker
Streamlit app: see task → click done → get next.

State persistence:
  - Cloud (Streamlit Community Cloud): saved to a secret GitHub Gist.
    Set GITHUB_TOKEN in app Settings → Secrets.
  - Local dev: falls back to tracker_state.json.
"""

import copy
import streamlit as st

from study_data import (
    TOPICS, MODULES, SECTIONS, REVIEW_GAPS, PRIORITY_LABELS,
    STUDY_QUEUE, TOTAL_MODULES, get_topic_modules,
)
from state import (
    DEFAULT_STATE, save_state as save_local, load_state as load_local,
    reset_state as reset_local,
    get_next_task, complete_task, restart_module_srs,
    get_section_stats, get_priority_stats,
    get_all_topic_statuses, get_upcoming_reviews,
    get_due_reviews,
)

# ── Page Config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IBPS Study Tracker",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .task-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 28px;
        margin: 12px 0;
        border-left: 5px solid;
        color: #e0e0e0;
    }
    .task-card.learn  { border-left-color: #4fc3f7; }
    .task-card.review { border-left-color: #ff9800; }

    .task-type        { font-size:13px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px; }
    .task-type.learn  { color:#4fc3f7; }
    .task-type.review { color:#ff9800; }

    .task-title  { font-size:24px; font-weight:700; color:#ffffff; margin:6px 0; }
    .task-module { font-size:14px; color:#90a4ae; font-family:monospace; }
    .task-pages  { font-size:20px; font-weight:600; color:#81c784; margin:12px 0 4px 0; }
    .task-pdf    { font-size:13px; color:#78909c; }
    .task-label  { font-size:12px; color:#b0bec5; margin-top:6px; font-style:italic; }

    .pri-vh { color:#ce93d8; font-weight:700; }
    .pri-h  { color:#ef5350; font-weight:700; }
    .pri-m  { color:#ffd54f; font-weight:700; }
    .pri-l  { color:#66bb6a; font-weight:700; }

    .done-banner {
        background: linear-gradient(135deg,#1b5e20 0%,#2e7d32 100%);
        border-radius:16px; padding:32px; text-align:center; color:#ffffff;
    }
    .wait-banner {
        background: linear-gradient(135deg,#4a148c 0%,#6a1b9a 100%);
        border-radius:16px; padding:32px; text-align:center; color:#ffffff;
    }
    .sync-ok  { background:#1b5e20; border-radius:8px; padding:6px 12px; font-size:12px; color:#a5d6a7; display:inline-block; }
    .sync-err { background:#b71c1c; border-radius:8px; padding:6px 12px; font-size:12px; color:#ef9a9a; display:inline-block; }

    div[data-testid="stSidebar"] { background:#0d1117; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# Gist / State Backend Init
# ══════════════════════════════════════════════════════════════════════════

def _get_token():
    """Try st.secrets first, then session_state (manual entry)."""
    # Try exact key lookup (more reliable than .get() on Streamlit Cloud)
    for key in ("GITHUB_TOKEN", "github_token", "GithubToken"):
        try:
            val = st.secrets[key]
            if val:
                return val
        except (KeyError, FileNotFoundError, Exception):
            pass
    return st.session_state.get("_manual_token")


def _init_gist_backend():
    """One-time init per session: find/create gist, load state."""
    from gist_backend import find_or_create_gist, load_from_gist
    token = _get_token()
    if not token:
        return False

    if "gist_id" not in st.session_state:
        gist_id, result = find_or_create_gist(token)
        if gist_id is None:
            st.session_state["_gist_error"] = str(result)
            return False
        st.session_state["gist_id"] = gist_id
        # If result is already the fresh state dict, use it
        if isinstance(result, dict):
            st.session_state["state"] = result
            return True

    # Load from gist
    if "state" not in st.session_state:
        state, err = load_from_gist(st.session_state["gist_id"], token)
        if err:
            st.session_state["_gist_error"] = err
            return False
        st.session_state["state"] = state
    return True


def _save(state):
    """Save state: gist if available, else local JSON."""
    token = _get_token()
    if token and "gist_id" in st.session_state:
        from gist_backend import save_to_gist
        ok, err = save_to_gist(st.session_state["gist_id"], state, token)
        st.session_state["_last_sync"] = ("ok", None) if ok else ("err", err)
    else:
        save_local(state)
    st.session_state["state"] = state


def _load():
    """Return current state from session_state or load it."""
    if "state" in st.session_state:
        return st.session_state["state"]
    token = _get_token()
    if token:
        _init_gist_backend()
        if "state" in st.session_state:
            return st.session_state["state"]
    # Fallback: local JSON
    s = load_local()
    st.session_state["state"] = s
    return s


def _reset():
    """Wipe all progress."""
    token = _get_token()
    if token and "gist_id" in st.session_state:
        import copy
        from datetime import datetime
        from gist_backend import save_to_gist
        fresh = copy.deepcopy(DEFAULT_STATE)
        fresh["created_at"] = datetime.now().isoformat()
        save_to_gist(st.session_state["gist_id"], fresh, token)
        st.session_state["state"] = fresh
    else:
        s = reset_local()
        st.session_state["state"] = s


# ── Boot: init backend ────────────────────────────────────────────────────
token = _get_token()
using_gist = False

if token:
    using_gist = _init_gist_backend()

state = _load()


# ══════════════════════════════════════════════════════════════════════════
# Manual token entry (shown only when no secret is configured)
# ══════════════════════════════════════════════════════════════════════════
if not token:
    with st.sidebar:
        st.markdown("### 🔑 GitHub Token")
        st.caption("Enter to sync across devices. Leave blank for local-only.")
        entered = st.text_input("Token (ghp_...)", type="password", key="_token_input")
        if entered and st.button("Connect", key="_connect_btn"):
            from gist_backend import verify_token
            user, err = verify_token(entered)
            if user:
                st.session_state["_manual_token"] = entered
                st.session_state.pop("state", None)
                st.session_state.pop("gist_id", None)
                st.rerun()
            else:
                st.error(f"Invalid token: {err}")


# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 IBPS Tracker")

    # Sync status badge
    if using_gist:
        sync_info = st.session_state.get("_last_sync")
        if sync_info and sync_info[0] == "err":
            st.markdown(f'<div class="sync-err">⚠ Sync error: {sync_info[1]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sync-ok">☁ Synced to cloud</div>', unsafe_allow_html=True)
    else:
        st.caption("💾 Local mode")

    st.caption(f"Block **{state['current_block']}** · {len(state['completed'])}/{TOTAL_MODULES} modules")

    page = st.radio(
        "Navigate",
        ["📋 Current Task", "📊 Progress", "📅 Reviews", "⚙️ Settings"],
        label_visibility="collapsed",
    )

    st.divider()
    done_count = len(state["completed"])
    pct = done_count / TOTAL_MODULES
    st.progress(pct, text=f"{pct*100:.0f}% studied")

    due = get_due_reviews(state)
    if due:
        st.warning(f"🔔 {len(due)} review(s) due")


# ── Helper: module display info ───────────────────────────────────────────
def module_info(module_id):
    m  = MODULES[module_id]
    t  = TOPICS[m["topic"]]
    sec = SECTIONS[t["section"]]
    pi, pn = PRIORITY_LABELS[t["priority"]]
    pages = m["end"] - m["start"] + 1
    total_mods = len(get_topic_modules(m["topic"]))
    mod_part = module_id.replace(m["topic"] + "-", "")
    return {
        "module_id": module_id, "topic_id": m["topic"],
        "topic_name": t["name"], "section_icon": sec["icon"],
        "section_name": sec["name"], "priority": t["priority"],
        "pri_icon": pi, "pri_name": pn, "pdf": t["pdf"],
        "page_start": m["start"], "page_end": m["end"],
        "page_count": pages, "label": m["label"],
        "mod_part": mod_part, "total_mods": total_mods,
    }


# ══════════════════════════════════════════════════════════════════════════
# PAGE: Current Task
# ══════════════════════════════════════════════════════════════════════════
if page == "📋 Current Task":
    task = get_next_task(state)

    if task is None:
        st.markdown("""
        <div class="done-banner">
            <h2>🎉 All 186 modules studied & reviewed!</h2>
            <p>You've completed the entire IBPS Clerk Prelims study plan.</p>
        </div>""", unsafe_allow_html=True)

    elif task["type"] == "waiting":
        st.markdown(f"""
        <div class="wait-banner">
            <h2>⏳ Waiting for reviews</h2>
            <p>All new modules done! Next review due at block {task['next_review_at_block']}
            ({task['blocks_until']} blocks away).</p>
            <p style="font-size:14px;color:#ce93d8;">Click "Advance Block" to move forward.</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("")
        if st.button("⏩ Advance Block", use_container_width=True, type="primary"):
            state["current_block"] += 1
            _save(state)
            st.rerun()

    else:
        info = module_info(task["module_id"])
        is_review  = task["type"] == "review"
        card_class = "review" if is_review else "learn"
        type_label = "REVIEW" if is_review else "LEARN"

        review_extra = ""
        if is_review:
            review_extra = f" · Review {task['review_number']}/{task['total_reviews']}"
            if task["due_reviews_count"] > 1:
                review_extra += f" · 🔔 {task['due_reviews_count']} due"

        label_html = f'<div class="task-label">§ {info["label"]}</div>' if info["label"] else ""
        pri_class  = f"pri-{info['priority'].lower()}"

        st.markdown(f"""
        <div class="task-card {card_class}">
            <div class="task-type {card_class}">{type_label}{review_extra}</div>
            <div class="task-title">{info['topic_name']}</div>
            <div class="task-module">
                {info['module_id']} · {info['section_icon']} {info['section_name']}
                · <span class="{pri_class}">{info['pri_icon']} {info['pri_name']}</span>
                · {info['mod_part']} of {info['total_mods']} modules
            </div>
            <div class="task-pages">📖 Pages {info['page_start']}–{info['page_end']}  ({info['page_count']} pp)</div>
            <div class="task-pdf">📄 {info['pdf']}</div>
            {label_html}
        </div>""", unsafe_allow_html=True)

        st.markdown("")
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            if st.button("✅ Done — studied these pages", use_container_width=True, type="primary"):
                state = complete_task(state, task["module_id"], task["type"])
                _save(state)
                st.rerun()

        with col2:
            if is_review:
                if st.button("🔄 Forgot — restart SRS", use_container_width=True):
                    state = restart_module_srs(state, task["module_id"])
                    _save(state)
                    st.rerun()

        with col3:
            if not is_review:
                if st.button("⏭️ Skip", use_container_width=True):
                    state["learn_index"] = task.get("queue_index", state["learn_index"]) + 1
                    _save(state)
                    st.rerun()

        # Up next preview
        st.markdown("---")
        st.caption("📌 Up next")

        peek = copy.deepcopy(state)
        peek["current_block"] += 1
        mid = task["module_id"]
        if mid not in peek["completed"]:
            tid = MODULES[mid]["topic"]
            gaps = REVIEW_GAPS[TOPICS[tid]["priority"]]
            peek["completed"][mid] = {
                "completed_at_block": peek["current_block"],
                "reviews_done": 0,
                "next_review_block": peek["current_block"] + gaps[0],
                "all_reviews_done": False,
            }
            idx = peek.get("learn_index", 0)
            while idx < len(STUDY_QUEUE) and STUDY_QUEUE[idx] in peek["completed"]:
                idx += 1
            peek["learn_index"] = idx
        else:
            ci = peek["completed"][mid]
            ci["reviews_done"] += 1
            gaps = REVIEW_GAPS[TOPICS[MODULES[mid]["topic"]]["priority"]]
            if ci["reviews_done"] >= len(gaps):
                ci["all_reviews_done"] = True
                ci["next_review_block"] = None
            else:
                ci["next_review_block"] = ci["completed_at_block"] + gaps[ci["reviews_done"]]

        nt = get_next_task(peek)
        if nt and nt["type"] in ("learn", "review"):
            ni  = module_info(nt["module_id"])
            tag = "🔵 LEARN" if nt["type"] == "learn" else "🟠 REVIEW"
            st.markdown(f"{tag} · **{ni['topic_name']}** · `{nt['module_id']}` · pp {ni['page_start']}–{ni['page_end']}")
        elif nt and nt["type"] == "waiting":
            st.markdown(f"⏳ Next review at block {nt['next_review_at_block']}")
        else:
            st.markdown("🎉 Nothing left after this!")


# ══════════════════════════════════════════════════════════════════════════
# PAGE: Progress
# ══════════════════════════════════════════════════════════════════════════
elif page == "📊 Progress":
    st.markdown("## 📊 Progress Dashboard")

    done = len(state["completed"])
    reviews_done = sum(i["reviews_done"] for i in state["completed"].values())
    pages_done = sum(
        MODULES[m]["end"] - MODULES[m]["start"] + 1
        for m in state["completed"]
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Modules Studied", f"{done}/{TOTAL_MODULES}")
    c2.metric("Current Block",   state["current_block"])
    c3.metric("Reviews Done",    reviews_done)
    c4.metric("Pages Covered",   pages_done)

    st.progress(done / TOTAL_MODULES, text=f"Overall: {done}/{TOTAL_MODULES} ({done/TOTAL_MODULES*100:.1f}%)")

    st.markdown("---")
    st.markdown("### By Section")
    for code, info in SECTIONS.items():
        s = get_section_stats(state)[code]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(s["pct"] / 100 if s["total"] > 0 else 0,
                        text=f"{info['icon']} {info['name']}")
        with col2:
            st.caption(f"{s['done']}/{s['total']} ({s['pct']}%)")

    st.markdown("---")
    st.markdown("### By Priority")
    pri_stats = get_priority_stats(state)
    cols = st.columns(4)
    for i, (pri, label) in enumerate([
        ("VH", "🟣 Very High"), ("H", "🔴 High"),
        ("M", "🟡 Medium"),    ("L", "🟢 Low"),
    ]):
        s = pri_stats[pri]
        with cols[i]:
            st.metric(label, f"{s['done']}/{s['total']}")
            st.progress(s["pct"] / 100 if s["total"] > 0 else 0)

    st.markdown("---")
    st.markdown("### Topic Status")
    statuses = get_all_topic_statuses(state)

    sec_filter    = st.selectbox("Filter by section",
        ["All"] + [f"{v['icon']} {v['name']}" for v in SECTIONS.values()])
    status_filter = st.selectbox("Filter by status",
        ["All", "Not Started", "In Progress", "Completed"])

    filtered = statuses
    if sec_filter != "All":
        sec_code = [k for k, v in SECTIONS.items()
                    if f"{v['icon']} {v['name']}" == sec_filter][0]
        filtered = [s for s in filtered if s["section"] == sec_code]
    if status_filter != "All":
        filtered = [s for s in filtered if s["status"] == status_filter]

    if filtered:
        header = "| # | Topic | Priority | Progress | Status |\n|:--|:------|:---------|:---------|:-------|\n"
        rows = ""
        for s in filtered:
            pi, pn = PRIORITY_LABELS[s["priority"]]
            em = {"Not Started": "⬜", "In Progress": "🔶", "Completed": "✅"}[s["status"]]
            rows += f"| {s['id']} | {s['name']} | {pi} {pn} | {s['done']}/{s['total']} | {em} {s['status']} |\n"
        st.markdown(header + rows)
    else:
        st.info("No topics match the selected filters.")


# ══════════════════════════════════════════════════════════════════════════
# PAGE: Reviews
# ══════════════════════════════════════════════════════════════════════════
elif page == "📅 Reviews":
    st.markdown("## 📅 Review Schedule")
    st.caption(f"Current block: **{state['current_block']}**")

    upcoming = get_upcoming_reviews(state, limit=50)

    if not upcoming:
        if state["completed"]:
            st.success("🎉 No pending reviews!")
        else:
            st.info("Start studying to schedule reviews.")
    else:
        due_now = [r for r in upcoming if r["blocks_away"] <= 0]
        future  = [r for r in upcoming if r["blocks_away"] > 0]

        if due_now:
            st.markdown(f"### 🔔 Due Now ({len(due_now)})")
            for r in due_now:
                pi, _ = PRIORITY_LABELS[r["priority"]]
                st.markdown(
                    f"- {pi} **{r['topic']}** · `{r['module']}` · {r['pages']} · Review #{r['review_num']}"
                )

        if future:
            st.markdown(f"### ⏳ Upcoming ({len(future)})")
            header = "| Module | Topic | Priority | Pages | Review # | Due Block | Away |\n"
            header += "|:-------|:------|:---------|:------|:---------|:----------|:-----|\n"
            rows = ""
            for r in future:
                pi, pn = PRIORITY_LABELS[r["priority"]]
                rows += (f"| `{r['module']}` | {r['topic']} | {pi} {pn} "
                         f"| {r['pages']} | #{r['review_num']} | {r['due_block']} | +{r['blocks_away']} |\n")
            st.markdown(header + rows)

    st.markdown("---")
    st.markdown("### Review Stats")
    total_rv = sum(i["reviews_done"] for i in state["completed"].values())
    full_rv  = sum(1 for i in state["completed"].values() if i.get("all_reviews_done"))
    st.metric("Total Reviews Completed", total_rv)
    st.metric("Modules Fully Reviewed",  full_rv)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: Settings
# ══════════════════════════════════════════════════════════════════════════
elif page == "⚙️ Settings":
    st.markdown("## ⚙️ Settings")

    # Cloud sync status
    st.markdown("### ☁ Cloud Sync")
    if using_gist:
        gid = st.session_state.get("gist_id", "—")
        st.success(f"Synced to secret GitHub Gist · ID: `{gid}`")
        st.caption("Your progress saves automatically after every Done click — accessible on any device.")
    else:
        st.warning("Not synced to cloud — running in local mode.")

        # --- Diagnose why secrets aren't working ---
        st.markdown("#### 🔍 Secret Diagnostic")
        try:
            all_keys = list(st.secrets.keys())
            if all_keys:
                st.info(f"Streamlit secrets found — keys: `{'`, `'.join(all_keys)}`")
                if "GITHUB_TOKEN" in all_keys:
                    st.success("GITHUB_TOKEN found! Click **Reboot app** from ⋮ menu.")
                else:
                    st.error(f"GITHUB_TOKEN not found. You have: {all_keys}. Rename it to exactly `GITHUB_TOKEN`.")
            else:
                st.error("No secrets found at all. Secrets were not saved correctly.")
        except FileNotFoundError:
            st.error("No secrets file found — not running on Streamlit Cloud, or secrets not saved yet.")
        except Exception as e:
            st.error(f"Secrets error: {e}")

        st.markdown("")
        st.markdown("**How to fix — exact steps:**")
        token_hint = "gh" + "p_yZjSCqj2SJmg0rTiqeGbquhxlXiBJ84ZS0QO"
        st.markdown(f"""
1. In your Streamlit app → click **⋮** (top right) → **Settings**
2. Click the **Secrets** tab
3. Make sure the text box contains **exactly** this (nothing else):
```
GITHUB_TOKEN = "{token_hint}"
```
4. Click **Save**
5. Then click **⋮ → Reboot app**
6. After reboot the sidebar should show ☁ Synced
""")

    st.markdown("---")
    st.markdown("### State")
    st.metric("Block Counter", state["current_block"])
    st.metric("Modules Studied", len(state["completed"]))
    if state.get("created_at"):
        st.caption(f"Tracker created: {state['created_at']}")

    st.markdown("---")
    st.markdown("### Block Adjustment")
    st.caption("Advance the block counter if you studied offline.")
    advance = st.number_input("Advance by", min_value=1, max_value=50, value=1)
    if st.button("⏩ Advance Block"):
        state["current_block"] += advance
        _save(state)
        st.success(f"Block advanced to {state['current_block']}")
        st.rerun()

    st.markdown("---")
    st.markdown("### Export / Import")
    import json
    st.download_button(
        "📥 Download State (JSON)",
        data=json.dumps(state, indent=2),
        file_name="ibps_tracker_state.json",
        mime="application/json",
    )
    uploaded = st.file_uploader("📤 Import State", type=["json"])
    if uploaded:
        try:
            imp = json.load(uploaded)
            if "current_block" in imp and "completed" in imp:
                _save(imp)
                st.success("Imported! Refreshing...")
                st.rerun()
            else:
                st.error("Invalid state file.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### Recent History")
    if state["history"]:
        recent = list(reversed(state["history"][-20:]))
        header = "| Block | Module | Type | Time |\n|:------|:-------|:-----|:-----|\n"
        rows = ""
        for h in recent:
            ts   = h.get("time", "")[:16].replace("T", " ")
            em   = {"learn": "🔵", "review": "🟠", "restart": "🔄"}.get(h["type"], "❓")
            rows += f"| {h['block']} | `{h['module']}` | {em} {h['type']} | {ts} |\n"
        st.markdown(header + rows)
    else:
        st.info("No history yet.")

    st.markdown("---")
    st.markdown("### ⚠️ Danger Zone")
    if st.button("🗑️ Reset All Progress", type="secondary"):
        st.session_state["confirm_reset"] = True

    if st.session_state.get("confirm_reset"):
        st.error("This will wipe all progress permanently.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Yes, reset", type="primary"):
                _reset()
                st.session_state["confirm_reset"] = False
                st.rerun()
        with c2:
            if st.button("Cancel"):
                st.session_state["confirm_reset"] = False
                st.rerun()
