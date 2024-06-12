import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
# you can use 'yolov8s.pt', 'yolov8m.pt', etc. for different model sizes
model = YOLO('yolov8n.pt')

# Function to perform person detection


def detect_person(frame):
    # Perform inference
    results = model(frame)

    person_count = 0

    # Process results
    for result in results:
        for box in result.boxes:
            cls = int(box.cls)  # Ensure the class is an integer
            if cls == 0:  # class 0 is 'person' in COCO dataset
                person_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                confidence = box.conf.item()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'Person {confidence:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    return person_count, frame
