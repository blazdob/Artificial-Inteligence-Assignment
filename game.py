import pygame
from math import sin, cos, pi, radians, degrees, copysign
from pygame.math import Vector2
from pygame.locals import *
import math
import numpy as np
import time
import random

from sensors import Sensors
from action import Action

class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('images/race_pads.png')
    hit = pygame.image.load('images/collision.png')

    def __init__(self, position):
        super(PadSprite, self).__init__()
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
        self.image = self.normal

    def update(self, hit_list):
        if self in hit_list:
            self.image = self.hit
        else:
            self.image = self.normal


class VerticalPad(pygame.sprite.Sprite):
    normal = pygame.image.load('images/vertical_pads.png')

    def __init__(self, position):
        super(VerticalPad, self).__init__()
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
        self.image = self.normal


class SmallHorizontalPad(pygame.sprite.Sprite):
    normal = pygame.image.load('images/small_horizontal.png')

    def __init__(self, position):
        super(SmallHorizontalPad, self).__init__()
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
        self.image = self.normal


class SmallVerticalPad(pygame.sprite.Sprite):
    normal = pygame.image.load('images/small_vertical.png')

    def __init__(self, position):
        super(SmallVerticalPad, self).__init__()
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
        self.image = self.normal


class CarSprite(pygame.sprite.Sprite):
    TURN_SPEED = 10

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = 5
        self.direction = 0
        self.k_left = self.k_right = 0
        self.crashed = False

    def restart_position(self, position):
        self.position = position
        self.speed = 5
        self.direction = 0
        self.k_left = self.k_right = 0
        self.crashed = False


    def update(self, deltat):
        # SIMULATION
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * pi / 180
        x += -self.speed * sin(rad)
        y += -self.speed * cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

pads = [
    VerticalPad((10, 610)),
    PadSprite((30, 350)),
    SmallVerticalPad((200, 626)),
    SmallHorizontalPad((314, 500)),
    SmallVerticalPad((270, 220)),
    SmallVerticalPad((425, 380)),
    PadSprite((532, 105)),
    SmallHorizontalPad((540, 265)),
    SmallVerticalPad((790, 220)),
    SmallVerticalPad((650, 400)),
    SmallHorizontalPad((788, 512)),
    SmallHorizontalPad((928, 332)),
    SmallHorizontalPad((1012, 332)),
    SmallVerticalPad((925, 625)),
    VerticalPad((1123, 584)),
    VerticalPad((1123, 614)),
    PadSprite((680, 740)),
    PadSprite((440, 740)),
    PadSprite((240, 870)),
    SmallHorizontalPad((550, 870)),
    PadSprite((885, 870))
]


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("AI Car game")
        width = 1200
        height = 900
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.pad_group = pygame.sprite.RenderPlain(*pads)
        self.car = CarSprite('images/car.png', (100, 730))
        self.sensors = Sensors(self.car.position, self.car.direction, self.pad_group)
        self.ticks = 60
        self.font = pygame.font.Font(None, 75)
        self.exit = False

    def run(self, action):
        car_group = pygame.sprite.RenderPlain(self.car)
        self.sensors = Sensors(self.car.position, self.car.direction, self.pad_group)
        self.car.speed += 0.01
        dt = self.clock.get_time() / 1000

        if action == 0:
            self.car.k_right = -3.5
            self.car.k_left = 0
        elif action == 1:
            self.car.k_left = 3.5
            self.car.k_right = 0

        self.screen.fill((0, 0, 0))
        car_group.update(dt)

        collisions = pygame.sprite.groupcollide(car_group, self.pad_group, False, False, collided=None)
        if collisions != {}:
            self.car.speed = 0
            self.car.k_right = 0
            self.car.k_left = 0
            self.car.crashed = True

        self.sensors.update_sensors(self.car.position, self.car.direction)
        for sens in self.sensors.sens_objs:
            sens.draw(self.screen)

        self.pad_group.update(collisions)
        self.pad_group.draw(self.screen)
        car_group.draw(self.screen)
        # Counter Render
        pygame.display.flip()

        self.clock.tick(self.ticks)

    def is_crashed(self):
        return self.car.crashed

    def get_sensor_values(self):
        return self.sensors.sens_objs

    def step(self, action):

        self.run(action)

        state = [-(200 / (sen.length - 15)) for sen in self.get_sensor_values()]
        state = np.array([state])
        
        if self.is_crashed():
            reward = -500
            self.car.restart_position((100, 730))
        else:
            reward = 10 + sum(state[0])
        return reward, state



if __name__ == '__main__':
    game = Game()
    while True:
        game.step(random.randint(0, 3))
