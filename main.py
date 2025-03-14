import re
import pytesseract
import cv2
import pyautogui
import keyboard
import numpy as np
import os
import json
import pygame

pygame.mixer.init()


def play_sound(file_path: str):
    try:
        sound = pygame.mixer.Sound(file_path)
        sound.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")


def get_stats(image: np.ndarray) -> dict:
    stats = {}
    dir_path = "./weapon_stats_images"
    needles = [
        f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
    ]

    stat_p1, stat_p2 = None, None

    for needle_path in needles:
        needle = cv2.imread(os.path.join(dir_path, needle_path))
        result = cv2.matchTemplate(image, needle, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.8

        if max_val >= threshold:
            needle_width = needle.shape[1]
            needle_height = needle.shape[0]
            needle_p1 = max_loc
            needle_p2 = (max_loc[0] + needle_width, max_loc[1] + needle_height)

            stat_p1 = (needle_p1[0], needle_p2[1] + 5)
            stat_p2 = (needle_p1[0] + 435, needle_p2[1] + 5)
            roi = image[stat_p1[1] : stat_p2[1] + 1, stat_p1[0] : stat_p2[0] + 1]
            white_pixels = np.sum((roi >= 200) & (roi <= 255))
            total_pixels = roi.size

            if total_pixels > 0:
                white_percentage = (white_pixels / total_pixels) * 100
                stats[needle_path.replace(".png", "")] = int(white_percentage)

    if stat_p1 is not None and stat_p2 is not None:
        add_stats_p1 = (stat_p1[0], stat_p1[1] + 12)
        add_stats_p2 = (add_stats_p1[0] + 300, add_stats_p1[1] + 100)
        add_stats = image[
            add_stats_p1[1] : add_stats_p2[1], add_stats_p1[0] : add_stats_p2[0]
        ]
        gray_add_stats = cv2.cvtColor(add_stats, cv2.COLOR_BGR2GRAY)
        _, thresh_add_stats = cv2.threshold(gray_add_stats, 100, 255, cv2.THRESH_BINARY)

        extracted_text = pytesseract.image_to_string(thresh_add_stats)
        numbers = re.findall(r"\d+\.\d+|\d+", extracted_text)
        numbers = [float(num) if "." in num else int(num) for num in numbers]

        keys = ("damage", "caliber", "rpm", "reload time", "mag size")
        for key, number in zip(keys, numbers):
            stats[key] = number

    return stats


def store_stats_list(name: str, stats: dict):
    with open("stats.json", "r") as file:
        stats_list = json.load(file)

    stats_list[name] = stats

    with open("stats.json", "w") as file:
        json.dump(stats_list, file, indent=4)
    print(f"Stored {name}:{stats}")


def get_weapon_name(image: np.ndarray) -> str:
    needle = cv2.imread("left_name_text.png")

    result = cv2.matchTemplate(image, needle, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8
    if max_val >= threshold:
        width = needle.shape[1]
        height = needle.shape[0]
        p1 = (max_loc[0] + width, max_loc[1])
        p2 = (max_loc[0] + width + 350, max_loc[1] + height)

        roi = image[p1[1] : p2[1], p1[0] : p2[0]]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh_roi = cv2.threshold(gray_roi, 70, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(thresh_roi)
        return text.strip()
    return None


def main():
    image = pyautogui.screenshot()
    # image = Image.open("tests/image.png")
    image_rgb = np.array(image)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    try:
        stats = get_stats(image_bgr)
        name = get_weapon_name(image_bgr)
        store_stats_list(name, stats)
        play_sound("success.mp3")
    except Exception as e:
        print("Unable to scan the weapon:", e)
        play_sound("error.mp3")


if __name__ == "__main__":
    print("Ready to scan")
    keyboard.add_hotkey("ctrl+p", main)
    keyboard.wait("ctrl+q")
