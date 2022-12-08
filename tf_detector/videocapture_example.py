import time
import numpy as np
import cv2 
from line_drawer import draw_scooter_line
from datetime import datetime

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 1
fps_avg_frame_count = 10

# Variables to calculate FPS
counter, fps = 0, 0
start_time = time.time()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 360)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_out = cv2.VideoWriter(str(datetime.now()) + '.avi', fourcc, 20.0, (640, 360))
if not cap.isOpened():
    print("Cannot find camera")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    frame = cv2.flip(frame, 1)
    video_out.write(frame)

    # Calculate the FPS
    if counter % fps_avg_frame_count == 0:
        end_time = time.time()
        fps = fps_avg_frame_count / (end_time - start_time)
        start_time = time.time()
    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)  

    cv2.putText(frame, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)
    frame = draw_scooter_line(frame)

    cv2.imshow('video capture', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
