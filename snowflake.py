import math
import sys
import turtle


def get_subpetal_length(length_before_subpetal, angle):
    angle_rad = math.radians(angle)
    x = length_before_subpetal * math.sin(angle_rad / 2)
    gamma = math.radians(30) + angle_rad / 2

    return (x / math.cos(gamma)) / 1.61


def draw_petal(thickness, petal_length, angle):
    turtle.pendown()
    length_before_subpetal = petal_length

    subpetal_lenght = get_subpetal_length(length_before_subpetal, angle)
    # 2/3 длинны
    turtle.forward(length_before_subpetal)
    # лучи
    turtle.right(60)

    turtle.forward(subpetal_lenght)
    turtle.circle(thickness / 2, 180)
    # обратная сторона
    a = math.radians(60)
    x = thickness / math.tan(a)

    turtle.forward(subpetal_lenght - x)
    turtle.right(180)
    turtle.left(60)

    turtle.forward(subpetal_lenght)

    turtle.circle(thickness / 2, 180)

    turtle.forward(subpetal_lenght)
    turtle.right(180)
    turtle.left(60)

    turtle.forward(subpetal_lenght - x)
    turtle.circle(thickness / 2, 180)
    turtle.forward(subpetal_lenght)
    turtle.right(60)
    turtle.forward(length_before_subpetal)


def positional(angle, thickness):
    turtle.penup()
    turtle.right(angle / 2)
    hypo = math.sin(angle / 2) * 0.5 * thickness
    turtle.forward(hypo)
    turtle.left(angle / 2)


def draw_snowflake(n_petal, thickness=20, petal_length=50):
    turtle.setheading(90)
    angle = 360 / n_petal
    positional(angle, thickness)
    for _ in range(n_petal):
        draw_petal(thickness, petal_length, angle)
        turtle.right(180)
        turtle.left(angle)
    turtle.penup()


def main():
    turtle.penup()
    turtle.hideturtle()
    turtle.bgcolor("#161481")
    turtle.fillcolor("#ffffff")
    turtle.pencolor("#000000")
    turtle.pensize(7)
    turtle.begin_fill()
    draw_snowflake(11, 40, 200)
    turtle.end_fill()


if __name__ == "__main__":
    turtle.Screen().title("Снежинка")
    try:
        main()
        turtle.exitonclick()
    except turtle.Terminator as e:
        sys.exit(0)
