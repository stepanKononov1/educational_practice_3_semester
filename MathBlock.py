# from time import sleep
import numpy as np
from numba import njit, int16, int8


class MathCalc:
    def __init__(self, height: int16, width: int16, matrix: np.array) -> None:
        self.__height = height
        self.__width = width
        self.__matrix = matrix
        self.__stack_memory = []

    def update(self) -> np.array:
        temp = get_next_matrix(self.__height, self.__width, self.__matrix)
        self.__stack_memory.append(self.__matrix)
        self.__matrix = temp
        return self.__matrix

    def get_previous_matrix(self):
        return self.__stack_memory.pop()

    def set_matrix(self, matrix: np.array):
        self.__matrix = matrix


@njit(fastmath=True,
      locals={'count': int8}
      )
def get_next_matrix(height: int16, width: int16, matrix_to_check: np.array) -> np.array:
    temp = np.zeros((height, width), dtype=np.bool_)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            count = (
                    sum(matrix_to_check[i - 1][j - 1:j + 2])
                    + matrix_to_check[i][j - 1]
                    + matrix_to_check[i][j + 1]
                    + sum(matrix_to_check[i + 1][j - 1:j + 2])
            )

            if not matrix_to_check[i, j]:
                if count == 3:
                    temp[i, j] = True
            else:
                if count == (2 or 3):
                    temp[i, j] = True

    return temp


# mat = np.array([
#     [0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0],
#     [0, 0, 1, 0, 0],
#     [0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0],
# ], dtype=np.bool_)
#
# math = MathCalc(5, 5, mat)
#
# while True:
#     sleep(1)
#     print(f'{math.update()}\n')
