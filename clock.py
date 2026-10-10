"""clock.py —— 大字时钟。

把现在的时间画成一整屏大字，每秒刷新。

运行：python clock.py
按键：q = 退出
"""
import time

import xt

# 每个字符都是 3 宽 5 高的点阵：1 亮，0 空
FONT = {
    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"],
    "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"],
    "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "111"],
    ":": ["000", "010", "000", "010", "000"],
    "-": ["000", "000", "111", "000", "000"],
    " ": ["000", "000", "000", "000", "000"],
}

WEEKDAYS = ["一", "二", "三", "四", "五", "六", "日"]


def render(text, scale):
    """把一行文字画成 5 行点阵。scale=2 时每个点用两个字符，看起来更胖。"""
    dot = "#" * scale
    blank = " " * scale
    gap = " " * scale
    rows = []
    for r in range(5):
        line = []
        for i, ch in enumerate(text):
            pattern = FONT.get(ch, FONT[" "])[r]
            for c in pattern:
                line.append(dot if c == "1" else blank)
            if i != len(text) - 1:
                line.append(gap)
        rows.append("".join(line))
    return rows


def main(frames=None):
    xt.setup()
    cols, rows = xt.size()
    scale = 2 if cols >= 70 else 1

    xt.clear()
    xt.hide_cursor()
    done = 0
    painted = None
    try:
        while True:
            now = time.localtime()
            stamp = time.strftime("%H:%M:%S", now)
            if stamp != painted:
                painted = stamp
                date_line = "%d 年 %d 月 %d 日   星期%s" % (
                    now.tm_year, now.tm_mon, now.tm_mday, WEEKDAYS[now.tm_wday])
                body = [xt.HOME, "", ""]
                for line in render(stamp, scale):
                    body.append(xt.center(xt.style(line, "cyan+", "bold"), cols))
                body.append("")
                body.append(xt.center(xt.style(date_line, "gray"), cols))
                body.append("")
                body.append(xt.center(xt.style("按 q 退出", "gray"), cols))
                xt.write("\n".join(body))

            if xt.key_pressed():
                k = xt.read_key()
                xt.flush_keys()
                if k in ("q", "esc"):
                    break

            done += 1
            if frames is not None and done >= frames:
                break
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        xt.show_cursor()
        xt.clear()
    print(xt.style("  时钟已关闭。", "cyan+"))


if __name__ == "__main__":
    main(xt.frames_from_argv())
