import cv2
import object_detector as od
import utils

_MODEL_FILE = 'efficientdet_lite0.tflite'
_IMAGE_FILE = 'test_imgs/9.png'
_ALLOW_LIST = ['person', 'car']
# _BBOX_IOU_THRESHOLD = 0.9
# _DENY_LIST = ['book']
# _SCORE_THRESHOLD = 0.3
# _MAX_RESULTS = 3

def run_prediction(image):
    option = od.ObjectDetectorOptions(label_allow_list=_ALLOW_LIST)
    detector = od.ObjectDetector(_MODEL_FILE, options=option)
    detections = detector.detect(image)

    image = utils.visualize(image, detections)
    
    cv2.imshow('object_detector', image)
    print(detections)

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
