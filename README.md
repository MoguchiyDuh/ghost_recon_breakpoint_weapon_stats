# Weapon Stats Scanner

## Overview

This Python script extracts weapon statistics from an on-screen image using OpenCV for image processing and Tesseract OCR for text recognition. The extracted stats are stored in a CSV file for further analysis.

## Features

- Captures a screenshot of the current screen.
- Uses template matching to locate weapon stats.
- Extracts numerical and textual data using OCR.
- Saves the extracted data into a CSV file.
- Plays sound notifications for success and failure.
- Hotkey-based activation (`Ctrl + P` to scan, `Ctrl + Q` to quit).

## Dependencies

Make sure you have the following installed:

- Python 3.x
- OpenCV (`cv2`)
- numpy
- pandas
- PyAutoGUI
- keyboard
- pygame
- pytesseract (Tesseract OCR)

### Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

### Configure Tesseract OCR

Ensure Tesseract OCR is installed and available in your system path. Download it from:
[Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)

## Usage

1. Run the script:

```bash
python main.py
```

2. Press `Ctrl + P` to scan weapon stats from the screen.
3. Press `Ctrl + Q` to exit.
4. Extracted stats will be stored in `stats.csv`.

# Stats Explanation

## 4-AC Assault Rifle Stats

| Stat            | Value         | Description                                                                                                     |
| --------------- | ------------- | --------------------------------------------------------------------------------------------------------------- |
| **Name**        | 4-AC          | Weapon name                                                                                                     |
| **Type**        | Assault Rifle | Weapon category                                                                                                 |
| **Accuracy**    | 60            | Measures horizontal recoil and sight sway                                                                       |
| **Handling**    | 50            | Affects vertical recoil and ADS (aim down sights) speed                                                         |
| **Mobility**    | 43            | Determines movement speed while aiming down sights                                                              |
| **Range**       | 45            | Indicates bullet drop distance                                                                                  |
| **Recoil**      | 45            | ? (you can't change the recoil of the same weapon in game using attachments/perks, so idk what this stat means) |
| **Damage**      | 25.0          | Damage per shot                                                                                                 |
| **Caliber**     | 5.56          | Ammunition type                                                                                                 |
| **RPM**         | 860.0         | Rounds per minute (fire rate)                                                                                   |
| **Reload Time** | 3.1s          | Time taken to reload a magazine                                                                                 |
| **Mag Size**    | 30            | Number of rounds per magazine                                                                                   |
| **DPS**         | 144.42        | Sustained damage per second, including reloads                                                                  |
| **Burst DPS**   | 358.33        | Damage per second while firing one full magazine without reloading                                              |

## All possible perks/proficiencies/attachments that affect weapon stats:

- Proficiencies:
  | Class | Proficiency Name | Values |
  | ------------ | ---------------------- | ----------------------------------------------------------------------- |
  | Assault | Assault Proficiency | +20 _Acc_ / +30 _Mob_ |
  | Panther | Class Proficiency | No _DMG_ reduction on HDGs and SMGs while using Suppressors |
  | Sharpshooter | Deep Lungs | +100% _Breath Control_ |
  | | Long Range Proficiency | -10% _RS_\* / +30 _Han_ |
  | Echelon | Handgun Proficiency | +20% _DMG_ with HDGs / No _DMG_ reduction on HDGs while using Suppressors |
  | Engineer | Piercing bullets | +10% _DMG to Drones_ |
  | | GRL Proficiency | +20% Explosion radius with GRLs |

  ***

  \* **+10% Reload Speed** is displayed in green in the game. However, the value appears to be inverted. Going forward, I will denote it as _-10%_ to indicate that 3.1s becomes 2.79s.

- Perks:
  | Perk Name | Stats |
  | ------------------- | --------------------------------------------------- |
  | Close & Personal | +15% _RS_ / +10 _Mob_ |
  | Pistolero | +20% _DMG_ with HDGs |
  | Rolling Thunder | +20% _DMG_ with SRs / +20% _DMG to Drones_ with SRs |
  | Gunslinger | +15 _Acc_ and +15 _Han_ after a hit |
  | Ballistic Advantage | +60 _Range_ / +15 _Han_ |
  | Sensor Hack | +10% _DMG to Drones_ |
  | Explosives Expert | +20% Explosive _DMG_ |
  | Adrenaline | +20% _RS_ / +40 _Acc_ |

- Attachments:
  | Attachment Name | Stats |
  | ------------------------------- | ---------------------------------------------------------------------------- |
  | Short Barrel | -10% _ADS speed_ / -5% _Vert Rec_ / -10%\* _Range_ |
  | Small Mags | +10% _RS_ |
  | Extended Mags | -10% _RS_ / +15% _Vert Rec_ |
  | Muzzle Breaks & Control Shields | -20% _Hipfire Rec_ / _-5% Shot Spread_ |
  | Compensators | -7% _Vert Rec_ / -10% _Shot Spread_ |
  | Flash Hiders | -20% _Shot Spread_ |
  | Suppressors | -20% _DMG_ |
  | ATPIALx3 | -10% _Hor Rec_ / -7% _ADS speed_/ -10% _Shot Spread_ |
  | ATPIAL HDG Laser | -30% _Hipfire Rec_ / -10% _Shot Spread_ |
  | PEQ-15 | -30% _Hipfire Rec_ |
  | MAWL-DA | +10% _Range_ / -10% _Sway_ / -20% _Shot Spread_ |
  | Range Finder | +15% _Range_ / +15% _ADS speed_ |
  | _Hor Rec_ Stocks | -7% _Hor Rec_ |
  | _Vert Rec_ Stocks | -5% _Vert Rec_ |
  | _ADS speed_ Stocks | -7% _ADS speed_ |
  | Grip Pod | -7% _Vert Rec_ / +10% _Range_ / -15% _ADS movement speed_ |
  | RU Vertical Grip | -7% _ADS speed_ / -15% _Vert Rec_ / +15% _Hor Rec_ |
  | SHIFT Angled Short Foregrip | -7% _ADS speed_ |
  | AFG-2 Angled Foregrip | -10% _ADS speed_ / -5% _Vert Rec_ / +15% _RS_ |
  | Lightweight Vertical Foregrip | -10% _Vert Rec_ / +10% _ADS movement speed_ / +10% _RS_ / +15% _Hor Rec_ |
  | PTK Angled Foregrip | -10% _ADS speed_ / -5% _Vert Rec_ / +10% _Hor Rec_ |
  | RVG Vertical Foregrip | -15% _Vert Rec_ / +15% _Hor Rec_ / +15% _RS_ |
  | SHIFT Vertical Foregrip | -7% _Vert Rec_ |
  | STFG Angled Grip | -10% _ADS speed_ / +10% _ADS movement speed_ / +15% _Hor Rec_ |
  | Tactical Vertical Foregrip | -5% _Vert Rec_ / -7% _Hor Rec_ / +15% _Sway_ / +10% _RS_ |
  | Underbarrel Grenade Launcher | +15% _Sway_ |
  | Vented Angled Foregrip | -7% _ADS speed_ / -5% _Vert Rec_ / +5% _ADS movement speed_ / +15% _Hor Rec_ |

  ***

  \* This is not a flat increase, but a percentage.

- Weapon modifiers: Possible stats are _Acc_, _Han_, _Mob_, _Range_, _DMG to Drones_, _RS_
- Weapon mastery upgrades: You can upgrade _Acc_, _Han_, _Mob_ for every weapon type up to +140 for 40 skill points total on 5th lvl
  | Level | Skill Point Cost | Increase Value |
  |-------|------------------|----------------|
  | 1 | 5 | 25 |
  | 2 | 5 | 25 |
  | 3 | 10 | 25 |
  | 4 | 10 | 25 |
  | 5 | 10 | 40 |
  | | total 40 | total +140 |
