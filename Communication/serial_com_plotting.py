import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Path3DCollection

if __name__ == '__main__':

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    xs, ys, zs = [], [], []
    plt.draw()

    tagScatter = ax.scatter([1], [1], [1])
    poseScatter = ax.scatter([1], [1], [1])

    tagScatter: Path3DCollection
    poseScatter: Path3DCollection

    print(tagScatter.get_array())

    plt.show(block=False)


    def update_line(hl, new_data):
        hl.set_xdata(np.array(new_data))
        hl.set_ydata(np.array(new_data))
        hl.set_ydata(np.array(new_data))
        plt.draw()


    plt.show()

    while True:
        update_line(tagScatter, [1])
        pass

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

                        xs.append(np.random.rand(1) * 10)
                        ys.append(np.random.rand(1) * 10)
                        zs.append(np.random.rand(1) * 10)
                        sc.set_offsets(np.c_[xs, ys, zs])
                        fig.canvas.draw_idle()
                        plt.pause(0.1)

                        print(new_pose)

                        previous_position = new_pose

                    lines.append(line)
                    line = ''
