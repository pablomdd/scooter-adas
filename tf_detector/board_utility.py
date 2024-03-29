# python3 -m pip3 install pyserial
import serial
import time

# Warning: Check serial port to correspond the board
# DEFAULT_PORT = "/dev/ttyACM0"
DEFAULT_PORT = "/dev/ttyUSB0"

DEFAULT_BAUD_RATE = 115200
DEFAULT_TIMEOUT = 0.1

class Board:
    """
    Connects to a microcontroller via a Serial interface.

    Specify the serial `port`, baud `rate` and `timeout`.

    `debug_mode` prints each step the board takes. Default to True
    
    Note that board needs about 2 seconds to start writing/reading operations properly
    """
    def __init__(self, port=DEFAULT_PORT, baud_rate=DEFAULT_BAUD_RATE, timeout=DEFAULT_TIMEOUT, debug_mode=True) -> None:
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.debug_mode = debug_mode

        try:
            self.board = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=self.timeout)
        except:
            raise Exception("Cannot initialize board communication")

    def write(self, data:str) -> None:
        if self.debug_mode:
            print("writing")
        self.board.write(bytes(data, 'utf-8'))
    
    def read(self) -> str:
        try:
            if self.debug_mode:
                print("reading")
            reading = self.board.readline().decode('utf-8')
            if reading == "":
                reading = "No reading"

        except:
            # raise Exception("Error reading board.")
            print("Error reading board.")
            return -1
        return reading

if __name__ == '__main__':
    print("initializing board")
    board = Board(debug_mode=False)

    # Note that board needs about 2 seconds to start writing/reading operations properly
    time.sleep(4)

    # for i in range(-2, 0):
    #     speed = board.read()
    #     print(speed)

    #     print("action:", i)
    #     board.write(str(i))
    #     # time.sleep(0.001)
    #     time.sleep(2)

    # for i in range(6, 2, -1):
    #     print("action:", i)
    #     speed = board.read()
    #     print(speed)

    #     board.write(str(i))
    #     # time.sleep(0.001)
    #     time.sleep(10)

    speed = board.read()
    print(speed)
    board.write(str(0))
    print("action:", 0)
    # time.sleep(0.001)
    time.sleep(5)

    # speed = board.read()
    # print(speed)


    # for i in range(10):
    #     speed = board.read()
    #     print(speed)
    #     print("action:", 4)
    #     board.write(str(4))
    #     time.sleep(2)

    board.write(str(3))
    print("action:", 3)
    # time.sleep(0.001)
    time.sleep(10)              

    speed = board.read()
    print(speed)
    board.write(str(1))
    print("action:", 1)
    # time.sleep(0.001)
    time.sleep(2)                           

    speed = board.read()
    print(speed)
    board.write(str(0))
    print("action:", 0)
    # time.sleep(0.001)
    time.sleep(2)

    