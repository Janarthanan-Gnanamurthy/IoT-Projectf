import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained SSD MobileNet V2 model
model = tf.saved_model.load('./efficientdet_d0_coco17_tpu-32/saved_model')

# Function to perform person detection on a frame


def detect_person(frame):
    # Convert the frame to a format suitable for TensorFlow
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_tensor = tf.convert_to_tensor(frame_rgb)
    frame_tensor = tf.expand_dims(frame_tensor, 0)

    # Run inference
    detections = model(frame_tensor)

    # Filter out detections with a confidence threshold
    threshold = 0.5
    boxes = detections['detection_boxes'][0].numpy()
    scores = detections['detection_scores'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int64)
    num_detections = detections['num_detections'][0]

    # Draw bounding boxes around detected persons
    for i in range(int(num_detections)):
        if scores[i] > threshold and classes[i] == 1:  # 1 corresponds to 'person' class
            h, w, _ = frame.shape
            box = boxes[i] * np.array([h, w, h, w])
            box = box.astype(np.int32)
            cv2.rectangle(frame, (box[1], box[0]),
                          (box[3], box[2]), (0, 255, 0), 2)

    return frame

# Function to process the webcam stream


def process_webcam_stream():
    # 0 for default webcam, change accordingly if you have multiple cameras
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform person detection on the frame
        result_frame = detect_person(frame)

        # Display the result
        cv2.imshow('Person Detection', result_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


# Start processing the webcam stream
process_webcam_stream()
