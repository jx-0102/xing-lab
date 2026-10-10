"""xing.py —— 玩具箱的入口。

双击它，或者在终端里：python xing.py
按下数字键就直接进去，不用敲回车。

里面的四个东西全是用 Python 自带的库写的，
没有第三方依赖 —— 拷到任何一台装了 Python 的电脑上都能跑。
"""
import clock
import life
import rain
import snake
import xt


def menu(cols):
    title = (xt.style("XING  LAB", "cyan+", "bold")
             + xt.style("   ·   ", "gray")
             + xt.style("兴 的 终 端 玩 具 箱", "white+"))
    rows = [
        ("1", "数字雨", "一整屏字符往下掉，每列都有自己的速度"),
        ("2", "贪吃蛇", "方向键控制，吃得越多跑得越快"),
        ("3", "生命游戏", "四条规则，长出会爬、会死的小世界"),
        ("4", "大字时钟", "把现在的时间画成一整屏大字"),
        ("q", "退出", ""),
    ]
    body = [xt.center(title, cols), ""]
    for key, name, desc in rows:
        body.append(xt.center("  " + xt.style(key, "yellow+", "bold") + "   "
                              + xt.style("%-8s" % name, "green+")
                              + xt.style(desc, "gray"), cols))
    body.append("")
    body.append(xt.center(xt.style("按对应的键，直接开始", "gray"), cols))
    return body


def main():
    xt.setup()
    cols, _ = xt.size()

    actions = {
        "1": rain.main,
        "2": snake.main,
        "3": life.main,
        "4": clock.main,
    }

    while True:
        xt.clear()
        xt.show_cursor()
        print("\n".join(menu(cols)))

        key = xt.wait_key()
        if key in ("q", "esc", "enter"):
            xt.clear()
            print(xt.style("  下次再来。", "cyan+"))
            return
        action = actions.get(key)
        if action is None:
            continue
        action()


if __name__ == "__main__":
    main()
