import tkinter as tk
from tkinter import messagebox
import random

# ===== 改良版踩地雷（第二版）=====
class MinesweeperV2:
    def __init__(self, root):
        self.root = root
        self.root.title("踩地雷 V2")

        self.rows = 6
        self.cols = 6
        self.mines = 6

        self.first_click = True
        self.buttons = {}
        self.flags = set()
        self.mines_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        top = tk.Frame(root)
        top.pack()
        tk.Button(top, text="重新開始", command=self.restart).pack()

        self.board = tk.Frame(root)
        self.board.pack()

        self.create_buttons()

    def create_buttons(self):
        self.buttons.clear()
        for widget in self.board.winfo_children():
            widget.destroy()

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board,
                    width=3,
                    height=1,
                    command=lambda r=r, c=c: self.left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def place_mines(self, safe_r, safe_c):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        positions.remove((safe_r, safe_c))
        for r, c in random.sample(positions, self.mines):
            self.mines_map[r][c] = -1

    def left_click(self, r, c):
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False

        if self.mines_map[r][c] == -1:
            self.buttons[(r, c)].config(text="💣", bg="red")
            messagebox.showinfo("結束", "你踩到地雷了！")
        else:
            self.buttons[(r, c)].config(text="安全", state="disabled")

    def right_click(self, r, c):
        btn = self.buttons[(r, c)]
        if btn["text"] == "":
            btn.config(text="🚩")
            self.flags.add((r, c))
        elif btn["text"] == "🚩":
            btn.config(text="")
            self.flags.remove((r, c))

    def restart(self):
        self.first_click = True
        self.mines_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_buttons()

root = tk.Tk()
game = MinesweeperV2(root)
root.mainloop()
