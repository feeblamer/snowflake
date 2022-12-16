import math
import turtle
from abc import ABC, abstractmethod

from factory import ShapeFactory


class Snowflake(ABC):

    def __init__(self, num_petal, thick_ray, petal_length, name_shape="simple shape"):
        self.num_petal = num_petal
        self.thick_ray = thick_ray
        self.petal_length = petal_length
        self.shape = ShapeFactory(name_shape, num_petal, thick_ray, petal_length, self.angle_degrees).shape

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def draw_petal(self):
        pass

    @abstractmethod
    def draw_shape(self):
        pass

    @property
    def angle_degrees(self):
        return 360 / self.num_petal


class Context:
    def __init__(self, snowflake: Snowflake):
        self.snowflake = snowflake

    def draw_snowflake(self):
        # self.snowflake.draw()
        self.snowflake.draw_shape()


class SnowflakeTurtle(Snowflake):

    def draw_shape(self):
        # self.set_start_draw_point()
        turtle.penup()
        turtle.setpos(self.shape._start_point)
        turtle.pendown()
        coordinates = self.shape.generate_coordinates()
        for coordinates in coordinates:
            turtle.setpos(coordinates)
        turtle.hideturtle()
        turtle.exitonclick()

    def draw_petal(self):
        turtle.pendown()
        length_before_subpetal = self.petal_length

        subpetal_lenght = self.get_subpetal_length(length_before_subpetal)
        # 2/3 длинны
        turtle.forward(length_before_subpetal)
        # лучи
        turtle.right(60)

        turtle.forward(subpetal_lenght)

        edge_radius = self.thick_ray / 2

        turtle.circle(edge_radius, 180)

        # обратная сторона
        a = math.radians(60)
        x = self.thick_ray / math.tan(a)

        turtle.forward(subpetal_lenght - x)
        turtle.right(180)
        turtle.left(60)

        turtle.forward(subpetal_lenght)

        turtle.circle(edge_radius, 180)

        turtle.forward(subpetal_lenght)
        turtle.right(180)
        turtle.left(60)

        turtle.forward(subpetal_lenght - x)
        turtle.circle(edge_radius, 180)
        turtle.forward(subpetal_lenght)
        turtle.right(60)
        turtle.forward(length_before_subpetal)

    def draw(self):
        turtle.setheading(90)
        self.set_start_draw_point()
        for _ in range(self.num_petal):
            self.draw_petal()
            turtle.right(180)
            turtle.left(self.angle_degrees)
        turtle.hideturtle()
        turtle.penup()
        turtle.exitonclick()

    def get_subpetal_length(self, length_before_subpetal):
        angle_rad = math.radians(self.angle_degrees)
        x = length_before_subpetal * math.sin(angle_rad / 2)
        gamma = math.radians(30) + angle_rad / 2

        return (x / math.cos(gamma)) / 1.61

    def set_start_draw_point(self):
        turtle.penup()

        half_angle_degrees = self.angle_degrees / 2
        turtle.right(half_angle_degrees)
        half_angle_rads = math.radians(half_angle_degrees)
        distance_to_start_point = math.sin(half_angle_rads) * 0.5 * self.thick_ray
        turtle.forward(distance_to_start_point)
        turtle.left(half_angle_degrees)
