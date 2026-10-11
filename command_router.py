import re
import spark_state
import pc_control


def _result(reply, action="NONE", target=""):
    return {"action": action, "target": target, "reply": reply}


def handle_command(command):
    text = command.strip()
    low = text.lower()

    if low in {"start engine", "start the engine", "engine start", "activate spark", "start spark"}:
        spark_state.status = "ONLINE"
        spark_state.control_status = "READY"
        return _result("Spark is online.")

    # Deterministic shortcuts for common commands. More complex language goes to the AI.
    m = re.match(r"^(?:search|find) (?:youtube|yt) (?:for )?(.+)$", low, re.I)
    if m:
        target = text[m.start(1):].strip()
        if target.lower().startswith("for "):
            target = target[4:].strip()
        return _result(f"Searching YouTube for {target}.", "SEARCH_YOUTUBE", target)

    m = re.match(r"^(?:search )?(?:spotify) (?:for )?(.+)$", text, re.I)
    if m:
        target = re.sub(r"^(?:search )?spotify (?:for )?", "", text, flags=re.I).strip()
        return _result(f"Searching Spotify for {target}.", "SEARCH_SPOTIFY", target)

    m = re.match(r"^open spotify and search (?:for )?(.+)$", text, re.I)
    if m:
        target = m.group(1).strip()
        return _result(f"Searching Spotify for {target}.", "SEARCH_SPOTIFY", target)

    m = re.match(r"^open youtube and search (?:for )?(.+)$", text, re.I)
    if m:
        target = m.group(1).strip()
        return _result(f"Searching YouTube for {target}.", "SEARCH_YOUTUBE", target)

    if low.startswith("open "):
        target = text[5:].strip()
        if target.lower() in pc_control.APP_ALIASES:
            return _result(f"Opening {target}.", "OPEN_APP", target)
        if target.lower() in pc_control.WEBSITES:
            return _result(f"Opening {target}.", "OPEN_WEBSITE", target)

    if low in {"left click", "click"}:
        return _result("Done.", "LEFT_CLICK")
    if low == "right click":
        return _result("Done.", "RIGHT_CLICK")
    if low == "double click":
        return _result("Done.", "DOUBLE_CLICK")
    if "scroll up" in low:
        return _result("Scrolling up.", "SCROLL_UP")
    if "scroll down" in low:
        return _result("Scrolling down.", "SCROLL_DOWN")
    if low in {"close window", "close this window"}:
        return _result("Closing the window.", "CLOSE_WINDOW")
    if low in {"minimize window", "minimize this window"}:
        return _result("Minimizing the window.", "MINIMIZE_WINDOW")
    if low in {"maximize window", "maximize this window"}:
        return _result("Maximizing the window.", "MAXIMIZE_WINDOW")
    if low.startswith("type "):
        return _result("Typing that.", "TYPE_TEXT", text[5:])
    if low.startswith("press "):
        return _result("Done.", "PRESS_KEY", text[6:].strip())

    return None
