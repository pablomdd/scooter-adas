import sys
import argparse
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-img", "--Image", help = "Image path to run detection")
parser.add_argument("-s", "--Speed", help = "Scooter speed in Km/h")
 

import cv2
import object_detector as od
# from line_drawer import find_intersections
import line_drawer
import decision_making
import utils

_MODEL_FILE = 'efficientdet_lite0.tflite'
# _IMAGE_FILE = 'test_imgs/1.png'
_IMAGE_FILE = 'test_imgs/1.png'
# _IMAGE_FILE = 'line_imgs/11m.png'

_ALLOW_LIST = ['person', 'car']
# _BBOX_IOU_THRESHOLD = 0.9
# _DENY_LIST = ['book']
# _SCORE_THRESHOLD = 0.3
_MAX_RESULTS = 10

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

def run_prediction(image, speed=0):
    """Receives and image and speed from outside and returns a preventive action.
    
    The proccess is as following:

        1. Runs TensorFlow EfficientDet to recognize people and cars.
    
        2. Detections go through findintersections() and it determines if any of them 
        it is an actual obstacle that is on the scoorter\'s line.
    
        3. If there is an obtacle, run decisionmaking.make() to emit determine preventive
        action based on the location of the obstacle and scooter's speed.
    
        4. Finally, the action, if any, is returned.

    Args:
        image: in RGB format.
        speed: in Km/h.

    Return:
        image: with scooter\'s line and detections.
        action (str): preventive action if an obtacle was detected. Empty string if not ("").
    """
    
    # STEP 1. Run object detector.
    option = od.ObjectDetectorOptions(label_allow_list=_ALLOW_LIST, max_results=_MAX_RESULTS)
    detector = od.ObjectDetector(_MODEL_FILE, options=option)
    detections = detector.detect(image)
        # Get boxes locally from detections raw list
        # print(get_bounding_boxes(detections))

    # Get image and boxes from drawing boxes utility
    image, boxes = utils.visualize(image, detections)
    print(boxes)
    image = line_drawer.draw_scooter_line(image)

    # STEP 2. Detect obstacles on Danger Areas.
    obstacle, danger_area = False, 0
    for idx, box in enumerate(boxes):
        obstacle, danger_area = line_drawer.find_intersections(rect=box, box_idx=idx)
        if obstacle:
            break
    
    # STEP 3. Get action based on obstacles
    action = ""
    if obstacle:
        action = decision_making.make(danger_area, speed)
    print(action)

    # Print image on screen. Not necessary when in production mode.
    # Resize to fit in device screen. Does not affect detection.
    image = cv2.resize(image, (1440, 810))                
    cv2.imshow('object_detector', image)
    
    while True:
        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('object_detector', image)
    cv2.destroyAllWindows()

    # STEP 3. Emit action.
    return image, action
    

def main():
    args = parser.parse_args()
    img_route = ""
    speed = 0.0
    
    if args.Image:
        img_route = args.Image

    if args.Speed:
        speed = float(args.Speed)

    # if(len(sys.argv) > 1):
    #     img_route = sys.argv[1]
    #     print(str(img_route))
    
    print(str(img_route))
    print(speed)

    if (img_route):
        image = cv2.imread(img_route)
    else: 
        image = cv2.imread(_IMAGE_FILE)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    _, action = run_prediction(image, speed)
    print(action)
    return action

if __name__ == '__main__':
    main()
