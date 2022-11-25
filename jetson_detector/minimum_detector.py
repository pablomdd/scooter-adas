from cv2 import threshold
import jetson_inference
import jetson_utils
import cv2

net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while(True):
    success, img = cap.read()

    # Convert img into CUDA format
    imgCuda = jetson_utils.cudaFromNumpy(img)
    
    detections = net.Detect(imgCuda)

    img = jetson_utils.CudaToNumpy(imgCuda)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
