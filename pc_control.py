import subprocess
import time
import webbrowser
from urllib.parse import quote_plus

try:
    import pyautogui
    pyautogui.PAUSE = 0.03
except Exception:
    pyautogui = None

APP_ALIASES = {
    "chrome": "Google Chrome",
    "google chrome": "Google Chrome",
    "safari": "Safari",
    "finder": "Finder",
    "calculator": "Calculator",
    "notes": "Notes",
    "textedit": "TextEdit",
    "notepad": "TextEdit",
    "terminal": "Terminal",
    "settings": "System Settings",
    "system settings": "System Settings",
    "discord": "Discord",
    "spotify": "Spotify",
    "music": "Music",
    "visual studio code": "Visual Studio Code",
    "vs code": "Visual Studio Code",
    "code": "Visual Studio Code",
}

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "instagram": "https://www.instagram.com",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "spotify web": "https://open.spotify.com",
    "spotify": "https://open.spotify.com",
}


def open_app(name: str) -> str:
    name = name.lower().strip()
    app = APP_ALIASES.get(name, name)
    try:
        subprocess.run(["open", "-a", app], check=True, timeout=8)
        return f"Opening {name}."
    except Exception as exc:
        print(f"OPEN_APP ERROR: {exc}")
        return f"I couldn't open {name}."


def open_website(site: str) -> str:
    site = site.strip()
    key = site.lower()
    url = WEBSITES.get(key)
    if not url:
        if site.startswith(("http://", "https://")):
            url = site
        elif "." in site:
            url = "https://" + site
        else:
            return f"I don't know that website."
    webbrowser.open(url)
    return f"Opening {site}."


def search_youtube(query: str) -> str:
    query = query.strip()
    if not query:
        return "What should I search for on YouTube?"
    url = "https://www.youtube.com/results?search_query=" + quote_plus(query)
    webbrowser.open(url)
    return f"Searching YouTube for {query}."


def search_google(query: str) -> str:
    query = query.strip()
    if not query:
        return "What should I search for?"
    url = "https://www.google.com/search?q=" + quote_plus(query)
    webbrowser.open(url)
    return f"Searching the web for {query}."


def search_spotify(query: str) -> str:
    query = query.strip()
    if not query:
        return "What should I search for on Spotify?"
    # Spotify desktop understands spotify:search:<query> on macOS.
    uri = "spotify:search:" + quote_plus(query)
    try:
        subprocess.run(["open", "-a", "Spotify", uri], check=True, timeout=8)
        return f"Searching Spotify for {query}."
    except Exception as exc:
        print(f"SPOTIFY SEARCH ERROR: {exc}")
        # Fall back to Spotify Web if the desktop app/URI handler is unavailable.
        webbrowser.open("https://open.spotify.com/search/" + quote_plus(query))
        return f"I couldn't open Spotify directly, so I opened Spotify Web and searched for {query}."


def open_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return "That isn't a valid web address."
    webbrowser.open(url)
    return "Opening it."


def _need_pyautogui():
    if pyautogui is None:
        raise RuntimeError("PyAutoGUI is not installed. Run the Spark launcher again.")


def left_click():
    _need_pyautogui(); pyautogui.click(); return "Done."


def right_click():
    _need_pyautogui(); pyautogui.rightClick(); return "Done."


def double_click():
    _need_pyautogui(); pyautogui.doubleClick(); return "Done."


def scroll_up():
    _need_pyautogui(); pyautogui.scroll(5); return "Scrolling up."


def scroll_down():
    _need_pyautogui(); pyautogui.scroll(-5); return "Scrolling down."


def press_key(key: str):
    _need_pyautogui()
    aliases = {"escape": "esc", "return": "enter"}
    key = aliases.get(key.lower().strip(), key.lower().strip())
    allowed = {"enter", "esc", "tab", "space", "backspace", "delete", "up", "down", "left", "right", "home", "end", "pageup", "pagedown", *{f"f{i}" for i in range(1, 13)}}
    if key not in allowed:
        return "That key is not allowed."
    pyautogui.press(key)
    return f"Pressed {key}."


def type_text(text: str):
    _need_pyautogui(); pyautogui.write(str(text), interval=0.015); return "Typing that."


def shortcut(name: str):
    _need_pyautogui()
    shortcuts = {
        "copy": ("command", "c"), "paste": ("command", "v"),
        "undo": ("command", "z"), "redo": ("command", "shift", "z"),
        "select all": ("command", "a"), "save": ("command", "s"),
        "find": ("command", "f"),
    }
    combo = shortcuts.get(name.lower().strip())
    if not combo:
        return "Unknown shortcut."
    pyautogui.hotkey(*combo)
    return f"{name.title()}."


def close_window():
    _need_pyautogui(); pyautogui.hotkey("command", "w"); return "Closing the window."


def minimize_window():
    _need_pyautogui(); pyautogui.hotkey("command", "m"); return "Minimizing the window."


def maximize_window():
    script = '''tell application "System Events"
        tell (first application process whose frontmost is true)
            try
                perform action "AXFullScreen" of window 1
            end try
        end tell
    end tell'''
    try:
        subprocess.run(["osascript", "-e", script], check=True, timeout=5)
        return "Maximizing the window."
    except Exception as exc:
        print(f"MAXIMIZE ERROR: {exc}")
        return "I couldn't maximize the window."


def execute_action(action, target=""):
    action = str(action or "NONE").upper().strip()
    target = str(target or "").strip()
    print(f"[ACTION] {action} | {target}")

    handlers = {
        "OPEN_APP": lambda: open_app(target),
        "OPEN_WEBSITE": lambda: open_website(target),
        "OPEN_URL": lambda: open_url(target),
        "SEARCH_YOUTUBE": lambda: search_youtube(target),
        "SEARCH_SPOTIFY": lambda: search_spotify(target),
        "SEARCH_WEB": lambda: search_google(target),
        "LEFT_CLICK": left_click,
        "RIGHT_CLICK": right_click,
        "DOUBLE_CLICK": double_click,
        "SCROLL_UP": scroll_up,
        "SCROLL_DOWN": scroll_down,
        "PRESS_KEY": lambda: press_key(target),
        "TYPE_TEXT": lambda: type_text(target),
        "CLOSE_WINDOW": close_window,
        "MINIMIZE_WINDOW": minimize_window,
        "MAXIMIZE_WINDOW": maximize_window,
        "SHORTCUT": lambda: shortcut(target),
    }
    if action == "NONE":
        return None
    handler = handlers.get(action)
    return handler() if handler else "I don't know how to perform that action."
