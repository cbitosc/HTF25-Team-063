# TODO List for AI Traffic Violation Detector

## Project Setup
- [x] Create project directory and virtual environment
- [x] Install dependencies (OpenCV, YOLOv8, DeepSORT, Tesseract, Streamlit, etc.)
- [x] Set up project structure with modules

## Core Modules
- [x] config.py: Configuration for models, thresholds, paths
- [x] detection.py: Object detection using YOLOv8 for vehicles, riders, helmets, signals, license plates
- [x] tracking.py: Vehicle and rider tracking using DeepSORT
- [x] violations.py: Logic for detecting violations (signal jumping, helmetless, overspeeding, wrong-lane, triple-riding)
- [x] evidence.py: Generate timestamped images/clips, OCR license plates, store evidence
- [x] main.py: Integrate modules for real-time processing of CCTV feeds

## Dashboard and UI
- [x] dashboard.py: Streamlit app for reviewing violations and evidence

## Advanced Features
- [x] Privacy safeguards: Face blurring in evidence
- [x] Edge deployment optimizations: Lightweight models
- [x] Human-in-the-loop: Review interface

## Testing and Deployment
- [x] Test with sample video feed
- [x] Run dashboard locally
- [x] Optimize for real-time performance
