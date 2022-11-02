import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # np.random.seed(42)

    aErrors = []
    dErrors = []

    scale = 10

    for i in range(1, 10):
        points = np.random.random((i, 2)) * scale

        actual = np.random.random((1, 2)) * scale / 1.5
        aActual = np.random.rand() * 10

        distances = np.linalg.norm(points - actual, 2, axis=1) / aActual

        ABi = 2 * (points[1:] - points[:1])

        Ci = distances[1:] - distances[:1]
        Ci = Ci.reshape(-1, 1)

        Q = np.concatenate((ABi, Ci), axis=1)

        Di = np.sum((points[1:] ** 2 - points[:1] ** 2), axis=1)

        p = np.linalg.pinv(Q) @ Di

        xy = p[:2]
        a = p[-1]

        pError = np.linalg.norm(xy - actual)
        aError = np.abs(aActual - a) / aActual * 100
        # print(i , pError, aError)

        if i == 4:
            print(xy)
            print(actual)
            print(pError)
            print(aError)

        dErrors.append(pError)
        aErrors.append(aError)

        plt.scatter(points[:, 0], points[:, 1], label="Tags")
        plt.scatter(actual[:, 0], actual[:, 1], label="Actual")
        plt.scatter(xy[0], xy[1], label="Pred")
        plt.legend()
        plt.show()

    # plt.plot(dErrors)
    # plt.show()
    # plt.plot(aErrors)
    # plt.show()
    # # Ai =
