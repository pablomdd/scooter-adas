from cv2 import threshold
from typing import List
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
_MARGIN = 30  # pixels
_ROW_SIZE = 30  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 2
_TEXT_COLOR = (255, 0, 0) 
_RED = (0, 255, 0)
_BOX_THICKNESS = 2


class JetsonDetector():
    """ 
        Custom object detector class based on CUDA.
        Specify the path (name) of an installed OD model.
        Set `debug_mode` to add bounding boxes and FPS to the image passed into `detect()`.
    """
    def __init__(self, model_path:str, threshold:float, detection_limit:int, debug_mode=False) -> None:
        self.path = model_path
        self.threshold = threshold
        self.detection_limit = detection_limit
        self.debug_mode = debug_mode

        self.net = jetson_inference.detectNet(self.path, self.threshold)

    def detect(self, img) -> List:
        """ 
        Runs an object detection inference and returns a list of objects detected.
        """
        # TODO: Add an allow list of detections to narrow down to people and cars 
        # TODO: Create and object/class to store detections. Currently they're plain added into a list 
       
        # Convert OpenCV img into CUDA format
        imgCuda = jetson_utils.cudaFromNumpy(img)
        
        detections = self.net.Detect(imgCuda, overlay="OVERLAY_NONE")

        objects = []
        for d in detections:
            if len(objects) >= self.detection_limit:
                break

            className = self.net.GetClassDesc(d.ClassID)
            objects.append([className, d.Confidence])
            
            if self.debug_mode:
                x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)

                cv2.rectangle(img, (x1, y1), (x2, y2), _RED, _BOX_THICKNESS)

        if self.debug_mode:
            cv2.putText(img, f'FPS: {self.net.GetNetworkFPS()}', (_MARGIN,_MARGIN), cv2.FONT_HERSHEY_PLAIN,
                    _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

        return objects



def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    detector = JetsonDetector("ssd-mobilenet-v2", 0.5, 2, True)
    while(True):
        success, img = cap.read()

        objects = detector.detect(img)

        print(len(objects))
        print(objects)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()