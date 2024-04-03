# coding:utf-8
"""
 * @Author superKing
 * @Date 2024-04-04 02:46:02
"""
import tkinter as tk
import random
import json
import configparser


class LoadConfig:
    """
    读取配置文件
    """

    def __init__(self) -> None:
        pass

    def init_config(
        self,
    ):
        """
        从配置文件内，初始化一些数据
        """
        # 创建配置解析器
        self.config = configparser.ConfigParser()
        self.config.read("./config.ini", encoding="utf-8")

        self.title_text = self.config["views"]["title_text"]
        self.blank_min_num = int(self.config["views"]["blank_min_num"])
        self.blank_max_num = int(self.config["views"]["blank_max_num"])

        self.loadconfig_button_text = self.config["views"]["loadconfig_button_text"]
        self.generate_button_text = self.config["views"]["generate_button_text"]
        self.show_solution_button_text = self.config["views"][
            "show_solution_button_text"
        ]
        self.hide_solution_button_text = self.config["views"][
            "hide_solution_button_text"
        ]
        self.export_button_text = self.config["views"]["export_button_text"]

        self.width = int(self.config["views"]["width"])
        self.height = int(self.config["views"]["height"])
        self.font_size = int(self.config["views"]["font_size"])
        self.font_padding = int(self.config["views"]["font_padding"])
        self.interval = self.height // 9


class DataCalculation:
    """
    数据处理
    """

    def __init__(self) -> None:
        pass

    def init_datas(
        self,
    ):
        """初始化数据"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        # 隐藏的答案
        self.answer = {}

    def remove_numbers(self):
        """
        随机删除数字
        """
        num_to_remove = random.randint(self.blank_min_num, self.blank_max_num)
        # 0-8 的所有排列组合
        row_col_list = [(x, y) for x in range(9) for y in range(9)]
        for _ in range(num_to_remove):
            while True:
                obj = random.choice(row_col_list)
                row_col_list.remove(obj)
                row, col = obj[0], obj[1]
                if self.board[row][col] != 0:
                    self.answer[(row, col)] = self.board[row][col]
                    self.board[row][col] = 0
                    break
                else:
                    pass

        # print(self.board)

    def solve_sudoku(self, board):
        """
        回溯算法，保证生成的数据是符合数独要求
        """
        empty = self.find_empty_location(board)
        if not empty:
            return True

        row, col = empty

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0

        return False

    @staticmethod
    def find_empty_location(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def show_solution(self):
        """
        显示答案
        """

        for obj in self.answer:
            self.board[obj[0]][obj[1]] = self.answer[obj]

    def hide_solution(self):
        """
        隐藏答案
        """
        for obj in self.answer:
            self.board[obj[0]][obj[1]] = 0

    @staticmethod
    def is_safe(board, row, col, num):
        return (
            DataCalculation.is_safe_row(board, row, num)
            and DataCalculation.is_safe_col(board, col, num)
            and DataCalculation.is_safe_box(board, row - row % 3, col - col % 3, num)
        )

    @staticmethod
    def is_safe_row(board, row, num):
        return num not in board[row]

    @staticmethod
    def is_safe_col(board, col, num):
        return all(board[i][col] != num for i in range(9))

    @staticmethod
    def is_safe_box(board, row, col, num):
        return all(board[row + i][col + j] != num for i in range(3) for j in range(3))


class SudokuGame(DataCalculation, LoadConfig):
    """
    主要是界面操作 和 数据互动
    """

    def __init__(self, master):
        self.init_config()
        self.master = master

        self.canvas = None
        self.popup = None
        self.init_view()

    def init_view(
        self,
    ):

        self.init_datas()
        self.init_config()

        if self.canvas:
            self.destroy_widgets()
            self.create_widgets()
        else:
            self.create_widgets()
        self.master.title(self.title_text)

    def destroy_widgets(self):
        """
        界面重新加载
        """
        self.canvas.destroy() if self.canvas else ...
        self.loadconfig_button.destroy() if self.loadconfig_button else ...
        self.generate_button.destroy() if self.generate_button else ...
        self.show_solution_button.destroy() if self.show_solution_button else ...
        self.hide_solution_button.destroy() if self.hide_solution_button else ...
        self.export_button.destroy() if self.export_button else ...
        self.popup.destroy() if self.popup else ...

    def create_widgets(self):
        """
        生成界面，以及绑定事件
        """
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()

        self.loadconfig_button = tk.Button(
            self.master, text=self.loadconfig_button_text, command=self.init_view
        )
        self.loadconfig_button.pack(side="left", padx=10, pady=5)

        self.generate_button = tk.Button(
            self.master, text=self.generate_button_text, command=self.generate_puzzle
        )
        self.generate_button.pack(side="left", padx=10, pady=5)

        self.show_solution_button = tk.Button(
            self.master, text=self.show_solution_button_text, command=self.show_solution
        )
        self.show_solution_button.pack(side="left", padx=10, pady=5)

        self.hide_solution_button = tk.Button(
            self.master, text=self.hide_solution_button_text, command=self.hide_solution
        )
        self.hide_solution_button.pack(side="left", padx=10, pady=5)

        self.export_button = tk.Button(
            self.master, text=self.export_button_text, command=self.open_popup
        )
        self.export_button.pack(side="left", padx=10, pady=5)
        self.draw_grid()

    def open_popup(
        self,
    ):
        if self.popup:
            self.popup.destroy()

        self.popup = tk.Toplevel(self.canvas)
        self.popup.title("当前界面的二维数组")

        # 创建多行文本框
        text = tk.Text(self.popup, wrap="word")

        # 添加示例文本
        sample_text = json.dumps(self.board)
        text.insert(tk.END, sample_text)
        text.pack(side="left", padx=self.width // 10, pady=self.height // 10)

    def draw_grid(self):
        """
        分割线
        """
        for i in range(10):
            color = "black" if i % 3 == 0 else "gray"

            self.canvas.create_line(
                i * self.interval, 0, i * self.interval, self.height, fill=color
            )
            self.canvas.create_line(
                0, i * self.interval, self.height, i * self.interval, fill=color
            )

    def generate_puzzle(self):

        self.canvas.delete("all")
        self.init_datas()
        self.draw_grid()

        # 生成数组
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku(board)
        self.board = board

        self.solution = [row[:] for row in self.board]
        self.answer = {}

        # 随机移除元素
        self.remove_numbers()

        # 更新数据到界面
        self.update_board(show_solution=False)

    def show_solution(self):
        """
        显示答案
        """
        super().show_solution()
        self.update_board(show_solution=True)

    def hide_solution(self):
        """
        隐藏答案
        """
        super().hide_solution()
        self.update_board(show_solution=False)

    def update_board(self, show_solution=False):
        self.canvas.delete("all")
        self.draw_grid()
        # print("更新页面")
        for i in range(9):
            for j in range(9):
                x = j * self.interval + self.font_padding
                y = i * self.interval + self.font_padding
                num = self.board[i][j]

                if num != 0:
                    if show_solution and (i, j) in self.answer:
                        num = self.solution[i][j]
                        self.canvas.create_text(
                            x, y, text=num, font=("Arial", self.font_size), fill="red"
                        )
                    else:
                        self.canvas.create_text(
                            x, y, text=num, font=("Arial", self.font_size)
                        )


def main():
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
