import numpy as np
import serial
from serial import Serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

from PositionCalcualtionNonLinear import calculate_pos

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

        tags = set()
        poses = []
        powers = []

        previous_position = np.array([0, 0, 0])

        while True:
            data = ser.read(10000).decode('utf-8')

            if data != '':
                line += data

                if '\n' in data:
                    line = line.strip()
                    print(line)

                    tag_id, seq, x, y, z, power = map(float, line.split(","))

                    tags.add(tag_id)
                    poses.append((x, y, z))
                    powers.append(power)

                    if len(tag_id) >= 3 and len(poses) >= 5:
                        new_pose, a = calculate_pos(previous_position, poses, powers)
                        poses.clear()
                        powers.clear()
                        tags.clear()

                        print(new_pose)

                        previous_position = new_pose

                    lines.append(line)
                    line = ''
