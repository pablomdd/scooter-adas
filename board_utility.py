# python3 -m pip3 install pyserial
import serial
import time

# Warning: Check serial port to correspond the board
DEFAULT_PORT = "/dev/ttyACM0"
# DEFAULT_PORT = "/dev/ttyUSB0"

DEFAULT_BAUD_RATE = 115200

class Board:
    def __init__(self, port=DEFAULT_PORT, baud_rate=DEFAULT_BAUD_RATE) -> None:
        self.port = port
        self.baud_rate = baud_rate

        try:
            self.board = serial.Serial(port=self.port, baudrate=self.baud_rate)
        except:
            raise Exception("Cannot initialize board communication")

    def write(self, data:str) -> None:
        self.board.write(bytes(data, 'utf-8'))
    
    def read(self) -> str:
        return self.board.readline().decode('utf-8')

if __name__ == '__main__':
    board = Board()
    time.sleep(1)
    board.write("1")
    print(board.read())

    time.sleep(1)
    board.write("3")
    print(board.read())

    