import argparse
import cv2
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="ROI event trigger and edge detection")
    parser.add_argument('--video', type=str, default=0,
                        help='Path to video file or camera index (default: 0)')
    parser.add_argument('--threshold', type=float, default=20.0,
                        help='Gray value change threshold to trigger event')
    return parser.parse_args()


def select_roi(window_name, frame):
    roi = cv2.selectROI(window_name, frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow(window_name)
    x, y, w, h = roi
    if w == 0 or h == 0:
        return None
    return x, y, w, h


def main():
    args = parse_args()
    video_source = args.video
    try:
        video_source = int(video_source)
    except ValueError:
        pass
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Cannot open video source")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read from video source")
        cap.release()
        return

    first_roi = select_roi("Select ROI for gray monitoring", frame)
    if first_roi is None:
        print("No ROI selected. Exiting.")
        cap.release()
        return

    x1, y1, w1, h1 = first_roi
    baseline_gray = cv2.cvtColor(frame[y1:y1+h1, x1:x1+w1], cv2.COLOR_BGR2GRAY).mean()

    event_triggered = False
    second_roi = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_region = cv2.cvtColor(frame[y1:y1+h1, x1:x1+w1], cv2.COLOR_BGR2GRAY)
        current_mean = gray_region.mean()

        if not event_triggered and abs(current_mean - baseline_gray) > args.threshold:
            print("Event triggered: gray value changed")
            event_triggered = True
            second_roi = select_roi("Select ROI for edge detection", frame)
            if second_roi is None:
                print("No second ROI selected. Exiting.")
                break

        if event_triggered and second_roi is not None:
            x2, y2, w2, h2 = second_roi
            gray2 = cv2.cvtColor(frame[y2:y2+h2, x2:x2+w2], cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray2, 100, 200)
            edge_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            frame[y2:y2+h2, x2:x2+w2] = edge_bgr

        cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
