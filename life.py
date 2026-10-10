"""life.py —— 康威生命游戏。

只有四条规则，却能长出会爬、会繁殖、会自己消失的东西。
这一版把边界接成了环形：从右边走出去，会从左边回来。

运行：python life.py
按键：空格 = 暂停 / 继续    n = 换一批随机    g = 放一只滑翔机    q = 退出
"""
import random
import sys
import time

import xt

ALIVE = "#"
BLANK = " "


def step(alive, width, height):
    """按规则算出下一代。"""
    neighbors = {}
    for (x, y) in alive:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                p = ((x + dx) % width, (y + dy) % height)
                neighbors[p] = neighbors.get(p, 0) + 1

    nxt = set()
    for p, n in neighbors.items():
        if n == 3 or (n == 2 and p in alive):
            nxt.add(p)
    return nxt


def glider(x, y, width, height):
    """一只滑翔机 —— 它会斜着一直爬下去。"""
    shape = [(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)]
    return set(((x + a) % width, (y + b) % height) for a, b in shape)


def seed(width, height):
    """随机撒一片，再放一只滑翔机当彩头。"""
    alive = set()
    for y in range(height):
        for x in range(width):
            if random.random() < 0.22:
                alive.add((x, y))
    alive |= glider(2, 2, width, height)
    return alive


def draw(alive, width, height, generation, paused):
    status = "暂停中" if paused else "运行中"
    lines = [
        xt.HOME,
        "  " + xt.style("康威生命游戏", "cyan+", "bold")
        + xt.style("   第 %d 代" % generation, "gray")
        + xt.style("   %s" % status, "yellow+" if paused else "green"),
        "",
        "  " + xt.style("+" + "-" * width + "+", "gray"),
    ]
    for y in range(height):
        current = None
        row = [xt.style("|", "gray")]
        for x in range(width):
            if (x, y) in alive:
                want, ch = "green+", ALIVE
            else:
                want, ch = None, BLANK
            if want != current:
                row.append(xt.RESET if want is None else xt.color_code(want))
                current = want
            row.append(ch)
        row.append(xt.RESET)
        row.append(xt.style("|", "gray"))
        lines.append("  " + "".join(row))
    lines.append("  " + xt.style("+" + "-" * width + "+", "gray"))
    lines.append("  " + xt.style("空格", "cyan+") + " 暂停   "
                 + xt.style("n", "cyan+") + " 换一批   "
                 + xt.style("g", "cyan+") + " 放滑翔机   "
                 + xt.style("q", "cyan+") + " 退出")
    xt.write("\n".join(lines))


def main(frames=None):
    xt.setup()
    cols, rows = xt.size()
    width = max(16, min(cols - 6, 60))
    height = max(8, min(rows - 10, 24))

    alive = seed(width, height)
    generation = 0
    paused = False
    done = 0

    xt.clear()
    xt.hide_cursor()
    try:
        while True:
            draw(alive, width, height, generation, paused)

            deadline = time.time() + 0.12
            while time.time() < deadline:
                if xt.key_pressed():
                    k = xt.read_key()
                    xt.flush_keys()
                    if k in ("q", "esc"):
                        return
                    if k == "space":
                        paused = not paused
                    elif k == "n":
                        alive = seed(width, height)
                        generation = 0
                    elif k == "g":
                        alive |= glider(random.randrange(width), random.randrange(height),
                                        width, height)
                if paused:
                    deadline = time.time() + 0.05
                time.sleep(0.01)

            if not paused:
                alive = step(alive, width, height)
                generation += 1
                if not alive:
                    alive = seed(width, height)
                    generation = 0

            done += 1
            if frames is not None and done >= frames:
                return
    finally:
        xt.show_cursor()
        xt.clear()
    print(xt.style("  生命游戏结束。", "green+"))


if __name__ == "__main__":
    main(xt.frames_from_argv())
