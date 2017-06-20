import numpy as np
from scipy.linalg import eig


class ellipse:
    """
    Ellipse Fitting Module
    Data should be numpy array with 2 * n matrix
    data[0] = x-coordinates
    data[1] = y-coordinates
    """

    def __init__(self, data):
        self.data = data
        self.size = len(data[0])

    def fitting(self):
        """
        follow courtney, 2004
        return coefficients vector a
        a[0] = x**2 coeff
        a[1] = xy coeff
        a[2] = y**2 coeff
        a[3] = x coeff
        a[4] = y coeff
        a[5] = 1 coeff

        """
        D = np.ndarray(shape=(self.size, 6), dtype=float)
        D[:, 0] = self.data[0] ** 2
        D[:, 1] = self.data[1] ** 2
        D[:, 2] = self.data[0] * self.data[1]
        D[:, 3] = self.data[0]
        D[:, 4] = self.data[1]
        D[:, 5] = 1.
        # Set D matrix Finished
        S = np.matmul(np.transpose(D), D)
        # Set S matrix Finished
        C = np.zeros(shape=(3, 3), dtype=float)
        C[0, 2] = 2
        C[1, 1] = -1
        C[2, 0] = 2
        # Set C matrix Finished

        # Now start to block decomposition
        S_11 = S[0:3, 0:3]
        S_12 = S[0:3, 3:6]
        S_21 = S[3:6, 0:3]
        S_22 = S[3:6, 3:6]
        E_temp = np.matmul(S_12, np.matmul(np.linalg.inv(S_22), S_21))
        # (lamda * I - E) a_1 = 0
        E = np.matmul(np.linalg.inv(C), S_11 - E_temp)
        # Now solve eigenvalue equation
        eigen_result = eig(E, left=False, right=True)
        a_1 = np.array([0, 0, 0], dtype=float)
        # select positive eigenvalues' eigenvector
        for i in range(3):
            a_1[i] = eigen_result[1][i][eigen_result[0] > 0]
        # scaling factor k
        k = 4 * a_1[2] * a_1[0] - a_1[1] * a_1[1]
        k = np.sqrt(1. / k)
        a_1 *= k
        a_2 = -np.matmul(np.linalg.inv(S_22), np.matmul(S_21, a_1))
        return np.concatenate((a_1, a_2))
