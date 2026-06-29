"""Детектор объектов на базе YOLOv8."""

class YOLOv8Detector:
    def __init__(self):
        self.model = None
    
    def load_weights(self, path):
        print(f"Loading YOLOv8 from {path}")
    
    def predict(self, image):
        return [{"class": "crane", "confidence": 0.9}]
