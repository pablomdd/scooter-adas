# python3 -m pip3 install pyserial
import serial
import time

# Warning: Check serial port to correspond the board
DEFAULT_PORT = "/dev/ttyACM0"
# DEFAULT_PORT = "/dev/ttyUSB0"

DEFAULT_BAUD_RATE = 115200
DEFAULT_TIMEOUT = 0.1

class Board:
    """
    Connects to a microcontroller via a Serial interface.

    Specify the serial `port`, baud `rate` and `timeout`.

    `debug_mode` prints each step the board takes. Default to True
    
    Note that board needs about 2 seconds to start writing/reading operations properly
    
    `DEFAULT_BAUD_RATE = 115200`
    `DEFAULT_TIMEOUT = 0.1`
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
    board = Board()

    # Note that board needs about 2 seconds to start writing/reading operations properly
    time.sleep(2)

    for i in range(-2, 8):
        board.write(str(i))
        time.sleep(0.001)
        action = board.read()
        print(action)
        time.sleep(0.1)

    