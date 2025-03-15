from dataclasses import dataclass, fields
from typing import Dict, Optional, Tuple

import cv2
import keyboard
import numpy as np
import pandas as pd
import pyautogui
import pygame
import pytesseract


@dataclass
class Weapon:
    """Represents a weapon with its attributes."""

    name: Optional[str] = None
    type: Optional[str] = None
    accuracy: Optional[int] = None
    handling: Optional[int] = None
    range: Optional[int] = None
    mobility: Optional[int] = None
    recoil: Optional[int] = None
    damage: Optional[int] = None
    caliber: Optional[str] = None
    reload_time: Optional[float] = None
    mag_size: Optional[int] = None
    rpm: Optional[int] = None

    @property
    def dps(self):
        if self.type == "Shotgun" and self.reload_time < 1:
            return (self.damage * self.mag_size) / (
                (self.mag_size / (self.rpm / 60)) + (self.reload_time * self.mag_size)
            )
        elif self.type in ("Handgun", "Sniper Rifle"):
            return None
        else:
            return (self.damage * self.mag_size) / (
                (self.mag_size / (self.rpm / 60)) + self.reload_time
            )

    @property
    def burst_dps(self):
        if self.type in ("Handgun", "Sniper Rifle"):
            return None
        else:
            return (self.damage * self.mag_size) / (self.mag_size / (self.rpm / 60))

    def to_dict(self) -> Dict[str, Optional[str | int | float]]:
        """Converts the Weapon instance to a dictionary."""
        return {field.name: getattr(self, field.name) for field in fields(self)} | {
            "dps": self.dps,
            "burst_dps": self.burst_dps,
        }


def match_template(
    image_gray: np.ndarray, template_path: str, threshold: float = 0.8
) -> Optional[Tuple[Tuple[int, int], float]]:
    """Matches a template in the grayscale image and returns the location and confidence if above the threshold."""
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return (max_loc, max_val) if max_val >= threshold else None


def extract_bar_stat(image_gray: np.ndarray, bar_roi: np.ndarray) -> int:
    """Extracts the percentage of white pixels in a bar ROI to represent the stat value."""
    white_pixels = np.sum((bar_roi >= 200) & (bar_roi <= 255))
    total_pixels = bar_roi.size
    return int((white_pixels / total_pixels) * 100) if total_pixels > 0 else 0


def extract_text_from_roi(
    roi: np.ndarray,
    config: str = r"--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.",
) -> str:
    """Extracts text from an ROI using Tesseract OCR."""
    text = pytesseract.image_to_string(roi, config=config).strip()
    if not text:
        thresh_roi = cv2.adaptiveThreshold(
            roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        text = pytesseract.image_to_string(thresh_roi, config=config).strip()
    return text


def get_stats(image: np.ndarray) -> Tuple[np.ndarray, Weapon]:
    """Extracts weapon stats from an image using template matching and OCR."""
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    weapon_stats = Weapon()

    # Extract bar stats (accuracy, handling, range, mobility, recoil)
    bar_needles = {
        "accuracy": "weapon_bars/accuracy.png",
        "handling": "weapon_bars/handling.png",
        "range": "weapon_bars/range.png",
        "mobility": "weapon_bars/mobility.png",
        "recoil": "weapon_bars/recoil.png",
    }

    for stat_name, template_path in bar_needles.items():
        match_result = match_template(image_gray, template_path)
        if match_result:
            max_loc, _ = match_result
            needle_width, needle_height = cv2.imread(
                template_path, cv2.IMREAD_GRAYSCALE
            ).shape[::-1]

            # Draw rectangle around matched bar name and bar itself (debugging)
            needle_p1 = max_loc
            needle_p2 = (max_loc[0] + needle_width, max_loc[1] + needle_height)
            cv2.rectangle(image, needle_p1, needle_p2, (0, 255, 0), 2)

            # Define region of interest (ROI) for the bar's fill area
            bar_p1 = (needle_p1[0], needle_p2[1] + 5)
            bar_p2 = (needle_p1[0] + 435, needle_p2[1] + 6)
            cv2.rectangle(image, bar_p1, bar_p2, (0, 255, 0), 1)  # Debugging
            bar_roi = image_gray[bar_p1[1] : bar_p2[1], bar_p1[0] : bar_p2[0]]

            # Calculate and set the stat value
            setattr(weapon_stats, stat_name, extract_bar_stat(image_gray, bar_roi))

    # Define stat_needles with multiple possible paths for each stat
    stat_needles = {
        "damage": {"paths": ("weapon_stats/damage.png",), "width": 30},
        "caliber": {
            "paths": ("weapon_stats/caliber.png", "weapon_stats/caliber_buckshot.png"),
            "width": 120,
        },
        "reload_time": {"paths": ("weapon_stats/reload time.png",), "width": 50},
        "mag_size": {"paths": ("weapon_stats/mag size.png",), "width": 50},
        "rpm": {"paths": ("weapon_stats/rpm.png",), "width": 50},
    }

    # Define the region of interest (ROI) for stats extraction
    stats_roi_p1 = (max_loc[0], max_loc[1] + needle_height + 15)
    stats_roi_p2 = (max_loc[0] + 270, stats_roi_p1[1] + 110)
    stats_roi = image[
        stats_roi_p1[1] : stats_roi_p2[1], stats_roi_p1[0] : stats_roi_p2[0]
    ]
    stats_roi_gray = cv2.cvtColor(stats_roi, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(image, stats_roi_p1, stats_roi_p2, (0, 128, 255), 2)  # Debugging

    # Iterate through each stat and its possible paths
    for stat_name, params in stat_needles.items():
        for template_path in params["paths"]:
            match_result = match_template(stats_roi_gray, template_path)
            if match_result:
                max_loc, _ = match_result
                needle_width, needle_height = cv2.imread(
                    template_path, cv2.IMREAD_GRAYSCALE
                ).shape[::-1]

                # Draw rectangle around matched stat name (debugging)
                needle_p1 = max_loc
                needle_p2 = (max_loc[0] + needle_width, max_loc[1] + needle_height)
                cv2.rectangle(stats_roi, needle_p1, needle_p2, (0, 255, 255), 1)

                # Define ROI for the stat value next to the matched name
                stat_p1 = (needle_p2[0], needle_p1[1] - 5)
                stat_p2 = (stat_p1[0] + params["width"], needle_p2[1] + 5)
                roi = stats_roi_gray[stat_p1[1] : stat_p2[1], stat_p1[0] : stat_p2[0]]
                cv2.rectangle(
                    stats_roi, stat_p1, stat_p2, (0, 255, 255), 1
                )  # Debugging

                # Extract and set the stat value
                text = extract_text_from_roi(roi)
                if stat_name == "caliber":
                    setattr(weapon_stats, stat_name, text)
                elif stat_name == "reload_time":
                    setattr(weapon_stats, stat_name, float(text))
                else:
                    setattr(weapon_stats, stat_name, int(text))
                break

    # Extract weapon name
    match_result = match_template(image_gray, "./blueprint_icon.png")
    if match_result:
        max_loc, _ = match_result
        needle_width, needle_height = cv2.imread(
            "./blueprint_icon.png", cv2.IMREAD_GRAYSCALE
        ).shape[::-1]

        # Draw rectangle around matched blueprint icon (debugging)
        blueprint_p1 = max_loc
        blueprint_p2 = (blueprint_p1[0] + needle_width, max_loc[1] + needle_height)
        cv2.rectangle(image, blueprint_p1, blueprint_p2, (255, 128, 0), 2)

        # Define the weapon name ROI and draw a rectangle around it (debugging)
        name_p1 = (blueprint_p2[0], blueprint_p1[1])
        name_p2 = (name_p1[0] + 300, blueprint_p2[1])
        roi = image_gray[name_p1[1] : name_p2[1], name_p1[0] : name_p2[0]]
        cv2.rectangle(image, name_p1, name_p2, (255, 255, 0), 2)

        # Extract and set the weapon name
        weapon_stats.name = extract_text_from_roi(roi, config="")

        # Define the weapon type roi and draw a rectangle around it
        type_p1 = (blueprint_p1[0], blueprint_p1[1] - 40)
        type_p2 = (type_p1[0] + 350, blueprint_p1[1])
        roi = image_gray[type_p1[1] : type_p2[1], type_p1[0] : type_p2[0]]
        cv2.rectangle(image, type_p1, type_p2, (255, 255, 0), 2)

        # Extract the weapon type
        weapon_stats.type = extract_text_from_roi(roi, config="")

    return image, weapon_stats


pygame.mixer.init()


def play_sound(file_path: str):
    try:
        sound = pygame.mixer.Sound("sounds/" + file_path)
        sound.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")


def store_stats_to_csv(weapon_stats: Weapon, csv_file_path: str) -> None:
    """
    Stores the weapon stats into an existing CSV file. If the file doesn't exist or is empty,
    it initializes the file with the correct column headers.

    Args:
        weapon_stats (Weapon): An instance of the Weapon class containing the stats.
        csv_file_path (str): Path to the existing CSV file.
    """

    stats_dict = weapon_stats.to_dict()
    stats_df = pd.DataFrame([stats_dict])
    try:
        existing_df = pd.read_csv(csv_file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        existing_df = pd.DataFrame(columns=stats_df.columns)
    updated_df = pd.concat([existing_df, stats_df], ignore_index=True)
    updated_df.to_csv(csv_file_path, index=False)


def main():
    image = pyautogui.screenshot()
    image_rgb = np.array(image)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    try:
        image, stats = get_stats(image_bgr)
        store_stats_to_csv(stats, "stats.csv")
        play_sound("success.mp3")
    except Exception as e:
        print("Unable to scan the weapon:", e)
        play_sound("error.mp3")


if __name__ == "__main__":
    print("Ready to scan, CTRL+P - scan, CTRL+Q - exit")
    keyboard.add_hotkey("ctrl+p", main)
    keyboard.wait("ctrl+q")
