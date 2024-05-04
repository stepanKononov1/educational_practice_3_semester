import numpy as np
from numba import njit, int16, int8

import config as cfg


class MatrixCalculator:
    def __init__(self) -> None:
        self.__height = cfg.matrix_height
        self.__width = cfg.matrix_width
        self.__matrix = cfg.init_matrix
        self.__stack_memory = [cfg.init_matrix]

    def __update(self) -> np.array:
        temp = get_next_matrix(self.__height, self.__width, self.__matrix)
        self.__matrix = temp
        self.update_stack()
        return self.__matrix

    def update_stack(self):
        self.__stack_memory.append(self.__matrix)
        if len(self.__stack_memory) > 100:
            self.__stack_memory.pop(0)
    
    def get_matrix_without_border(self, matrix) -> np.array:
        return get_trim_matrix(self.__height, self.__width, matrix)

    def __get_previous_matrix(self):
        try:
            stack_matrix = self.__stack_memory.pop()
        except IndexError:
            stack_matrix = self.__matrix
        self.__matrix = stack_matrix
        return stack_matrix
    
    def set_matrix(self, matrix: np.array):
        self.__matrix = matrix

    def get_matrix(self):
        return self.__matrix

    def do_single_update_interface(self):
        return self.get_matrix_without_border(self.__update())

    def do_single_previous_interface(self):
        return self.get_matrix_without_border(self.__get_previous_matrix())


@njit(fastmath=True,
      locals={
          'count': int8,
          'i': int16,
          'j': int16
      }
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
                if count in (2, 3):
                    temp[i, j] = True
                else:
                    temp[i, j] = False

    return temp


@njit(fastmath=True,
      locals={
          'i': int16,
          'j': int16
      }
      )
def get_trim_matrix(height: int16, width: int16, matrix: np.array) -> np.array:
    temp = np.zeros((height - 2, width - 2), dtype=np.bool_)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            temp[i - 1][j - 1] = matrix[i][j]
    return temp
