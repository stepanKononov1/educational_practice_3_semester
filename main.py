import tkinter as tk
import GameLife

root = tk.Tk()
height = 600
width = 600
cell_size = 10
root.geometry('{}x{}'.format(width, height))
game = GameLife.GameOfLife(root, round(width // cell_size), round(height * 0.9 // cell_size), cell_size)
root.mainloop()
