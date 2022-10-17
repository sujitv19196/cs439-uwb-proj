import serial

from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

if __name__ == '__main__':
    com_port = None

    for i in list_ports.grep("", False):
        i: ListPortInfo

        if i.description.startswith("JLink"):
            com_port = i.name
    print("Printing from port", com_port)

    with serial.Serial(com_port, baudrate=115200, timeout=0) as ser:
        s = ser.read(100)  # read up to one hundred bytes

        print(s)
        # or as much is in the buffer
