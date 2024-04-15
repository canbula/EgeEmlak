import pyautogui
import platform
import time
import random
import os
import csv


HOME = os.path.expanduser("~")


def get_mouse_position():
    return pyautogui.position()


def get_screen_size():
    return pyautogui.size()


def move_mouse(x, y, duration=1):
    pyautogui.moveTo(x, y, duration=duration)


def click_mouse(x=None, y=None):
    pyautogui.click(x, y)


def vertical_scroll(clicks, x=None, y=None):
    pyautogui.scroll(clicks, x, y)


def horizontal_scroll(clicks, x=None, y=None):
    pyautogui.keyDown("shift")
    pyautogui.scroll(clicks, x, y)
    pyautogui.keyUp("shift")


def img_position(img_path, region=None, confidence=0.9):
    factor = 2 if platform.system() == "Darwin" else 1
    try:
        x, y, w, h = pyautogui.locateOnScreen(
            img_path, region=region, confidence=confidence
        )
        return (x + w / 2) / factor, (y + h / 2) / factor
    except pyautogui.ImageNotFoundException:
        return None


def close_window(duration=1):
    window_buttons = img_position("window_buttons.png")
    if window_buttons:
        move_mouse(window_buttons[0] - 20, window_buttons[1])
        time.sleep(duration)
        click_mouse()
    else:
        pyautogui.press("esc")
        time.sleep(duration)
        if platform.system() == "Darwin":
            pyautogui.keyDown("command")
            pyautogui.press("w")
            pyautogui.keyUp("command")
            # pyautogui.hotkey("command", "w", interval=0.5)
        else:
            pyautogui.keyDown("ctrl")
            pyautogui.press("w")
            pyautogui.keyUp("ctrl")
            # pyautogui.hotkey("ctrl", "w", interval=0.5)


def get_the_most_recent_file(folder=""):
    files = os.listdir(folder)
    paths = [
        os.path.join(folder, basename)
        for basename in files
        if basename.endswith(".csv")
    ]
    return max(paths, key=os.path.getctime)


if __name__ == "__main__":
    city = "izmir5"
    page = 1
    while True:
        print(f"{city} page {page} is downloading...")
        move_mouse(700, 150)
        time.sleep(3 + random.random() * 2)
        click_mouse()
        time.sleep(1)
        print("Finding the extension logo...")
        extension_logo_position = img_position("extension_logo.png")
        print("Extension logo position: ", extension_logo_position)
        move_mouse(*extension_logo_position)
        print("Clicking the extension logo...")
        click_mouse()
        time.sleep(2)
        print("Finding the CSV button...")
        csv_button_position = img_position("csv_button.png")
        print("CSV button position: ", csv_button_position)
        move_mouse(*csv_button_position)
        time.sleep(1)
        print("Clicking the CSV button...")
        click_mouse()
        time.sleep(1)
        print("Closing the extension...")
        close_window()
        time.sleep(1)
        most_recent_file = get_the_most_recent_file(f"{HOME}/Downloads")
        print("Downloaded file: ", most_recent_file)
        # move the file to the desired location
        print("Moving the file to the data folder...")
        os.rename(most_recent_file, f"{os.getcwd()}/data/{city}_{page:03d}.csv")
        move_mouse(700, 150)
        time.sleep(1)
        click_mouse()
        print("Scrolling...")
        pyautogui.keyDown("command")
        time.sleep(0.5)
        pyautogui.press("down")
        pyautogui.press("down")
        pyautogui.press("down")
        pyautogui.keyUp("command")
        vertical_scroll(-5000)
        time.sleep(1)
        horizontal_scroll(-5000)
        time.sleep(3 + random.random() * 2)
        print("Finding the next button...")
        next_button_position = img_position("next_button.png")
        print("Next button position: ", next_button_position)
        while not next_button_position:
            print("Trying to find the next button...")
            vertical_scroll(-5000)
            time.sleep(0.1)
            next_button_position = img_position("next_button.png")
        move_mouse(*next_button_position)
        print("Clicking the next button...")
        click_mouse()
        time.sleep(1)
        print(f"{city} page {page} is downloaded.")
        page += 1
        # if shift is pressed, break the loop
        if pyautogui.keyDown("shift"):
            break
