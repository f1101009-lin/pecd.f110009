import tkinter as tk
from tkinter import messagebox
import random
import time

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("踩地雷遊戲")

        # ===== 遊戲基本設定 =====
        self.rows = 9
        self.cols = 9
        self.mines = 10

        self.first_click = True
        self.start_time = None

        # ===== 上方資訊區 =====
        top_frame = tk.Frame(root)
        top_frame.pack(pady=5)

        self.time_label = tk.Label(top_frame, text="時間：0 秒")
        self.time_label.pack(side=tk.LEFT, padx=10)

        restart_btn = tk.Button(top_frame, text="重新開始", command=self.restart)
        restart_btn.pack(side=tk.LEFT)

        # ===== 棋盤區 =====
        self.board_frame = tk.Frame(root)
        self.board_frame.pack()

        self.create_game()

    # =========================
    # 建立新遊戲
    # =========================
    def create_game(self):
        self.first_click = True
        self.start_time = None
        self.time_label.config(text="時間：0 秒")

        self.buttons = {}
        self.flags = set()
        self.mines_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # 清空舊棋盤
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # 建立按鈕
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=3,
                    height=1,
                    command=lambda r=r, c=c: self.left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # =========================
    # 放置地雷（第一次點擊後）
    # =========================
    def place_mines(self, safe_r, safe_c):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        positions.remove((safe_r, safe_c))

        for r, c in random.sample(positions, self.mines):
            self.mines_map[r][c] = -1
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.mines_map[nr][nc] != -1:
                            self.mines_map[nr][nc] += 1

    # =========================
    # 左鍵點擊
    # =========================
    def left_click(self, r, c):
        if self.buttons[(r, c)]["state"] == "disabled":
            return

        # 第一次點擊才放地雷
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
            self.start_time = time.time()
            self.update_timer()

        # 踩到地雷
        if self.mines_map[r][c] == -1:
            self.show_all_mines()
            self.buttons[(r, c)].config(bg="red")
            self.disable_all_buttons()
            messagebox.showinfo("遊戲結束", "你踩到地雷了！")
        else:
            self.reveal(r, c)
            self.check_win()

    # =========================
    # 右鍵插旗
    # =========================
    def right_click(self, r, c):
        btn = self.buttons[(r, c)]
        if btn["state"] == "disabled":
            return

        if btn["text"] == "":
            btn.config(text="🚩")
            self.flags.add((r, c))
        elif btn["text"] == "🚩":
            btn.config(text="")
            self.flags.remove((r, c))

    # =========================
    # 顯示數字
    # =========================
    def reveal(self, r, c):
        btn = self.buttons[(r, c)]
        if btn["state"] == "disabled":
            return

        value = self.mines_map[r][c]
        btn.config(
            text=str(value) if value > 0 else "",
            relief=tk.SUNKEN,
            state="disabled"
        )

    # =========================
    # 勝利判斷
    # =========================
    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mines_map[r][c] != -1:
                    if self.buttons[(r, c)]["state"] != "disabled":
                        return
        self.disable_all_buttons()
        messagebox.showinfo("恭喜", "你成功完成踩地雷！")

    # =========================
    # 顯示所有地雷
    # =========================
    def show_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mines_map[r][c] == -1:
                    self.buttons[(r, c)].config(text="💣", bg="pink")

    # =========================
    # 停用所有按鈕
    # =========================
    def disable_all_buttons(self):
        for btn in self.buttons.values():
            btn.config(state="disabled")

    # =========================
    # 計時器
    # =========================
    def update_timer(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"時間：{elapsed} 秒")
            self.root.after(1000, self.update_timer)

    # =========================
    # 重新開始
    # =========================
    def restart(self):
        self.create_game()

# ===== 主程式 =====
root = tk.Tk()
game = Minesweeper(root)
root.mainloop()
