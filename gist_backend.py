"""
Gist Backend — stores tracker state as a secret GitHub Gist.
Cross-device: any browser, any device, same state.
"""
import urllib.request
import urllib.error
import json

GIST_FILENAME = "ibps_tracker_state.json"
GIST_DESCRIPTION = "IBPS-STUDY-TRACKER-STATE"  # used to find the gist


def _api(method, path, data=None, token=None):
    """Low-level GitHub API call. Returns (parsed_json, http_status)."""
    url = "https://api.github.com" + path
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "ibps-study-tracker/1.0",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8")), r.status
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8")
            return json.loads(body), e.code
        except Exception:
            return {"message": str(e)}, e.code
    except Exception as e:
        return {"message": str(e)}, 0


def find_or_create_gist(token):
    """Return gist_id of the state gist. Creates it if not found.
    Searches all user gists for GIST_DESCRIPTION + GIST_FILENAME.
    """
    # Paginate through gists (up to 5 pages of 100)
    for page in range(1, 6):
        gists, code = _api("GET", f"/gists?per_page=100&page={page}", token=token)
        if code != 200 or not gists:
            break
        for g in gists:
            if (
                g.get("description") == GIST_DESCRIPTION
                and GIST_FILENAME in g.get("files", {})
            ):
                return g["id"], None  # found

    # Not found — create fresh gist
    from state import DEFAULT_STATE
    import copy
    from datetime import datetime
    fresh = copy.deepcopy(DEFAULT_STATE)
    fresh["created_at"] = datetime.now().isoformat()

    payload = {
        "description": GIST_DESCRIPTION,
        "public": False,
        "files": {
            GIST_FILENAME: {
                "content": json.dumps(fresh, indent=2, ensure_ascii=False)
            }
        },
    }
    gist, code = _api("POST", "/gists", data=payload, token=token)
    if code == 201:
        return gist["id"], fresh
    return None, f"Failed to create gist: {gist.get('message', code)}"


def load_from_gist(gist_id, token):
    """Load state JSON from gist. Returns (state_dict, error_str_or_None)."""
    gist, code = _api("GET", f"/gists/{gist_id}", token=token)
    if code != 200:
        return None, f"Gist load failed ({code}): {gist.get('message')}"
    try:
        raw = gist["files"][GIST_FILENAME]["content"]
        return json.loads(raw), None
    except (KeyError, json.JSONDecodeError) as e:
        return None, f"Gist parse error: {e}"


def save_to_gist(gist_id, state, token):
    """Save state dict to gist. Returns (success_bool, error_str_or_None)."""
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": json.dumps(state, indent=2, ensure_ascii=False)
            }
        }
    }
    _, code = _api("PATCH", f"/gists/{gist_id}", data=payload, token=token)
    if code == 200:
        return True, None
    return False, f"Gist save failed ({code})"


def verify_token(token):
    """Quick check: returns (username, None) or (None, error)."""
    data, code = _api("GET", "/user", token=token)
    if code == 200:
        return data.get("login"), None
    return None, data.get("message", f"HTTP {code}")
