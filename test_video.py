import cv2
import os

# Test if video6.mp4 can be opened
video_path = '../video6.mp4'  # Path relative to traffic_violation_detector folder
print(f"Looking for video at: {video_path}")
print(f"File exists: {os.path.exists(video_path)}")

cap = cv2.VideoCapture(video_path)
print(f"Video opened: {cap.isOpened()}")

if cap.isOpened():
    ret, frame = cap.read()
    print(f"Frame read: {ret}")
    if ret:
        print(f"Frame shape: {frame.shape}")
    cap.release()
else:
    print("Could not open video6.mp4")
    # Try absolute path
    abs_path = r'C:\Users\GoliReddy\Desktop\video6.mp4'
    print(f"Trying absolute path: {abs_path}")
    cap2 = cv2.VideoCapture(abs_path)
    print(f"Absolute path opened: {cap2.isOpened()}")
    if cap2.isOpened():
        cap2.release()
