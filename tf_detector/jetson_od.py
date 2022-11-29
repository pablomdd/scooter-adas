from cv2 import threshold
from typing import List, NamedTuple
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


class Rect(NamedTuple):
  """A rectangle in 2D space."""
  left: float
  top: float
  right: float
  bottom: float


class Category(NamedTuple):
  """A result of a classification task."""
  label: str
  score: float
  index: int


class Detection(NamedTuple):
  """A detected object as the result of an ObjectDetector."""
  bounding_box: Rect
  categories: List[Category]


class JetsonDetector():
    """ 
        Custom object detector class based on CUDA.
        Specify the path (name) of an installed OD model.
        Set `debug_mode` to add bounding boxes and FPS to the image passed into `detect()`.
    """
    def __init__(self,
            model_path:str,
            threshold:float,
            detection_limit:int,
            allow_list=[],
            debug_mode=False) -> None:
        self.path = model_path
        self.threshold = threshold
        self.detection_limit = detection_limit
        self.allow_list = set(allow_list)
        self.debug_mode = debug_mode

        self.net = jetson_inference.detectNet(self.path, self.threshold)

    def detect(self, img) -> List:
        """ 
        Runs an object detection inference and returns a list of objects detected.
        """
        # Convert OpenCV img into CUDA format
        imgCuda = jetson_utils.cudaFromNumpy(img)
        
        detections = self.net.Detect(imgCuda, overlay="OVERLAY_NONE")

        objects = []
        for d in detections:
            if len(objects) >= self.detection_limit:
                break

            class_name = self.net.GetClassDesc(d.ClassID)

            if(self.allow_list):
                if not class_name in self.allow_list:
                    break

            category = Category(label=class_name, score=d.Confidence, index=d.ClassID)
            x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
            bounding_box = Rect(x1, y1, x2, y2)
            objects.append([Detection(bounding_box=bounding_box, categories=[category])])
            
            if self.debug_mode:
                cv2.rectangle(img, (x1, y1), (x2, y2), _RED, _BOX_THICKNESS)

        if self.debug_mode:
            cv2.putText(img, f'FPS: {self.net.GetNetworkFPS()}', (_MARGIN,_MARGIN), cv2.FONT_HERSHEY_PLAIN,
                    _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

        return objects



def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    allow_list = ['person', 'car', 'truck', 'motorcycle', 'bicycle']
    detector = JetsonDetector("ssd-mobilenet-v2", 0.5, 12, allow_list, True)
    while(True):
        success, img = cap.read()

        objects = detector.detect(img)

        print(len(objects))
        print(objects)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    main()