from cv2 import threshold
import jetson_inference
import jetson_utils
import cv2

"""
Detection class output 
<detectNet.Detection object>
   -- ClassID: 1
   -- Confidence: 0.503906
   -- Left:    383.125
   -- Top:     146.25
   -- Right:   397.5
   -- Bottom:  207.188
   -- Width:   14.375
   -- Height:  60.9375
   -- Area:    875.977
   -- Center:  (390.312, 176.719)
"""
_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 2
_TEXT_COLOR = (255, 0, 0) 


net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while(True):
    success, img = cap.read()

    # Convert img into CUDA format
    imgCuda = jetson_utils.cudaFromNumpy(img)
    
    detections = net.Detect(imgCuda)

    for d in detections:
        # print(d)
        x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)

    img = jetson_utils.cudaToNumpy(imgCuda)
    cv2.putText(img, f'FPS: {net.GetNetworkFPS()}', (30,30), cv2.FONT_HERSHEY_PLAIN,
            _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
