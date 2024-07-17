# README

## Introduction

Mage.space has announced the retirement of their image services and suggested that users download the images they want to keep. Many users have thousands of images, and downloading them by hand is onerous. This software automates a lot of that; it gathers up the URLs of the images that have been marked as "public" by the user and does its best not to download the same image twice.

This tool is designed for users of the Mage UI who need to recover their images. It is intended to be user-friendly and not require extensive technical knowledge. We'll see how well I did with that. 

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

Here's what this means; the mage username should be obvious.  The way this works is by loading your mage profile, scrolling down some number of pages (to make mage load the thumbnails) then it walks through those thumbnails to find the images.  The --scrolls argument tells how many pages to scroll before it starts, and --images is how many images to load before it stops. 

This software keeps track of the thumbnails it expanded in earlier sessions, and doesn't repeat them.  So you might want to run it several times to make sure you got them all.  Or make --images much larger than --scrolls (say, 10 times as big), and it should get them all. 
This software is pretty rough, so it could break.  I've tried to make it resilient to a bunch of error modes, so that it continues when that happens, and all of its progress so far is saved in the two output files, processed_images.json and main_images.json.  
The way I plan to use this is to mark images I don't like as "private", then run this on the remaining ones.  When I feel that I have got the images I want, I will make the first few pages as "private" and run again.  Repeat until mage turns us off. 

This results in a list of URLs to the high-resolution images, stored in main_images.json.  I'm going to write a program later this weel that will actcually do the downloads from those links.  Get your hard drives ready. 

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
