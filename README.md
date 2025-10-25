# AI Traffic Violation Detector

A computer-vision–based system designed to monitor traffic violations in real time, addressing challenges such as signal jumping, helmetless riding, overspeeding, wrong-lane driving, and triple-riding.

## Features

- **Real-time Detection**: Analyzes live CCTV feeds for multiple violation types
- **Object Detection**: Uses YOLOv8 for detecting vehicles, riders, and traffic signals
- **Object Tracking**: DeepSORT for tracking vehicles and riders across frames
- **Violation Detection**: Specialized logic for each violation type
- **Evidence Generation**: Timestamped images and video clips with license plate data
- **Privacy Protection**: Face blurring for privacy-by-design
- **Dashboard**: Streamlit-based interface for reviewing violations
- **Edge Deployment**: Optimized for near-real-time performance

## Installation

1. Clone or download the project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Detector

```bash
python main.py
```

This will start live detection using your default webcam. To use a video file:

```python
from main import TrafficViolationDetector
detector = TrafficViolationDetector()
detector.run_live_detection('path/to/video.mp4')
```

### Running the Dashboard

```bash
streamlit run dashboard.py
```

Access the dashboard at `http://localhost:8501`

## Project Structure

```
traffic_violation_detector/
├── config.py              # Configuration settings
├── detection.py           # Object detection modules
├── tracking.py            # Object tracking with DeepSORT
├── violations.py          # Violation detection logic
├── evidence.py            # Evidence generation and management
├── main.py                # Main application
├── dashboard.py           # Streamlit dashboard
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── models/                # Pre-trained models (to be added)
├── evidence/              # Generated evidence storage
│   ├── images/
│   └── clips/
└── logs/                  # Application logs
```

## Violation Types Detected

1. **Signal Jumping**: Vehicles crossing stop lines during red lights
2. **Helmetless Riding**: Motorcyclists without helmets
3. **Overspeeding**: Vehicles exceeding speed limits
4. **Wrong-lane Driving**: Vehicles in incorrect lanes
5. **Triple Riding**: More than 2 persons on motorcycles

## Configuration

Edit `config.py` to customize:
- Model paths
- Detection thresholds
- Video settings
- Evidence storage locations
- Privacy settings

## Requirements

- Python 3.8+
- Webcam or CCTV feed
- Tesseract OCR (for license plate recognition)
- Sufficient storage for evidence

## Future Enhancements

- Custom helmet detection model
- Lane detection for wrong-lane violations
- Traffic light color recognition
- Integration with traffic authority systems
- Mobile app for officers
- Advanced analytics and reporting

## License

This project is for educational and research purposes. Ensure compliance with local laws and privacy regulations when deploying.

## Contributing

Contributions are welcome! Please open issues for bugs or feature requests.
