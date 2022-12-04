import argparse
import time
import cv2
# from main import run_prediction
from board_utility import Board
from orchestrator import Orchestrator

_DEFAULT_DEBUG_MODE = False
_DEFAULT_PORT = "/dev/ttyUSB0"
_READ_SAMPLE_TIME_SECONDS = 1
_WRITE_SAMPLE_TIME_SECONDS = 1

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
        print("Starting board communication...")
        board = Board(port=_DEFAULT_PORT, debug_mode=debug_mode)
        # Needed to start communication correctly
        time.sleep(4)
    except Exception as e:
        raise(e)

    speed = 0.0
    lastSpeed = 0.0
    read_start_time = time.time()
    write_start_time = time.time()

    try:
        print("Starting camera...")
        cap = cv2.VideoCapture(0)   
        # TODO: Make resize pair-values into a array/dict of tupples
        cap.set(3, 640)
        cap.set(4, 360)
    except:
        print("Cannot initialize video capture")

    # TODO: Abstract orchestrator setup options into class
    print("Starting Inferience Orchestrator...")
    allow_list = ['person', 'car', 'truck', 'motorcycle', 'bicycle']
    orchestrator = Orchestrator("ssd-mobilenet-v2", 0.5, 12, allow_list, debug_mode)

    print("Set up ready. Starting main process...")
    while cap.isOpened():
        # Step 1: Read speed from board.
        if time.time() - read_start_time > _READ_SAMPLE_TIME_SECONDS:
            boardReading = board.read()
            read_start_time = time.time()

        if boardReading == "No reading":
            speed = lastSpeed
        else:
            speed = float(boardReading)
            lastSpeed = speed

        # Step 2 Read imager from camera.
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break

        # Step 3: Run prediction and get preventive action. 
        action, image = orchestrator.get_prediction(frame, speed)
        print("Action:", action)

        # Step 4: Send preventive action to board.
        if time.time() - write_start_time > _WRITE_SAMPLE_TIME_SECONDS:
            board.write(str(action))
            write_start_time = time.time()

        if debug_mode:
            text_location = (left_margin, row_size)  
            action_text = "Speed " + str(speed) + " | ACTION: " + str(action)

            cv2.putText(image, action_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        font_size, text_color, font_thickness)
            cv2.imshow('video capture', image)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
