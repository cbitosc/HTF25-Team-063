import cv2
import numpy as np
import pytesseract
import logging

logger = logging.getLogger(__name__)

class ObjectDetector:
    def __init__(self, model_path='models/yolov8n.pt'):
        # Placeholder for YOLO model - will use OpenCV's DNN module for simplicity
        self.net = None
        self.classes = []
        self.vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
        self.person_class = 0
        self.traffic_light_class = 9

    def detect_objects(self, frame):
        """
        Detect objects in the frame using OpenCV DNN (mock implementation for testing)
        Returns: detections as list of dicts with bbox, class_id, confidence
        """
        # Mock detections for testing - simulate realistic traffic scenarios
        import random

        detections = []
        height, width = frame.shape[:2]

        # Simulate varying number of vehicles (2-8)
        num_vehicles = random.randint(2, 8)

        for i in range(num_vehicles):
            # Random positions for vehicles
            x1 = random.randint(50, width - 150)
            y1 = random.randint(100, height - 150)
            x2 = x1 + random.randint(80, 120)
            y2 = y1 + random.randint(60, 100)

            # Alternate between cars and motorcycles
            class_id = 2 if i % 2 == 0 else 3  # car or motorcycle
            label = 'car' if class_id == 2 else 'motorcycle'

            detections.append({
                'bbox': (x1, y1, x2, y2),
                'class_id': class_id,
                'confidence': random.uniform(0.7, 0.95),
                'label': label
            })

        # Add some persons (riders)
        num_persons = random.randint(1, num_vehicles)
        for i in range(num_persons):
            # Position near some vehicles
            vehicle = detections[i % len(detections)]
            vx1, vy1, vx2, vy2 = vehicle['bbox']

            # Person near vehicle
            px1 = vx1 + random.randint(-20, 20)
            py1 = vy1 - random.randint(30, 50)
            px2 = px1 + random.randint(20, 40)
            py2 = py1 + random.randint(40, 60)

            detections.append({
                'bbox': (px1, py1, px2, py2),
                'class_id': 0,  # person
                'confidence': random.uniform(0.75, 0.9),
                'label': 'person'
            })

        # Occasionally add traffic light
        if random.random() < 0.3:
            tx1 = random.randint(10, 50)
            ty1 = random.randint(10, 50)
            tx2 = tx1 + 30
            ty2 = ty1 + 80

            detections.append({
                'bbox': (tx1, ty1, tx2, ty2),
                'class_id': 9,  # traffic light
                'confidence': random.uniform(0.8, 0.95),
                'label': 'traffic light'
            })

        return detections

    def detect_vehicles(self, detections):
        """Filter detections for vehicles"""
        return [d for d in detections if d['class_id'] in self.vehicle_classes]

    def detect_persons(self, detections):
        """Filter detections for persons"""
        return [d for d in detections if d['class_id'] == self.person_class]

    def detect_traffic_lights(self, detections):
        """Filter detections for traffic lights"""
        return [d for d in detections if d['class_id'] == self.traffic_light_class]

class LicensePlateDetector:
    def __init__(self):
        # Initialize Tesseract OCR
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path if needed

    def extract_license_plate(self, frame, bbox):
        """
        Extract license plate text from a cropped region
        """
        x1, y1, x2, y2 = bbox
        plate_img = frame[y1:y2, x1:x2]

        # Preprocess image for better OCR
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        try:
            text = pytesseract.image_to_string(thresh, config='--psm 8')
            return text.strip()
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""

class HelmetDetector:
    def __init__(self, model_path=None):
        # For now, use a simple heuristic or placeholder
        # In production, train a custom model for helmet detection
        self.model = None

    def detect_helmets(self, frame, person_detections):
        """
        Detect helmets on persons (placeholder implementation)
        """
        helmets = []
        for person in person_detections:
            # Simple heuristic: check if there's a dark region on top of head
            # This is a placeholder - real implementation needs trained model
            helmets.append({'person_id': person['id'], 'helmet_detected': True})  # Assume helmet for now
        return helmets
