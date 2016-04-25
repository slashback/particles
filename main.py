# coding: utf-8

from scene import *
from random import choice, randint
from uuid import uuid4

GAME_SPEED = 0.6
POINTS_COUNT = 20
DISTANCE = 80


class Particle(object):
    def __init__(
            self,
            position_x,
            position_y,
            direction_x,
            direction_y,
            speed=GAME_SPEED,
            radius=0.5
    ):
        self._id = uuid4()
        self.radius = radius
        self.diameter = self.radius * 2
        self.position = dict(
                x=position_x,
                y=position_y
        )
        self.speed_modifier = speed
        self.direction_x = direction_x
        self.direction_y = direction_y

    @property
    def x(self):
        return self.position['x']

    @x.setter
    def x(self, value):
        self.position['x'] = value

    @property
    def y(self):
        return self.position['y']

    @y.setter
    def y(self, value):
        self.position['y'] = value


class MyScene(Scene):
    def setup(self):
        self.points = []
        self.init_points(POINTS_COUNT)
        self.distance_to_link = DISTANCE

    def init_points(self, count):
        directions = (-2, -1, 1, 2)
        for i in xrange(count):
            # random position
            pos_x = randint(0, self.size.w)
            pos_y = randint(0, self.size.h)
            # random direction
            dir_x = choice(directions)
            dir_y = choice(directions)

            point = Particle(
                    pos_x,
                    pos_y,
                    dir_x,
                    dir_y
            )
            self.points.append(point)

    def move(self, point):
        collision_right = point.x > (self.size.w - point.diameter)
        collision_top = point.y > (self.size.h - point.diameter)
        collision_left = point.x < 0
        collision_bottom = (point.y + point.diameter) < 0

        if collision_right or collision_left:
            point.direction_x *= -1

        if collision_top or collision_bottom:
            point.direction_y *= -1

        # move
        point.position['x'] += (point.speed_modifier * point.direction_x)

        point.position['y'] += (point.speed_modifier * point.direction_y)

    def close_enough(self, point1, point2):
        dist_x = abs(point1.x - point2.x)
        dist_y = abs(point1.y - point2.y)
        if dist_x < self.distance_to_link and dist_y < self.distance_to_link:
            return True

    def draw_particle(self, particle):
        ellipse(
                particle.x,
                particle.y,
                particle.diameter,
                particle.diameter
        )

    def draw_line(self, one, other):
        line(
                one.x + one.radius,
                one.y + one.radius,
                other.x + other.radius,
                other.y + other.radius
        )

    def draw_lines(self, point):
        for other_point in self.points:
            if point._id == other_point._id:
                continue
            if self.close_enough(point, other_point):
                self.draw_line(
                        point,
                        other_point
                )

    def update(self):
        background(1, 1, 1)
        fill(1, 1, 1)
        stroke(0.9, 0.9, 0.9)
        stroke_weight(1)

        for point in self.points:
            self.draw_particle(point)
            self.draw_lines(point)
            self.move(point)


if __name__ == '__main__':
    run(MyScene(), show_fps=True)
