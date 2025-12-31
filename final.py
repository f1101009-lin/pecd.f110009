import tkinter as tk
from tkinter import messagebox
import random

# ===== 基本踩地雷（第一版）=====
class MinesweeperV1:
    def __init__(self, root):
        self.root = root
        self.root.title("踩地雷 V1")

        self.rows = 5
        self.cols = 5
        self.mines = 5

        self.buttons = {}
        self.mines_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.place_mines()
        self.create_buttons()

    def place_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        for r, c in random.sample(positions, self.mines):
            self.mines_map[r][c] = -1

    def create_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.root,
                    width=4,
                    height=2,
                    command=lambda r=r, c=c: self.click(r, c)
                )
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def click(self, r, c):
        if self.mines_map[r][c] == -1:
            self.buttons[(r, c)].config(text="💣", bg="red")
            messagebox.showinfo("結束", "你踩到地雷了！")
        else:
            self.buttons[(r, c)].config(text="安全", state="disabled")

root = tk.Tk()
game = MinesweeperV1(root)
root.mainloop()
