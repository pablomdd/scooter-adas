import cv2 as cv
import numpy as np
from typing import List, NamedTuple
from jetson_od import Rect


class DangerArea(NamedTuple):
  """Danger area coordinates."""
  bottom_left: List[float]
  top_left: List[float]
  top_right: List[float]
  bottom_right: List[float]

# Global util constants
_RED = (0, 0, 255)
_YELLOW = (0,255,255)
_GREEN = (0, 255, 0)
_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 2

"""Danger Areas definition
AREA_1 is the closest to the scooter, thus, the most dangerous if an object detected.

- AREA_1 [0 or 2-3] meters: Goes from the bottom, the first part of the bottom image that the camera can see.
    For the testing camera it is 1.93m~=2m up to 3m. 
    Our scooter prroved it can brake from 15km/h to 0 in around 3m. 
- AREA_2 (3-5] meters 
- AREA_3 (5-9] meters 
"""

ratio = 3
X1 = 110
X2 = 70
Y2 = 280

_AREA_1 = DangerArea(
        bottom_left=[(960-X1)/ratio,1080/ratio],
        top_left=[(960-X2)/ratio,(1080-Y2)/ratio],
        top_right=[(960+X2)/ratio,(1080-Y2)/ratio],
        bottom_right=[(960+X1)/ratio,1080/ratio])

X3 = 960-40
Y3 = 410

_AREA_2 = DangerArea(
        bottom_left=[(960-X2)/ratio,(1080-Y2)/ratio],
        top_left=[(X3)/ratio,(1080-Y3)/ratio],
        top_right=[((960+(960-X3))/ratio),(1080-Y3)/ratio],
        bottom_right=[(960+X2)/ratio,(1080-Y2)/ratio])

X4 = 960-25
Y4 = 600

_AREA_3 = DangerArea(
        bottom_left=[X3/ratio,(1080-Y3)/ratio],
        top_left=[X4/ratio,Y4/ratio],
        top_right=[(960+(960-X4))/ratio,Y4/ratio],
        bottom_right=[(960+(960-X3))/ratio,(1080-Y3)/ratio])



_AREA_COLORS = {
    1: _GREEN,
    2: _YELLOW,
    3: _RED
}

_DANGER_AREAS = [_AREA_1, _AREA_2, _AREA_3]

def draw_scooter_line(image: np.ndarray, areas: List=_DANGER_AREAS) -> np.ndarray:
    for idx, area in enumerate(areas):
        pts = np.array([area.bottom_left, area.top_left, area.top_right, area.bottom_right], np.int32)
        pts = pts.reshape((-1,1,2))
        cv.polylines(image,[pts],True, _AREA_COLORS[idx+1], 3)
    return image

def find_intersections(rect:Rect, areas:List[DangerArea]=_DANGER_AREAS, box_idx=-1):
    """Looks for rectangle bottom coordinates intersections in the closest Danger Area for one box.
    
    The closest Danger Area is 1, then 2, and 3. 
    
    When a intersection is identified, the function returns and does not goes to the rest of the areas.
    
    Args:
        rect: Rect. 
        area: List[DangerArea].
        box_idx: optional argument for debugging.

    Returns:
        result: boolean - if an intersection is detected.
        area: int - number of the area (1-3) in which object was detected. Zero (0) if none object.
    """
    box_bot_left = rect.left, rect.bottom
    box_bot_right = rect.right, rect.bottom

    for i, area in enumerate(areas):    
        # Compare rectangle bottom left 
        if box_bot_left[0] > area.bottom_left[0] and box_bot_left[0] < area.bottom_right[0]:
            if box_bot_left[1] > area.top_left[1] and box_bot_left[1] < area.bottom_left[1]:
                print("box", box_idx, "bot left inside area", i + 1)
                return True, i+1
        # Compare rectangle bottom right
        elif box_bot_right[0] > area.bottom_left[0] and box_bot_right[0] < area.bottom_right[0]:
            if box_bot_right[1] > area.top_left[1] and box_bot_right[1] < area.bottom_left[1]:
                print("box", box_idx, "bot right inside area", i + 1)
                return True, i+1
        
    print("no intersection found")
    return False, 0


def draw_boxes(boxes:List, image):

    for idx, box in enumerate(boxes):
        start_point = box.left, box.top
        end_point = box.right, box.bottom
        result_text = "Box " + str(idx)
        text_location = (_MARGIN + box.left,
                        _MARGIN + _ROW_SIZE + box.top)
        cv.putText(image, result_text, text_location, cv.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _RED, _FONT_THICKNESS)
        cv.rectangle(image, start_point, end_point, _RED, 3)
    return image


def main():
    _IMAGE_FILE = 'line_imgs/cam_logi_line.jpg'
    image = cv.imread(_IMAGE_FILE)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # MIDDLE LINE COORDS
    top, bot = (960, 0), (960, 1080)
    cv.line(image, top, bot, _GREEN, 3)

    # Draw danger zones in the scooter line 
    image = draw_scooter_line(image, _DANGER_AREAS)

    # Test box
    rect_0 = Rect(left = 500, top = 1, right = 800, bottom = 1000)
    rect_1 = Rect(left = 1000, top = 200, right = 1200, bottom = 900)
    rect_2 = Rect(left = 600, top = 150, right = 900, bottom = 800)
    rect_3 = Rect(left = 1500, top = 400, right = 1900, bottom = 1000)
    boxes = [rect_0, rect_1, rect_2, rect_3]
    image = draw_boxes(boxes, image)

    for idx, box in enumerate(boxes):
        find_intersections(box, _DANGER_AREAS, idx)

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
# ~ 0. GET DANGER AREAS CORRDS. MAKE CALCS~
# ~ 1. GET INTERSECTION objects with bottom areas and go up~
# 2. POST ALERTS