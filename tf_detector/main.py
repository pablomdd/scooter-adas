from re import L
import cv2
import object_detector as od
# from line_drawer import find_intersections
import line_drawer
import decision_making
import utils

_MODEL_FILE = 'efficientdet_lite0.tflite'
_IMAGE_FILE = 'test_imgs/1.png'
_ALLOW_LIST = ['person', 'car']
# _BBOX_IOU_THRESHOLD = 0.9
# _DENY_LIST = ['book']
# _SCORE_THRESHOLD = 0.3
# _MAX_RESULTS = 3

def get_bounding_boxes(detections):
    """ Gets an array of Rect (NamedTuple) of the bouding boxes.
    Args:
        detections: The list of all "Detection" entities from the Object Detector.

    Returns:
        Array of bounding boxes. These are object_detector Rect classes:

        class Rect(NamedTuple):
            # A rectangle in 2D space
            left: float
            top: float
            right: float
            bottom: float
    """
    return [detection.bounding_box for detection in detections]

def run_prediction(image):
    option = od.ObjectDetectorOptions(label_allow_list=_ALLOW_LIST)
    detector = od.ObjectDetector(_MODEL_FILE, options=option)
    detections = detector.detect(image)

    # Get image and boxes from drawing boxes utility
    image, boxes = utils.visualize(image, detections)
    print(boxes)
    image = line_drawer.draw_scooter_line(image)

    # Detect obstacle on Danger Areas
    obstacle, danger_area = False, 0
    for idx, box in enumerate(boxes):
        obstacle, danger_area = line_drawer.find_intersections(rect=box, box_idx=idx)
        if obstacle:
            break
    
    # Get alert based on obstacles
    speed = 20
    action = decision_making.make(danger_area, speed)
    print(action)

    # TODO: Emit alert


    image = cv2.resize(image, (1440, 810))                
    cv2.imshow('object_detector', image)
    
    # Get boxes locally from detections raw list
    # print(get_bounding_boxes(detections))
    
    while True:
        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('object_detector', image)

    cv2.destroyAllWindows()
    

def main():
    image = cv2.imread(_IMAGE_FILE)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    run_prediction(image)
    
    return

if __name__ == '__main__':
    main()
