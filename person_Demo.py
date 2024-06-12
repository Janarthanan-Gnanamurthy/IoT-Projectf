import cv2
from ultralytics import YOLO

# Load the YOLOv8 model with segmentation capability
model = YOLO('yolov8n-seg.pt')

# Function to perform person detection with segmentation


def detect_person(frame):
    # Perform inference
    results = model(frame)

    # Process results
    for result in results:
        # Draw segmentation masks
        if hasattr(result, 'masks'):
            masks = result.masks.xy  # Get the masks
            for mask in masks:
                frame = cv2.polylines(
                    frame, [mask.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Draw bounding boxes and labels
        for box in result.boxes:
            cls = int(box.cls)  # Ensure the class is an integer
            if cls == 0:  # class 0 is 'person' in COCO dataset
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                confidence = box.conf.item()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'Person {confidence:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    return frame


# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect persons in the frame
    frame = detect_person(frame)

    # Display the resulting frame
    cv2.imshow('Person Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
