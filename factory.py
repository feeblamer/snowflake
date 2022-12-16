from abc import ABC, abstractmethod
import numpy as np


class Shape(ABC):

    def __init__(self, num_petal, thick_ray, petal_length, angle_degrees):
        self.num_petal = num_petal
        self.angle_degrees = angle_degrees
        self.angle_radians = np.radians(angle_degrees)
        self.thick_ray = thick_ray
        self.petal_length = petal_length

    @property
    def _start_point(self):
        half_angle_rads = np.radians(self.angle_degrees / 2)
        x_start = self.thick_ray / 2
        y_start = 0.5 * self.thick_ray / np.tan(half_angle_rads)
        return np.array([x_start, y_start])

    @abstractmethod
    def generate_coordinates(self):
        pass


class SimpleShape(Shape):

    @property
    def start_coordinates(self):
        coordinates = np.array([
            [0, self.petal_length],
            [-self.thick_ray, self.petal_length],
            [-self.thick_ray, 0],
        ])
        result = [c + self._start_point for c in coordinates]
        return result

    def rotate_petal_coordinates(self):
        alpha = self.angle_radians
        for n in range(1, self.num_petal):
            for x, y in self.start_coordinates:
                next_x = x * np.cos(n * alpha) - y * np.sin(n * alpha)
                next_y = x * np.sin(n * alpha) + y * np.cos(n * alpha)
                yield np.array([next_x, next_y])

    def generate_coordinates(self):
        yield from self.start_coordinates
        yield from self.rotate_petal_coordinates()


class SecondShape(Shape):

    @property
    def subpetal_length(self):
        beta = np.radians(30)
        x = 0.62 * self.petal_length * np.sin(self.angle_radians / 2)
        gamma = beta + self.angle_radians / 2
        return (x / np.cos(gamma)) / 1.61

    @property
    def start_coordinates(self):
        beta = np.radians(60)
        sub_petal_length = self.subpetal_length
        coordinates = np.array([
            [0, y := 0.5 * self.petal_length],
            [x := sub_petal_length * np.cos(beta), y2 := y + np.tan(beta) * x],
            [x - np.sin(beta) * self.thick_ray, y2 + np.cos(beta) * self.thick_ray],
            [0, y4 := y + self.thick_ray / np.cos(beta)],
            [0, y4 + sub_petal_length],
        ])
        revers = coordinates[::-1]
        mirror = np.array([[-x - self.thick_ray, y] for x, y in revers])
        last_coord = [[-self.thick_ray, 0]]
        all_coords = np.append(np.append(coordinates, mirror, axis=0), last_coord, axis=0)

        result = [c + self._start_point for c in all_coords]
        return result

    def rotate_petal_coordinates(self):
        alpha = self.angle_radians
        for n in range(1, self.num_petal):
            for x, y in self.start_coordinates:
                next_x = x * np.cos(n * alpha) - y * np.sin(n * alpha)
                next_y = x * np.sin(n * alpha) + y * np.cos(n * alpha)
                yield np.array([next_x, next_y])

    def generate_coordinates(self):
        yield from self.start_coordinates
        yield from self.rotate_petal_coordinates()


class ThirdShape(Shape):

    def __init__(self, *args):
        super().__init__(*args)
        self.before_petal = 0.62 * self.petal_length
        self.square_diagonal = self.before_petal / 3
        self.square_cathetus = np.sin(np.radians(45)) * self.square_diagonal
        self.subpetal_length = self.square_diagonal * 1.68
        self.subpetal_angle_radians = np.radians(45)

    @property
    def start_coordinates(self):
        coordinates = np.array([
            [0, y := self.square_diagonal],
            [np.cos(np.radians(45)) * self.square_cathetus, y := y + self.square_diagonal * 0.5],
            [0, y := y + self.square_diagonal * 0.5],
            [0, y := y + self.square_diagonal],
            [x := np.cos(self.subpetal_angle_radians) * self.subpetal_length,
             y := y + np.tan(self.subpetal_angle_radians) * x],
            [x - np.sin(self.subpetal_angle_radians) * self.thick_ray,
             y + np.cos(self.subpetal_angle_radians) * self.thick_ray],
            [0, y := self.thick_ray / np.cos(self.subpetal_angle_radians) + self.before_petal],
            [0, y + self.subpetal_length],
        ]
        )

        revers = coordinates[::-1]
        mirror = np.array([[-x - self.thick_ray, y] for x, y in revers])
        last_coord = [[-self.thick_ray, 0]]
        all_coords = np.append(np.append(coordinates, mirror, axis=0), last_coord, axis=0)

        result = [c + self._start_point for c in all_coords]
        return result

    def rotate_petal_coordinates(self):
        alpha = self.angle_radians
        for n in range(1, self.num_petal):
            for x, y in self.start_coordinates:
                next_x = x * np.cos(n * alpha) - y * np.sin(n * alpha)
                next_y = x * np.sin(n * alpha) + y * np.cos(n * alpha)
                yield np.array([next_x, next_y])

    def generate_coordinates(self):
        yield from self.start_coordinates
        yield from self.rotate_petal_coordinates()


class ShapeFactory:
    shapes = {'simple shape': SimpleShape,
              'second shape': SecondShape,
              'third shape': ThirdShape,
              }

    def __init__(self,
                 shape_name: str,
                 num_petal: int,
                 thick_ray: int,
                 petal_length: int,
                 angle_degrees
                 ):
        self.shape = self.shapes[shape_name](
            num_petal,
            thick_ray,
            petal_length,
            angle_degrees)
