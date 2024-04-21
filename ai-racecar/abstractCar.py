import pygame
import math

from utils import blit_rotate_center

class AbstractCar:
    def __init__(self, max_vel, rotation_vel, img, start_pos):
        self.img = img
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = start_pos
        self.acceleration = 0.1
        self.start_pos = start_pos
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win, x_offset, y_offset):
        blit_rotate_center(win, self.img, (self.x + x_offset, self.y + y_offset), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0, x_offset=0, y_offset=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x + x_offset), int(self.y - y + y_offset))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0