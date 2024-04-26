import numpy as np

main_window_height = 1200
main_window_width = 800

# scale must be below one
matrix_window_padding_x = 300
matrix_window_padding_y = 40

cell_size = 10

matrix_window_height = round(main_window_height * 0.8) // cell_size * cell_size
matrix_window_width = round(main_window_width * 0.8) // cell_size * cell_size

matrix_height = int(matrix_window_height / cell_size)
matrix_width = int(matrix_window_width / cell_size)

init_matrix = np.random.choice([True, False], size=(matrix_height, matrix_width))
