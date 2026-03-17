"""Draw a spirograph"""

import turtle as tt
from pathlib import Path
from typing import Literal

save_path = Path("/")

# Set the background color as black,
# pensize as 2 and speed 10 (relative)
tt.bgcolor("black")
tt.pensize(2)
tt.speed(100)


def draw_spiro(
    size: int = 100,
    reps: Literal[2, 3, 4, 5, 6, 9, 12, 15, 30, 45, 60] = 2,
    hole: int = 0,
) -> None:
    """reps x len(colours) x move left = 360"""

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

    for i in range(reps):
        # Choose your color combination
        for color in colors:
            tt.down()
            tt.color(color)
            tt.circle(size)  # cdraw ircle(radius)
            tt.left(gap)  # Move left(pixels)
            tt.up()
            tt.forward(hole)

    tt.hideturtle()  # hide cursor


"""

for i in range(6):
    draw_spiro(30, 6, 10)
    tt.left(60)

"""

if __name__ == "__main__":
    draw_spiro(100, 12, 0)

    tt.done()  # leaves screen window open
    # tt.exitonclick()
