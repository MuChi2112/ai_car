import pygame
from abstractCar  import AbstractCar

class PlayerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel, red_car, start_pos):
        IMG = red_car
        super().__init__(max_vel, rotation_vel, IMG, start_pos)
        
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()
    
    def calculate_offset(player_car, width, height):
        x_offset = width / 2 - player_car.x
        y_offset = height / 2 - player_car.y
        return x_offset, y_offset