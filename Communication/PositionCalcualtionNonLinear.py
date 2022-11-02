import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares


def error(guess, points, distances):
    xyz, a = guess[:3], guess[-1]

    return np.linalg.norm(points - xyz, 2, axis=1) - distances * a


def calculate_pos(guess, points, powers):
    guess = np.array(guess)
    points = np.array(points)
    powers = np.array(powers).reshape((-1, 1))

    output = least_squares(error, x0=guess, args=(points, powers))

    return output.x[:3], output.x[-1]


if __name__ == '__main__':
    # np.random.seed(42)

    aErrors = []
    dErrors = []

    scale = 10

    pointDim = 3
    n = 10

    for n in range(1, 10):
        points = np.random.random((n, pointDim)) * scale

        actual = np.random.random((1, pointDim)) * scale / 1.5
        aActual = np.random.rand() * 10

        distances = np.linalg.norm(points - actual, 2, axis=1)
        distances += np.random.normal(0, .5)

        distances /= aActual

        guess = np.array((0, 0, 0, 1))
        out = calculate_pos(guess, points, distances)

        xy = out[:pointDim]
        a = out[-1]
        # print(out.x, actual, aActual)

        pError = np.linalg.norm(xy - actual)
        aError = np.abs(aActual - a) / aActual * 100
        print(n, pError, aError)

        dErrors.append(pError)
        aErrors.append(aError)

        plt.scatter(points[:, 0], points[:, 1], label="Tags")
        plt.scatter(actual[:, 0], actual[:, 1], label="Actual")
        plt.scatter(xy[0], xy[1], label="Pred")
        plt.legend()
        plt.title(f"n={n} Tags")
        plt.show()

    plt.plot(dErrors)
    plt.show()
    # plt.plot(aErrors)
    # plt.show()
    # # Ai =
