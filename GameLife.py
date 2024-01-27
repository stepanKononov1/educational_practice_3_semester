import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np


class GameOfLife:
    def __init__(self, root, width, height, cell_size):
        self.__brush_radius = 0
        # Создаём верхнее поле

        self.__main_menu = tk.Menu()
        self.__main_menu.add_cascade(label="Файл")
        self.__main_menu.add_cascade(label="Вид")
        self.__main_menu.add_cascade(label="Справка")

        self.__root = root
        self.__root.title('КА "Игра Жизнь"')
        self.__root.config(menu=self.__main_menu)
        self.__width = width
        self.__height = height
        self.__cell_size = cell_size
        self.__running = True

        # Создаём клеточное поле
        self.__canvas = tk.Canvas(self.__root, width=self.__width * self.__cell_size,
                                  height=self.__height * self.__cell_size, bg="black")
        self.__canvas.pack(expand=True, anchor=N)

        self.cells = np.zeros((self.__height, self.__width), dtype=int)
        
        self.__canvas.bind("<B1-Motion>", self.__toggle_cell)
        self.__canvas.bind("<Button-1>", self.__toggle_cell)
        self.__root.bind("<Button-3>", self.toggle_pause)
        self.__root.bind("<B3-Motion>", self.toggle_pause)

        # Создаем кнопки
        self.__increase_brush_button = ttk.Button(text="Увеличить кисть", command=self.increase_brush)
        self.__increase_brush_button.pack(side=LEFT)

        self.__decrease_brush_button = ttk.Button(text="Уменьшить кисть", command=self.decrease_brush)
        self.__decrease_brush_button.pack(side=LEFT)

        # self.__previous_step = ttk.Button(text='|<')
        # self.__previous_step.pack(side=LEFT)

        self.__pause_button = ttk.Button(text='Пауза', command=self.toggle_pause)
        self.__pause_button.pack(side=LEFT)

        # self.__next_step = ttk.Button(text='>|', command=self.next_move)
        # self.__next_step.pack(side=LEFT)

        # Виджет Label для отображения значения self.__brush_radius
        self.__brush_label = ttk.Label(text=f"Текущий радиус кисти: {self.__brush_radius + 1}")
        self.__brush_label.pack(side=RIGHT)

        self.__update()

    def __toggle_cell(self, event):
        x, y = event.x // self.__cell_size, event.y // self.__cell_size
        self.__toggle_cells_around(x, y)
        self.__redraw()

    def __toggle_cells_around(self, x, y):
        for i in range(-self.get_brush_radius(), self.get_brush_radius() + 1):
            for j in range(-self.get_brush_radius(), self.get_brush_radius() + 1):
                nx, ny = (x + i) % self.__width, (y + j) % self.__height
                self.cells[ny][nx] = 1 if np.random.rand() < 0.5 else 0

    def __draw_cell(self, x, y):
        color = "white" if self.cells[y][x] else "black"
        x0, y0 = x * self.__cell_size, y * self.__cell_size
        self.__canvas.create_rectangle(x0, y0, x0 + self.__cell_size,
                                       y0 + self.__cell_size, fill=color,
                                       outline="white")

    def __count_neighbors(self, x, y):
        neighbor_indices = [
            ((x+i) % self.__width, (y+j) % self.__height)
            for i in range(-1, 2)
            for j in range(-1, 2) if not (i == 0 and j == 0)
        ]
        return sum(self.cells[ny][nx] for nx, ny in neighbor_indices)

    def __step(self):
        new_cells = np.zeros((self.__height, self.__width), dtype=int)

        for y in range(self.__height):
            for x in range(self.__width):
                neighbors = self.__count_neighbors(x, y)
                if self.cells[y][x]:
                    new_cells[y][x] = 1 if neighbors in (2, 3) else 0
                else:
                    new_cells[y][x] = 1 if neighbors == 3 else 0

        self.cells = new_cells

    def __redraw(self):
        self.__canvas.delete("all")
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                self.__draw_cell(x, y)

    def __update(self, *args):
        if self.__running:
            self.__step()
            self.__redraw()
        self.__root.after(1, self.__update)

    def next_move(self, *args):
        self.__step()
        self.__redraw()

    def toggle_pause(self, *args):
        self.__running = not self.__running
        
    def increase_brush(self):
        self.__brush_radius += 1
        self.__brush_label.config(text=f"Текущий радиус кисти: {self.__brush_radius}")

    def decrease_brush(self):
        self.__brush_radius = max(0, self.__brush_radius - 1)
        self.__brush_label.config(text=f"Текущий радиус кисти: {self.__brush_radius}")

    def get_brush_radius(self):
        __brush_radius = self.__brush_radius
        return __brush_radius
