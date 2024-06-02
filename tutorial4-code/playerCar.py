from abstractCar import AbstractCar
import utils
import pygame
import math
from playerCar import PlayerCar

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
    
    def check_radar(self, mask, player_car):
        collision_point_list = []
        for degree in range(-90, 120, 45):
            length = 0
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

            current_rader = player_car.collide(mask)

            # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
            while current_rader != None and length < 300:
                length = length + 1
                x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
                y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

            # Calculate Distance To Border And Append To Radars List
            dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
            self.radars.append([(x, y), dist])

        return collision_point_list
    
    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

        