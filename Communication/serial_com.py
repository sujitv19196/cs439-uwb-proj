import serial
from serial import Serial

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
        ser: Serial

        lines = []

        line = ''

        while True:
            data = ser.read(10000).decode('utf-8')

            if data != '':
                line += data

                if '\n' in data:
                    line = line.strip()
                    print(line)
                    lines.append(line)
                    line = ''
