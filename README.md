# Video ROI Event Trigger and Edge Detection

This repository contains a simple Python script that monitors a region of interest (ROI) in a video stream. When the grayscale intensity in the ROI changes beyond a user-defined threshold, an event is triggered. After the event, you can select a second ROI where edges will be highlighted using the Canny edge detector.

## Requirements

- Python 3
- OpenCV (`opencv-python`)
- NumPy

Install the dependencies with:

```bash
pip install opencv-python numpy
```

## Usage

Run the script with a webcam or a video file:

```bash
python roi_edge_detection.py --video 0
```

Replace `0` with the path to a video file if needed. After starting, follow the on-screen prompts to select the ROIs. Press `q` to quit.
