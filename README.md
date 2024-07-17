# README

## Introduction

Mage.space has announced the retirement of their image services and suggested that users download the images they want to keep. Many users have thousands of images, and downloading them by hand is onerous. This software automates a lot of that; it gathers up the URLs of the images that have been marked as "public" by the user and does its best not to download the same image twice.

This tool is designed for users of the Mage UI who need to recover their images. It is intended to be user-friendly and does not require extensive technical knowledge.

## Installation

### Python Installation

1. **Download and Install Python**: Ensure you have Python 3.7 or later installed on your system.
   - **Windows**: Download the installer from the [official Python website](https://www.python.org/downloads/windows/) and run it.
   - **Mac**: Download the installer from the [official Python website](https://www.python.org/downloads/macos/) and run it.

2. **Verify Python Installation**: Open your terminal (Mac) or PowerShell (Windows) and run:
   ```sh
   python --version
   ```
   Ensure it shows Python 3.7 or later.

### Installing Dependencies

1. **Install Selenium**: Run the following command in your terminal (Mac) or PowerShell (Windows):
   ```sh
   pip install selenium
   ```

### Installing ChromeDriver

1. **Download ChromeDriver**: Download the latest ChromeDriver for your platform from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/#stable).
   - **Windows**: Download the zip file, extract it, and place `chromedriver.exe` in a directory of your choice.
   - **Mac**: Download the zip file, extract it, and place `chromedriver` in a directory of your choice.

2. **Set Environment Variable**:
   - **Windows (PowerShell)**:
     ```powershell
     $env:CHROMEDRIVER_PATH = "C:/path/to/your/chromedriver.exe"
     ```
   - **Mac (Terminal)**:
     ```sh
     export CHROMEDRIVER_PATH="/path/to/your/chromedriver"
     ```

## Running the Script

### Command-Line Arguments

- **username**: The Mage user to scrape (required).
- **--scrolls**: Number of page scrolls to do at the start (default: 5).
- **--images**: Number of new images to process (default: 20).

### Example Usage

1. **Windows (PowerShell)**:
   ```powershell
   python scrape.py crywoof --scrolls 10 --images 30
   ```

2. **Mac (Terminal)**:
   ```sh
   python scrape.py crywoof --scrolls 10 --images 30
   ```

### JSON Files

- **processed_images.json**: This file keeps track of the thumbnails (original images) that have been processed to avoid duplicates.
- **main_images.json**: This file stores the URLs of the full-resolution images you want to keep.

## How It Works

1. **Image Detection**: The script identifies all public images on the Mage user profile by scrolling through the page.
2. **Processing Images**: For each image, it checks if it has been processed before. If not, it opens the image popup to retrieve the full-resolution image URL.
3. **Skipping Duplicates**: The script skips any image that has already been processed in previous runs.
4. **Public Images Only**: The script only downloads URLs for public images. It is recommended to go through Mage and ensure only the desired images are public.
5. **Output**: The result is a list of URLs to the full-resolution images stored in `main_images.json`.

### Important Notes

- **Public Images**: Ensure the images you want to keep are public before running the script. Mage does not allow adult images to be public.
- **Privacy**: Once you have scraped the images, consider making them private again.
- **Downloading Images**: The script does not download images during processing to save time and space. You will receive a list of URLs for the full-resolution images. A separate Python program will be provided to download the images if needed.

## Additional Information

After running the script, you can use the URLs in `main_images.json` to download the images yourself or wait for a simple Python program that will handle the downloading for you. Ensure you have sufficient disk space before downloading the images.

By following these instructions, you should be able to automate the process of gathering and downloading your Mage images, saving you significant time and effort. If you have any issues or questions, feel free to reach out for support.
