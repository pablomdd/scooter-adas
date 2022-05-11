from email.mime import image
from re import A
import cv2 as cv
import numpy as np
from typing import Dict, List, NamedTuple
from object_detector import Rect


class DangerArea(NamedTuple):
  """Danger area coordinates."""
  bottom_left: List[float]
  top_left: List[float]
  top_right: List[float]
  bottom_right: List[float]

_RED = (0, 0, 255)
_GREEN = (0, 255, 0)
# TODO: define all danger areas
_AREA_1 = DangerArea(
        bottom_left=[960-60*3,1080],
        top_left=[960-50*3,1080-80*3],
        top_right=[960+50*3,1080-80*3],
        bottom_right=[960+60*3,1080])


# TODO paint all danger areas
def draw_scooter_line(image: np.ndarray, areas: List) -> np.ndarray:
    for area in areas:
        pts = np.array([area.bottom_left, area.top_left, area.top_right, area.bottom_right], np.int32)
        pts = pts.reshape((-1,1,2))
        cv.polylines(image,[pts],True,(0,255,255))
    return image

def find_intersections(rect:Rect, area:DangerArea):
    """Looks for rectangle bottom coordinates intersections in Danger Area.
    Args:
        rect: Rect 
        area: DangerArea.

    Returns:
        boolean 
    """
    box_bot_left = rect.left, rect.bottom
    box_bot_right = rect.right, rect.bottom
    
    # Compare rectangle bottom left 
    if box_bot_left[0] > area.bottom_left[0] and box_bot_left[0] < area.bottom_right[0]:
        if box_bot_left[1] > area.top_left[1] and box_bot_left[1] < area.bottom_left[1]:
            print("box bot left inside area")
            return True
    # Compare rectangle bottom right
    elif box_bot_right[0] > area.bottom_left[0] and box_bot_right[0] < area.bottom_right[0]:
        if box_bot_right[1] > area.top_left[1] and box_bot_right[1] < area.bottom_left[1]:
            print("box bot right inside area")
            return True
    
    print("no intersection found")
    return False


def draw_boxes(boxes:List, image):
    for box in boxes:
        start_point = box.left, box.top
        end_point = box.right, box.bottom
        cv.rectangle(image, start_point, end_point, _RED, 3)
    return image


def main():
    _IMAGE_FILE = 'line_imgs/1_93m_start.png'
    image = cv.imread(_IMAGE_FILE)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # MIDDLE LINE COORDS
    top, bot = (960, 0), (960, 1080)
    cv.line(image, top, bot, _GREEN, 3)

    # Draw danger zones in the scooter line 
    image = draw_scooter_line(image, [_AREA_1])
        
    # Test box
    rect_0 = Rect(left = 500, top = 1, right = 800, bottom = 1000)
    rect_1 = Rect(left = 1000, top = 200, right = 1200, bottom = 900)
    rect_2 = Rect(left = 600, top = 150, right = 900, bottom = 800)
    rect_3 = Rect(left = 1500, top = 400, right = 1900, bottom = 1000)
    boxes = [rect_0, rect_1, rect_2, rect_3]
    image = draw_boxes(boxes, image)

    find_intersections(rect_3, _AREA_1)

    # Resize image for fitting in the screen
    #image = cv.resize(image, (960, 540))                
    image = cv.resize(image, (1440, 810))                
    cv.imshow('scooter line', image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return

if __name__ == '__main__':
    main()


# Intersection steps
# 0. GET DANGER AREAS CORRDS. MAKE CALCS
# 1. GET INTERSECTION objects with bottom areas and go up
# 2. POST ALERTS