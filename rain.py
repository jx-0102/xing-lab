"""rain.py —— 数字雨。

屏幕上会下起一场绿色的雨，每一列都有自己的速度和尾巴长度。
纯标准库，没有任何依赖。

运行：python rain.py
按键：空格 = 切换速度    q = 退出
"""
import random
import sys
import time

import xt

# 雨点用的字符。全是半角字符，保证在任何终端里都占一格。
CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&*+=<>"

# 每一档的帧间隔（秒），按空格循环切换
SPEEDS = [0.16, 0.10, 0.065, 0.04]


class Drop(object):
    """一列雨。"""

    __slots__ = ("y", "speed", "tail")

    def __init__(self, rows):
        self.reset(rows, top=False)

    def reset(self, rows, top):
        if top:
            self.y = random.randint(-rows, 0)
        else:
            self.y = random.randint(0, rows)
        self.speed = random.choice([1, 1, 1, 1, 2])
        self.tail = random.randint(4, max(6, rows // 2))


def main(frames=None):
    xt.setup()
    cols, rows = xt.size()
    cols = max(20, min(cols - 1, 100))
    rows = max(8, min(rows - 1, 34))

    drops = [Drop(rows) for _ in range(cols)]
    speed_index = 2

    xt.clear()
    xt.hide_cursor()
    done = 0
    try:
        while True:
            for d in drops:
                d.y += d.speed
                if d.y - d.tail > rows:
                    d.reset(rows, top=True)

            grid = [[" "] * cols for _ in range(rows)]
            shade = [[""] * cols for _ in range(rows)]
            for c, d in enumerate(drops):
                for k in range(d.tail):
                    y = d.y - k
                    if 0 <= y < rows:
                        grid[y][c] = random.choice(CHARS)
                        if k == 0:
                            shade[y][c] = "white+"
                        elif k <= 2:
                            shade[y][c] = "green+"
                        elif k <= d.tail // 2:
                            shade[y][c] = "green"
                        else:
                            shade[y][c] = "gray"

            buf = [xt.HOME]
            for r in range(rows):
                current = None
                line = []
                for c in range(cols):
                    s = shade[r][c] or "gray"
                    if s != current:
                        line.append(xt.color_code(s))
                        current = s
                    line.append(grid[r][c])
                line.append(xt.RESET)
                buf.append("".join(line))
            sys.stdout.write("\n".join(buf))
            sys.stdout.flush()

            if xt.key_pressed():
                k = xt.read_key()
                xt.flush_keys()
                if k in ("q", "esc"):
                    break
                if k == "space":
                    speed_index = (speed_index + 1) % len(SPEEDS)

            done += 1
            if frames is not None and done >= frames:
                break
            time.sleep(SPEEDS[speed_index])
    except KeyboardInterrupt:
        pass
    finally:
        xt.show_cursor()
        xt.clear()

    print(xt.style("  雨停了。", "green+", "bold"))
    print(xt.style("  （想看下一场：python rain.py）", "gray"))


if __name__ == "__main__":
    main(xt.frames_from_argv())
