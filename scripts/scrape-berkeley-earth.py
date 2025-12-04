#!/usr/bin/env python3
"""
Scrape images from a Berkeley Earth monthly temperature update blog post.
Downloads all images from the given month/year report into ../img/

Usage:
  python3 scrape-berkeley-earth.py [mm/YYYY] [mm/YYYY]
  # Example: python3 scrape-berkeley-earth.py 01/2020 12/2020
  # If no args, defaults to current month/year
"""
import sys
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'img')
BASE_URL = 'https://berkeleyearth.org/'

# Helper to get month name
MONTHS = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]

def parse_date_arg(arg):
    # arg: MM/YYYY
    month, year = arg.split('/')
    month = int(month)
    year = int(year)
    if not (1 <= month <= 12):
        raise ValueError(f"Month must be 1-12: {month}")
    return year, month

def get_report_url(month, year):
    return f"{BASE_URL}{month}-{year}-temperature-update/"

def download_images_from_report(url, out_dir):
    """Download relevant images from the given report URL."""
    print(f"Fetching: {url}")
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        print(f"Failed to fetch page: {resp.status_code} {resp.reason}")
        return 0
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Find the first figure.wp-block-image.size-large after h2 containing 'Spatial Variation'
    h2s = soup.find_all('h2')
    spatial_h2 = None
    for h2 in h2s:
        if 'Spatial Variation' in h2.get_text():
            spatial_h2 = h2
            break
    if not spatial_h2:
        print("No <h2> with 'Spatial Variation' found.")
        return 0
    # Traverse siblings after h2
    next_elem = spatial_h2
    target_figure = None
    while next_elem:
        next_elem = next_elem.find_next_sibling()
        if next_elem and next_elem.name == 'figure' and 'wp-block-image' in next_elem.get('class', []) and 'size-large' in next_elem.get('class', []):
            target_figure = next_elem
            break
    if not target_figure:
        print("No figure.wp-block-image.size-large found after 'Spatial Variation' h2.")
        return 0
    img_tag = target_figure.find('img')
    if not img_tag or not img_tag.get('src'):
        print("No <img> found in the target figure.")
        return 0
    src = img_tag.get('src')
    if not src.startswith('http'):
        print(f"Image src is not a valid URL: {src}")
        return 0
    # Save as mm_YYYY.png
    match = re.search(r'(\w+)-(\d+)-temperature-update', url)
    if match:
        month_str, year_str = match.groups()
        month_num = MONTHS.index(month_str.lower()) + 1 if month_str.lower() in MONTHS else 1
        fname = f"{year_str}_{month_num:02d}.png"
    else:
        fname = "unknown.png"
    out_path = os.path.join(out_dir, fname)
    os.makedirs(out_dir, exist_ok=True)
    print(f"Downloading {src} -> {out_path}")
    try:
        r = requests.get(src, stream=True)
        r.raise_for_status()
        with open(out_path, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        print(f"Saved image as {out_path}")
        return 1
    except Exception as e:
        print(f"Failed to download {src}: {e}")
        return 0


def get_date_range():
    """Parse command line args for date range."""
    if len(sys.argv) == 3:
        start = parse_date_arg(sys.argv[1])
        end = parse_date_arg(sys.argv[2])
    else:
        now = datetime.now()
        start = (now.year, now.month)
        end = (now.year, now.month)
    return start, end


def month_year_iter(start, end):
    """Yield (year, month) tuples from start to end inclusive."""
    y, m = start
    ey, em = end
    while (y, m) <= (ey, em):
        yield y, m
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1

def main():
    print("hi")
    start, end = get_date_range()
    print(f"Scraping from {start[1]:02d}/{start[0]} to {end[1]:02d}/{end[0]}")
    for y, m in month_year_iter(start, end):
        url = get_report_url(MONTHS[m-1], y)
        print(f"\n--- Scraping {m:02d}/{y} ---")
        download_images_from_report(url, IMG_DIR)

if __name__ == '__main__':
    main()
