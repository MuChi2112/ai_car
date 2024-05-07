import pygame
from utils import scale_image, blit_text_center, draw, handle_collision
from playerCar import PlayerCar
from gameInfo import GameInfo
from checkPoint import CheckPoint
import time
import sys


class CarGame :

    def __init__(self):
        pygame.font.init()
        self.MAIN_FONT = pygame.font.SysFont("comicsans", 44)
        self.TRACK = scale_image(pygame.image.load("imgs/track.png"), 1)
        self.TRACK_BORDER = scale_image(pygame.image.load("imgs/border.png"), 1)
        self.TRACK_BORDER_MASK = pygame.mask.from_surface(self.TRACK_BORDER)
        self.FINISH = pygame.transform.rotate(scale_image(pygame.image.load("imgs/finish.png"), 3), 155)

        self.current_check_point = 0

        self.CHECK_POINTS = []
        self.CHECK_POINTS_MASK = []
        for i in range(1, 6):
            self.CHECK_POINTS.append(scale_image(pygame.image.load(f"imgs/checkPoint({i}).png"), 1))
            self.CHECK_POINTS_MASK.append(pygame.mask.from_surface(self.CHECK_POINTS[i-1]))

        self.FINISH_MASK = pygame.mask.from_surface(self.FINISH)
        self.FINISH_POSITION = (14600, 11345)
        self.START_POS = (14561, 11548)

        self.RED_CAR = scale_image(pygame.image.load("imgs/car.png"), 0.4)
        self.CIRCLE = scale_image(pygame.image.load("imgs/circle.png"), 200)

        # self.WIDTH, self.HEIGHT = self.TRACK.get_width(), self.TRACK.get_height()
        self.WIDTH, self.HEIGHT = 1000, 925
        print(f"{self.WIDTH * 20} ,  {self.HEIGHT * 20}") 
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Racing Game!")

        self.min_distance = sys.maxsize

        self.FPS = 60

        self.run = True
        self.clock = pygame.time.Clock()
        self.images = [(self.TRACK, (0, 0)), (self.FINISH, self.FINISH_POSITION), (self.TRACK_BORDER, (0, 0))]
            


        self.player_car = PlayerCar(100, 4, self.RED_CAR, self.START_POS)
        
        self.game_info = GameInfo()

        self.check_point = CheckPoint(self.CHECK_POINTS[self.current_check_point], self.CHECK_POINTS_MASK[self.current_check_point])

        self.collision_point_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        


    def move_player(self, player_car, FINAL_MOVE):
        keys = FINAL_MOVE
        moved = False

        if keys == [1, 0, 0, 0]:
            player_car.rotate(left=True)
        if keys == [0, 1, 0, 0]:
            player_car.rotate(right=True)
        if keys == [0, 0, 1, 0]:
            moved = True
            player_car.move_forward()
        if keys == [0, 0, 0, 1]:
            moved = True
            player_car.move_backward()

        if not moved:
            player_car.reduce_speed()

    def play_game(self, FINAL_MOVE):

        reward = 0

        # time.sleep(0.1)
        self.clock.tick(self.FPS)

        x_offset, y_offset = PlayerCar.calculate_offset(self.player_car, self.WIDTH, self.HEIGHT)
        # print(f"x_offset: {x_offset},  y_offset: {y_offset}")
        
        self.collision_point_list = self.player_car.circle_hit_check(x_offset, y_offset, self.TRACK_BORDER_MASK)
        # print(collision_point_list)
        
        draw(self.WIN, self.images, self.player_car, self.game_info, x_offset, y_offset, self.MAIN_FONT, self.HEIGHT)

        self.move_player(self.player_car, FINAL_MOVE)
        score, done = handle_collision(self.player_car, self.game_info, self.TRACK_BORDER_MASK, self.FINISH_MASK, self.FINISH_POSITION)

        if(self.check_point.check_point_check(self.player_car, self.CHECK_POINTS_MASK[self.current_check_point])):
            self.current_check_point += 1
            print(f"current_check_point: {self.current_check_point}")
            if(self.current_check_point == 5):
                self.current_check_point = 0
                
            self.check_point = CheckPoint(self.CHECK_POINTS[self.current_check_point], self.CHECK_POINTS_MASK[self.current_check_point])
            self.min_distance = sys.maxsize
            print(f"distance: {self.check_point.calculate_check_point_distance(self.player_car.x, self.player_car.y)}")

        temp_distance = self.check_point.calculate_check_point_distance(self.player_car.x, self.player_car.y)

        if self.min_distance != sys.maxsize:
            reward += self.min_distance - temp_distance
        
        print(f"temp distance: {temp_distance}, min: {self.min_distance}")
        
        self.min_distance = min(self.min_distance, temp_distance)

        reward = score

        return reward, done, score
    
    def reset(self):
        self.game_info.reset()
        self.player_car.reset()