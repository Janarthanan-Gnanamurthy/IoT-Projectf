# person_detection.py
import cv2
import numpy as np
import tensorflow as tf

# Enable GPU growth to avoid memory issues
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# Load the pre-trained model
model = tf.saved_model.load('./efficientdet_d0_coco17_tpu-32/saved_model')


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
    num_detections = int(detections['num_detections'][0])

    person_count = 0
    for i in range(num_detections):
        if scores[i] > threshold and classes[i] == 1:  # 1 corresponds to 'person' class
            person_count += 1

            # Get bounding box coordinates
            box = boxes[i]
            (startY, startX, endY, endX) = box

            # Convert normalized coordinates to pixel values
            (h, w) = frame.shape[:2]
            startX = int(startX * w)
            startY = int(startY * h)
            endX = int(endX * w)
            endY = int(endY * h)

            # Draw bounding box
            cv2.rectangle(frame, (startX, startY),
                          (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, f'Person: {scores[i]:.2f}', (
                startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return person_count, frame
