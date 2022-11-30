import sys
import cv2
import line_drawer
import decision_making
# import utils
from jetson_od import JetsonDetector

_MODEL_FILE = 'efficientdet_lite0.tflite'
# _IMAGE_FILE = 'test_imgs/1.png'
_IMAGE_FILE = 'test_imgs/2.png'
# _IMAGE_FILE = 'line_imgs/11m.png'

_ALLOW_LIST = ['person', 'car']
# _BBOX_IOU_THRESHOLD = 0.9
# _DENY_LIST = ['book']
# _SCORE_THRESHOLD = 0.3
_MAX_RESULTS = 10


class Orchestrator():
    def __init__(self, model_path, threshold, detection_limit, allow_list, debug_mode) -> None:
        try:
            self.detector = JetsonDetector(model_path, threshold, detection_limit, allow_list, debug_mode)
        except:
            raise("Could not initialize Jetson Detector")
        self.debug_mode = debug_mode


    def get_prediction(self, image, speed=0):
        """Receives and image and speed from outside and returns a preventive action.
        
        The proccess is as following:

            1. Runs Object Detector to recognize labels in Allow List.
        
            2. Detections go through findintersections() and it determines if any of them 
            it is an actual obstacle that is on the scoorter\'s line.
        
            3. If there is an obtacle, run decisionmaking.make() to emit determine preventive
            action based on the location of the obstacle and scooter's speed.
        
            4. Finally, the action, if any, is returned.

        Args:
            image: in OpenCV BGR format.
            speed: in Km/h.

        Returns:
            action (str): preventive action if an obtacle was detected. Empty string if not ("").
        """
        # STEP 1. Run object detector.
        # If debug mode is set in Detector, it will paint the detection bounding boxes
        detections, boxes = self.detector.detect(image)

        if self.debug_mode:
            image = line_drawer.draw_scooter_line(image)

        # STEP 2. Detect obstacles on Danger Areas.
        obstacle, danger_area = False, 0
        for idx, box in enumerate(boxes):
            obstacle, danger_area = line_drawer.find_intersections(rect=box, box_idx=idx)
            if obstacle:
                break
        
        # STEP 3. Get action based on obstacles
        action = "None"
        if obstacle:
            action = decision_making.make(danger_area, speed)

        return action


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    allow_list = ['person', 'car', 'truck', 'motorcycle', 'bicycle']
    orchestrator = Orchestrator("ssd-mobilenet-v2", 0.5, 12, allow_list, True)
    while(True):
        success, img = cap.read()

        action = orchestrator.get_prediction(img, 0.0)

        print(action)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    main()