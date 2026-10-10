"""snake.py —— 终端贪吃蛇。

运行：python snake.py
操作：方向键 或 W A S D 控制，q 退出
规则：吃到 * 得 10 分，撞墙或咬到自己就结束，吃得越多跑得越快
"""
import collections
import random
import time

import xt

HEAD = "@"
BODY = "o"
FOOD = "*"
WALL = "#"
BLANK = " "


def new_food(width, height, snake):
    """在空着的地方随机放一颗食物。"""
    while True:
        p = (random.randrange(width), random.randrange(height))
        if p not in snake:
            return p


def draw(width, height, snake, food, score):
    body = set(snake)
    body.discard(snake[0])

    top = "+" + WALL * width + "+"
    lines = [
        xt.HOME,
        "  " + xt.style("得分 ", "gray") + xt.style("%-4d" % score, "yellow+", "bold"),
        "  " + xt.style(top, "gray"),
    ]
    for y in range(height):
        current = "__start__"
        row = [xt.style("|", "gray")]
        for x in range(width):
            p = (x, y)
            if p == snake[0]:
                want, ch = "green+", HEAD
            elif p in body:
                want, ch = "green", BODY
            elif p == food:
                want, ch = "red+", FOOD
            else:
                want, ch = None, BLANK
            if want != current:
                row.append(xt.RESET if want is None else xt.color_code(want))
                current = want
            row.append(ch)
        row.append(xt.RESET)
        row.append(xt.style("|", "gray"))
        lines.append("  " + "".join(row))
    lines.append("  " + xt.style(top, "gray"))
    lines.append("  " + xt.style("方向键 / WASD 控制，q 退出", "gray"))
    xt.write("\n".join(lines))


def play(width, height, frames=None):
    """玩一局，返回这一局的分数。给了 frames 就跑够帧数自动收工（方便自动测试）。"""
    snake = collections.deque([(width // 2, height // 2)])
    direction = (1, 0)
    pending = direction
    food = new_food(width, height, snake)
    score = 0
    tick = 0.16
    done = 0

    xt.clear()
    xt.hide_cursor()
    try:
        while True:
            while xt.key_pressed():
                k = xt.read_key()
                if k in ("q", "esc"):
                    return score
                where = {
                    "up": (0, -1), "w": (0, -1),
                    "down": (0, 1), "s": (0, 1),
                    "left": (-1, 0), "a": (-1, 0),
                    "right": (1, 0), "d": (1, 0),
                }.get(k)
                # 不许原地掉头
                if where and (where[0] + direction[0], where[1] + direction[1]) != (0, 0):
                    pending = where

            direction = pending
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            if not (0 <= head[0] < width and 0 <= head[1] < height):
                return score                      # 撞墙
            if head in snake:
                return score                      # 咬到自己

            snake.appendleft(head)
            if head == food:
                score += 10
                food = new_food(width, height, snake)
                tick = max(0.05, tick - 0.004)     # 越吃越快
            else:
                snake.pop()

            draw(width, height, snake, food, score)
            done += 1
            if frames is not None and done >= frames:
                return score
            time.sleep(tick)
    finally:
        xt.show_cursor()


def main(frames=None):
    xt.setup()
    cols, rows = xt.size()
    width = max(16, min(cols - 6, 56))
    height = max(8, min(rows - 8, 20))

    best = 0
    while True:
        score = play(width, height, frames)
        best = max(best, score)
        xt.clear()
        xt.show_cursor()
        print()
        print("  " + xt.style("— 这一局结束了 —", "red+", "bold"))
        print()
        print("  本局得分  " + xt.style(str(score), "yellow+", "bold")
              + "     最高分  " + xt.style(str(best), "green+", "bold"))
        print()
        print("  " + xt.style("空格", "cyan+") + " 再来一局      "
              + xt.style("q", "cyan+") + " 退出")
        if frames is not None:
            print()
            print("  " + xt.style("自动测试结束（跑了 %d 帧）。" % frames, "gray"))
            return
        while True:
            k = xt.wait_key()
            if k in ("q", "esc"):
                print()
                print("  " + xt.style("下次再来。", "gray"))
                return
            if k == "space":
                break


if __name__ == "__main__":
    main(xt.frames_from_argv())
