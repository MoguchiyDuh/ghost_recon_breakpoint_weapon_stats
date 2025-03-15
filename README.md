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
