from email.mime import image
from re import A
import cv2 as cv
import numpy as np
from typing import Dict, List, NamedTuple

class DangerArea(NamedTuple):
  """Danger area coordinates."""
  bottom_left: List[float]
  top_left: List[float]
  top_right: List[float]
  bottom_right: List[float]


_RED = (0, 0, 255)


class LineDrawer():

    def draw_line(self, input_image: np.ndarray) -> np.ndarray:
        
        image = input_image
        
        return image


def main():
    _IMAGE_FILE = 'line_imgs/1_93m_start.png'
    image = cv.imread(_IMAGE_FILE)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # img = np.zeros((100, 500, 3), np.uint8)
    GREEN = (0, 255, 0)
    p0, p1 = (100, 30), (400, 90)
    def mouse(event, x, y, flags, param):
        if flags == 1:
            p1 = x, y
            cv.displayOverlay('window', f'p1=({x}, {y})')
            img[:] = 0
            cv.line(img, p0, p1, GREEN, 10)
            cv.imshow('window', img)
    
    img = np.zeros((100, 500, 3), np.uint8)
    cv.line(img, p0, p1, GREEN, 10)

    cv.imshow('window', img)
    cv.setMouseCallback('window', mouse)

    # MIDDLE LINE COORDS
    top, bot = (960, 0), (960, 1080)

    cv.line(image, top, bot, GREEN, 3)

    # Draw area 1
    _AREA_1 = DangerArea(
            bottom_left=[960-60*3,1080],
            top_left=[960-50*3,1080-80*3],
            top_right=[960+50*3,1080-80*3],
            bottom_right=[960+60*3,1080])

    pts = np.array([_AREA_1.bottom_left, _AREA_1.top_left, _AREA_1.top_right, _AREA_1.bottom_right], np.int32)
    pts = pts.reshape((-1,1,2))
    cv.polylines(image,[pts],True,(0,255,255))
        
    # Test box
    rect = [(500, 1), (800, 1000)]
    cv.rectangle(image, rect[0], rect[1], _RED , 3)

    # Resize image for fitting in the screen
    #image = cv.resize(image, (960, 540))                
    # image = cv.resize(image, (1440, 810))                
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