import pygetwindow as gw
import pyautogui
import pyperclip
import time

import win32gui

def enum_windows_callback(hwnd, results):
    title = win32gui.GetWindowText(hwnd)
    if "YouTube" in title and win32gui.IsWindowVisible(hwnd):
        results.append((hwnd, title))

def find_youtube_windows():
    youtube_windows = []

    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "YouTube" in title:
                youtube_windows.append((hwnd, title))
    win32gui.EnumWindows(enum_callback, None)
    return youtube_windows

def get_youtube_url_from_browser():
    for window in gw.getAllTitles():
        if "YouTube" in window:
            yt_window = gw.getWindowsWithTitle(window)[0]
            yt_window.activate()
            break
    else:
        print("YouTube window not found.")
        return None

    time.sleep(1)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    url = pyperclip.paste()
    if "youtube.com/watch" in url:
        return url
    else:
        return None

def get_youtube_video_info(video_url):
    if not video_url:
        return None
    try:
        command = [
            "yt-dlp",
            "--skip-download",
            "--no-warnings",
            "--print-json",
            video_url
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        video_info = json.loads(result.stdout)
        return {
            "title": video_info.get("title"),
            "uploader": video_info.get("uploader"),
            "duration": video_info.get("duration_string"),
            "thumbnail": video_info.get("thumbnail")
        }
    except Exception as e:
        print("Error fetching video info:", e)
        return None

while True:
    window = find_youtube_windows()
    for hwnd, title in window:
        print(f"HWND: {hwnd}, Title: {title}")
        video_info = get_youtube_video_info(get_youtube_url_from_browser())
        # if video_info:
        #     print(f"Title: {video_info['title']}")
        #     print(f"Uploader: {video_info['uploader']}")
        #     print(f"Duration: {video_info['duration']}")
        #     print(f"Thumbnail: {video_info['thumbnail']}")

# def get_active_window_title():
#     window = win32gui.GetForegroundWindow()
#     return win32gui.GetWindowText(window)
#
# title = get_active_window_title()
# if "YouTube" in title:
#     print("YouTube video:", title)
# else:
#     print("Active window:", title)