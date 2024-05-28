import pygame
from abstractCar  import AbstractCar
from utils import polar_to_cartesian

class PlayerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel, red_car, start_pos):
        IMG = red_car
        super().__init__(max_vel, rotation_vel, IMG, start_pos)

        second_values = [10, 15, 20, 25]

        self.pair_list = []
        for first in range(-90, 91, 45):
            self.pair_list.append([first, 50])
        
        for i in second_values:
            self.pair_list.append([0, i])
        

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
    
    def circle_hit_check(self, x_offset, y_offset, mask):
        collision_point_list = []

        for i in self.pair_list:
            cir_x_rel , cir_y_rel = polar_to_cartesian(i[0] - self.angle -90 , i[1])
            cir_x_true, cir_y_true = (cir_x_rel  + self.x + 19 * 0.4/25), (cir_y_rel  + self.y + 38 * 0.4/25)
            # pygame.draw.circle(screen, pygame.Color(255, 0, 0), (cir_x_true, cir_y_true), 5)
            
            collision_point = mask.get_at((self.x , self.y))
            collision_point_list.append(collision_point)

            
        return collision_point_list
