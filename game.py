import os 
import pygame
from math import sin, cos, pi, radians, degrees, copysign
from pygame.math import Vector2
from pygame.locals import *


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


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


class Trophy(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/trophy.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 10

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0

    def update(self, deltat):
        # SIMULATION
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        if self.k_up + self.k_down == 0:
            if self.speed < 0:
                self.speed += 0.08
            elif -0.08 < self.speed < 0.08:
                self.speed = 0
            else:
                self.speed += -0.08
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * pi / 180
        x += -self.speed * sin(rad)
        y += -self.speed * cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("AI Car game")
        width = 1200
        height = 800
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.font = pygame.font.Font(None, 75)
        self.exit = False

    def run(self):
        car = CarSprite('images/car.png', (100, 730))
        car_group = pygame.sprite.RenderPlain(car)
        car.ACCELERATION = 0.1

        pads = [
            VerticalPad((10, 650)),
            PadSprite((30, 400)),
            VerticalPad((200, 800)),
            SmallHorizontalPad((314, 550)),
            SmallVerticalPad((270, 270)),
            SmallVerticalPad((425, 430)),
            PadSprite((512, 155)),
            SmallHorizontalPad((540, 315)),
            SmallVerticalPad((760, 270)),
            SmallVerticalPad((650, 450)),
            PadSprite((890, 562)),
            SmallHorizontalPad((898, 382)),
            SmallHorizontalPad((1012, 382))
        ]
        pad_group = pygame.sprite.RenderPlain(*pads)

        trophies = [Trophy((1100, 450))]
        trophy_group = pygame.sprite.RenderPlain(*trophies)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if not hasattr(event, 'key'):
                    continue
                down = event.type == KEYDOWN
                if event.key == K_RIGHT:
                    car.k_right = down * -3.5
                elif event.key == K_LEFT:
                    car.k_left = down * 3.5
                elif event.key == K_UP:
                    car.k_up = down * 0.25
                elif event.key == K_DOWN:
                    car.k_down = down * -0.4
                elif event.key == K_ESCAPE:
                    self.exit = True  # quit the game
                elif event.key == K_SPACE:
                    self.run()

            self.screen.fill((0, 0, 0))
            car_group.update(dt)

            collisions = pygame.sprite.groupcollide(car_group, pad_group, False, False, collided=None)
            if collisions != {}:
                car.image = pygame.image.load('images/collision.png')
                car.MAX_FORWARD_SPEED = 0
                car.MAX_REVERSE_SPEED = 0
                car.k_right = 0
                car.k_left = 0

            trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True)
            if trophy_collision != {}:
                car.MAX_FORWARD_SPEED = 0
                car.MAX_REVERSE_SPEED = 0

            pad_group.update(collisions)
            pad_group.draw(self.screen)
            car_group.draw(self.screen)
            trophy_group.draw(self.screen)
            # Counter Render
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
