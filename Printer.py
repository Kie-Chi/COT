import time
from blessed import Terminal
import curses
from wcwidth import wcwidth

class Printer:
    def __init__(self):
        self.term = Terminal()
        self.progress = 1.0  # 进度条初始值
        self.width = self.term.width
        self.flag = 1

    def stop(self):
        """显示提示信息并等待用户按键"""
        with self.term.cbreak():
            print(self.term.yellow("(按下 Enter 键继续)"), end="\r")
            self.term.inkey()
            print("                     ", end="\r")

    def end(self):
        self.progress = 0
        self.draw_progress_bar()
        self.term.inkey()

    def pre_print(self):
        print(self.term.cyan("COT>"), end="")

    def print_out(self, text="", fg_color="white", bg_color="black", style="", delay=0.05, end="\n"):
        """逐字符打印文本"""
        for char in text: 
            func = getattr(self.term, fg_color)
            color_text = func(char)
            print(color_text, end="", flush=True)
            if self.progress > 0.01:
                self.update_progress(delta=0.002)
            time.sleep(delay)
        print(end, end="")
    def draw_progress_bar(self, bar_length=50):
        """绘制进度条"""
        full_blocks = int(self.progress * bar_length)
        remaining = self.progress * bar_length - full_blocks
        partial_block = "▏▎▍▌▋▊▉█"[round(remaining * 8) - 1] if remaining > 0 else ""
        empty_blocks = bar_length - full_blocks - (1 if partial_block else 0)
        bar = "█" * full_blocks + partial_block + " " * empty_blocks
        with self.term.location(0, 0):  # 固定光标位置
            if self.progress == 1.0:
                print(self.term.green(f"[{bar}] 100%"))
            elif self.progress > 0.6:
                print(self.term.green(f"[{bar}] {int(self.progress * 100)}% "))
            elif self.progress > 0.2:
                print(self.term.yellow(f"[{bar}] {int(self.progress * 100)}% "))
            elif self.progress > 0:
                print(self.term.red(f"[{bar}] {max(1, int(self.progress * 100))}%  "))
            else:
                print(f"[{bar}] {int(self.progress * 100)}%  ")
    def update_progress(self, delta=0.01):
        """更新进度条值"""
        self.progress = max(0.0, self.progress - delta)
        self.draw_progress_bar()

    def run(self, *funcs):
        """运行指定的主函数"""
        with self.term.fullscreen(), self.term.hidden_cursor():
            self.term.clear()
            with self.term.location(0, 1):
                for func in funcs:
                    func(self)

    def class_start(self, obj, *args):
        funcs = [getattr(obj, arg, None) for arg in args]
        self.run(*funcs)
        
if __name__ == "__main__":
    # print("▏▎▍▌▋▊▉█")
    # printer = Printer()
    # printer.run(example_usage)
    pass