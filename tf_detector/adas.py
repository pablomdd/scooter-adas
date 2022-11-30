import argparse
import time
import cv2
# from main import run_prediction
from board_utility import Board
from orchestrator import Orchestrator

_DEFAULT_DEBUG_MODE = False
_DEFAULT_PORT = "/dev/ttyUSB0"

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-img", "--Image", help = "Image path to run detection")
parser.add_argument("-s", "--Speed", help = "Scooter speed in Km/h")
parser.add_argument("-dev", "--Development", help = "Set debug mode true o false")

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 2
fps_avg_frame_count = 10


def main():
    args = parser.parse_args()

    debug_mode = _DEFAULT_DEBUG_MODE
    if args.Development:
        print("entering dev flag conditional")
        if args.Development == "False" or args.Development == "false":
            debug_mode = False
        else:
            debug_mode = True

    print("*********************************************************")
    print("Debug mode set to ", debug_mode)
    print("*********************************************************")

    if args.Image:
        img_route = args.Image

    if args.Speed:
        speed = float(args.Speed)

    try:
        board = Board(port=_DEFAULT_PORT, debug_mode=debug_mode)
        # Needed to start communication correctly
        time.sleep(4)
    except:
        print("Cannot initialize board")

    speed = 0.0
    lastSpeed = 0.0

    # if (img_route):
    #     image = cv2.imread(img_route)
    # else: 
    #     image = cv2.imread(_IMAGE_FILE)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # action, img_processed = run_prediction(image, speed)

    # Variables to calculate FPS
    counter, fps = 0, 0
    read_start_time = time.time()
    write_start_time = time.time()

    try:
        cap = cv2.VideoCapture(0)   
    except:
        print("Cannot initialize video capture")

    cap.set(3, 640)
    cap.set(4, 360)

    allow_list = ['person', 'car', 'truck', 'motorcycle', 'bicycle']
    orchestrator = Orchestrator("ssd-mobilenet-v2", 0.5, 12, allow_list, debug_mode)

    while cap.isOpened():
        # TODO: Add sample time to run read speed from board

        if time.time() - read_start_time > 1:
            boardReading = board.read()
            read_start_time = time.time()

        if boardReading == "No reading":
            speed = lastSpeed
        else:
            speed = float(boardReading)
            lastSpeed = speed

        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break

        # TODO: Make resize pair-values into a array/dict of tupples
        # frame = cv2.resize(frame, (480, 270))  
        # frame = cv2.resize(frame, (480*2, 270*2))                              

        # if debug_mode:
            # [DEBUG]: Flipping for natual mirrror looking
            # frame = cv2.flip(frame, 1)
            # # [DEBUG]:  Calculate the FPS
            # if counter % fps_avg_frame_count == 0:
            #     end_time = time.time()
            #     fps = fps_avg_frame_count / (end_time - start_time)
            #     start_time = time.time()

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        action, image = orchestrator.get_prediction(frame, speed)
        print("Action:", action)

        # TODO: Add sample time to run write action to board
        if time.time() - write_start_time > 1:
            if action == "None":
                action = 0
            board.write(str(action))
            write_start_time = time.time()

        if debug_mode:
            # [DEBUG]:  Show the FPS
            # fps_text = 'FPS = {:.1f}'.format(fps) + " ACTION: " + action
            text_location = (left_margin, row_size)  
            # cv2.putText(frame, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
            #             font_size, text_color, font_thickness)

            action_text = "Speed " + str(speed) + " | ACTION: " + str(action)

            cv2.putText(image, action_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        font_size, text_color, font_thickness)

            # [DEBUG]: Show video
            cv2.imshow('video capture', image)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
