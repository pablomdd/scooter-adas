import numpy as np
import cv2 

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot find camera")
    exit()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Cannot receive frame")
        break
    frame = cv2.flip(frame, 1)
    cv2.imshow('video capture', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
