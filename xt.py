"""xt.py —— 兴的小工具箱：让终端听话的那几件事。

这个文件不单独运行，被其他几个玩具 import 用。
里面全是 Python 自带的库，不需要安装任何东西。
"""
import os
import re
import shutil
import sys
import time
import unicodedata

# 让中文和各种符号在 Windows 上也能正常输出（即使输出被重定向也安全）
for _stream in (sys.stdout, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

IS_WIN = os.name == "nt"

# ------------------------------------------------------------------ 颜色
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

FG = {
    "black": 30, "red": 31, "green": 32, "yellow": 33,
    "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
    "gray": 90,
    "red+": 91, "green+": 92, "yellow+": 93, "blue+": 94,
    "magenta+": 95, "cyan+": 96, "white+": 97,
}

_ANSI = re.compile("\033\\[[0-9;?]*[a-zA-Z]")


def color_code(name):
    """拿到某个颜色的转义码（没这个名字就返回空串）。"""
    return "\033[%dm" % FG[name] if name in FG else ""


def style(text, *names):
    """给一段文字上色。例：style("你好", "green+", "bold")"""
    prefix = ""
    for n in names:
        if n == "bold":
            prefix += BOLD
        elif n == "dim":
            prefix += DIM
        else:
            prefix += color_code(n)
    if not prefix:
        return str(text)
    return prefix + str(text) + RESET


# ------------------------------------------------------------------ 排版
def width(text):
    """算一段文字在屏幕上有多少列宽（中文按 2 列算，颜色代码不占宽）。"""
    plain = _ANSI.sub("", str(text))
    total = 0
    for ch in plain:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            total += 2
        else:
            total += 1
    return total


def center(text, columns=None, fill=" "):
    """把一行字居中（能正确处理中文和颜色代码）。"""
    if columns is None:
        columns, _ = size()
    pad = max(0, (columns - width(text)) // 2)
    return fill * pad + str(text)


# ------------------------------------------------------------------ 屏幕
CLEAR = "\033[2J\033[H"
HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def setup():
    """Windows 上要先敲一下，终端才认识 \033[ 开头的颜色代码。"""
    if IS_WIN:
        os.system("")


def clear():
    sys.stdout.write(CLEAR)
    sys.stdout.flush()


def home():
    """光标回左上角。逐帧重画时用它，屏幕不会闪。"""
    sys.stdout.write(HOME)
    sys.stdout.flush()


def hide_cursor():
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()


def size(fallback=(80, 24)):
    """终端有多大（列, 行）。"""
    s = shutil.get_terminal_size(fallback)
    return s.columns, s.lines


def write(text):
    sys.stdout.write(text)
    sys.stdout.flush()


# ------------------------------------------------------------------ 键盘
# 目标：按一下就能读到，不用再敲回车。
if IS_WIN:
    import msvcrt

    _ARROWS = {b"H": "up", b"P": "down", b"K": "left", b"M": "right"}

    def key_pressed():
        return msvcrt.kbhit()

    def read_key():
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            return _ARROWS.get(msvcrt.getch(), "?")
        if ch == b"\x1b":
            return "esc"
        if ch in (b"\r", b"\n"):
            return "enter"
        if ch == b" ":
            return "space"
        try:
            return ch.decode("utf-8").lower()
        except UnicodeDecodeError:
            return "?"

    def flush_keys():
        """把连击残留的按键吃掉。"""
        while msvcrt.kbhit():
            msvcrt.getch()
else:
    import select
    import termios
    import tty

    _ARROWS = {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}

    def key_pressed():
        ready, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(ready)

    def read_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                return _ARROWS.get(sys.stdin.read(2), "esc")
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        if ch in ("\r", "\n"):
            return "enter"
        if ch == " ":
            return "space"
        return ch.lower()

    def flush_keys():
        while key_pressed():
            read_key()


def wait_key():
    """一直等，直到按下某个键。"""
    while not key_pressed():
        time.sleep(0.02)
    key = read_key()
    flush_keys()
    return key


def frames_from_argv(default=None):
    """命令行里给了 --frames N 就跑 N 帧然后退出（用来做自动测试）。
    没给就返回 default —— 通常写 None，意思是一直跑下去。"""
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--frames" and i + 1 < len(args):
            try:
                return int(args[i + 1])
            except ValueError:
                pass
    return default
