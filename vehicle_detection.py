import cv2
import numpy as np
import os

net = cv2.dnn.readNet("yolov7.weights", "yolov7.cfg")

classes = []
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

image_dir = "test_images/"
output_dir = "output_images/"

os.makedirs(output_dir, exist_ok=True)

for i in range(1, 5):
    image_path = image_dir + str(i) + ".jpg"
    image = cv2.imread(image_path)

    height, width, _ = image.shape

    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    output_layers = net.getUnconnectedOutLayersNames()

    detections = net.forward(output_layers)

    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.5:
                label = classes[class_id]
                if label == 'car' or label == 'bus' or label == 'truck':
                    center_x = int(obj[0] * width)
                    center_y = int(obj[1] * height)
                    w = int(obj[2] * width)
                    h = int(obj[3] * height)
                    
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

    cv2.imshow("Vehicle Detection", image)
    cv2.waitKey(0)

    output_path = output_dir + "output_" + str(i) + ".jpg"
    cv2.imwrite(output_path, image)

cv2.destroyAllWindows()
