from abstractCar import AbstractCar
import utils
import pygame

class PlayerCar(AbstractCar):
    def __init__(self, RED_CAR, max_vel, rotation_vel):
        IMG = RED_CAR
        START_POS = (180, 200)
        super().__init__(max_vel, rotation_vel, IMG, START_POS)

        self.pair_list = []
        for first in range(-90, 91, 45):
            self.pair_list.append([first, 20])
            self.pair_list.append([first, 30])
        

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def circle_hit_check(self, mask, screen):
        collision_point_list = []

        for i in self.pair_list:
            cir_x_rel , cir_y_rel = utils.polar_to_cartesian(i[0] - self.angle -90 , i[1])
            cir_x, cir_y = (cir_x_rel + self.x + 38/8),  (cir_y_rel + self.y + 76/8)

            # print(f"cir x: {cir_x}, cir y: {cir_y}")
            pygame.draw.circle(screen, pygame.Color(255, 0, 0), (cir_x, cir_y), 5)
            
            collision_point = mask.get_at((cir_x , cir_y))
            collision_point_list.append(collision_point)

        return collision_point_list