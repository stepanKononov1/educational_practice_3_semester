import numpy as np

# we can change this parameters
main_window_height = 1200
main_window_width = 600
cell_size = 20

# but we CAN'T change anything under this line
matrix_height = round(main_window_width * 0.7 * cell_size ** -1)
matrix_width = round(main_window_height * 0.7 * cell_size ** -1)

matrix_window_padding_x = 300
matrix_window_padding_y = 40

matrix_window_height = matrix_width * cell_size
matrix_window_width = matrix_height * cell_size

init_matrix = np.random.choice([True, False], size=(matrix_height, matrix_width))

min_speed = 16
max_speed = 1000
min_size_brash = 100
max_size_brash = 500
brush_step = 100
