"""Draw a spirograph"""

import sys
import turtle as tt
from typing import Literal

from utils.notate import FORMAT, notate

sys.path.append("./")


DEBUG = True


@notate(
    DEBUG,
    docs=DEBUG,
    note="Remember to close window after drawing",
    warn="DANGER!",
    name_fmt=FORMAT.WHITE + FORMAT.BOLD,
)
def draw_spiro(
    size: int = 100,
    reps: Literal[2, 3, 4, 5, 6, 9, 12, 15, 30, 45, 60] = 2,
    hole: int = 0,
) -> None:
    """Draws a spirograph with the given size, repetitions, and hole size."""
    # Set the background color as black,
    # pensize as 2 and speed 10 (relative)
    tt.bgcolor("black")
    tt.pensize(2)
    tt.speed(100)

    colors = [
        "red",
        "magenta",
        "blue",
        "cyan",
        "green",  # 'white',
        "yellow",
    ]
    num = reps * len(colors)
    gap = int(360 / num)

    for _i in range(reps):
        # Choose your color combination
        for color in colors:
            tt.down()
            tt.color(color)
            tt.circle(size)  # cdraw ircle(radius)
            tt.left(gap)  # Move left(pixels)
            tt.up()
            tt.forward(hole)

    tt.hideturtle()  # hide cursor
    tt.exitonclick()
    # tt.done()  # leaves screen window open

    return None


if __name__ == "__main__":
    draw_spiro(100, 12, 0)
