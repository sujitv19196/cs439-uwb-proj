import matplotlib.pyplot as plt
import numpy as np
import serial
from serial import Serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

from PositionCalcualtionNonLinear import calculate_pos

NORMALIZER = -94.04254097

hl, = plt.plot([], [])

plt.scatter(
    [0, 3, 2, 0], [0, 0, 2, 1.2]
)

scale = 10


def update_plot(new_x, new_y):
    hl.set_xdata(np.append(hl.get_xdata(), new_x))
    hl.set_ydata(np.append(hl.get_ydata(), new_y))
    plt.draw()
    plt.pause(.1)


if __name__ == '__main__':
    plt.show(block=False)

    print("heloo")
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

        previous_position = np.array([10, 10])

        dataP = []

        estimates = []

        i = 0

        while True:
            data = ser.readline()

            if data != '':
                line += data.decode('utf-8')

                if b'\n' in data:

                    line = line.strip()

                    if line.startswith("Reception"):
                        line = ''
                        continue

                    tag_id, seq, x, y, z, power = map(float, line.split(","))

                    tags.add(tag_id)
                    poses.append((x, y, z))
                    powers.append(power * scale)

                    dataP.append(power)

                    if len(tags) >= 3:
                        P = poses
                        D = powers

                        print(x,y)

                        new_pose = calculate_pos(previous_position, P, D)
                        # poses.clear()
                        # powers.clear()
                        tags.clear()

                        print(new_pose)

                        estimates.append(new_pose)

                        update_plot(new_pose[0] / scale, new_pose[1] / scale)

                        previous_position = new_pose

                    lines.append(line)
                    line = ''

                    # if len(extra) > 1:
                    #     line += extra[1]
        plt.plot(dataP)
        plt.show()
