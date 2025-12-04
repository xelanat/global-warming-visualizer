# Global Warming Visualizer

A simple web visualizer to scrub through temperature anomaly figures from Berkeley Earth. Currently only displaying the Spatial Variation visualization.

## Usage

1. Images are pulled from Berkeley Earth using the `scrape-berkeley-earth.py` script, which takes in a date range.
    - `python scrape-berkeley-earth.py "01/2025" "12/2025"`
1. They're loaded into the `img/` directory.
1. Simple web interface plots these images on a continuum, where they can be interacted with via slider.

## Controls
- **Slider**: Scrub through frames
- **◀/▶ buttons**: Previous/next frame
- **Keyboard**: Left/right arrows for prev/next
