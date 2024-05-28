import pygame
import time
import math
import utils
from playerCar import PlayerCar
from abstractCar import AbstractCar
from checkPoint import CheckPoint, current_point


class CarGame:
    def __init__(self):
        pygame.font.init()

        self.GRASS = utils.scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
        self.TRACK = utils.scale_image(pygame.image.load("imgs/track.png"), 0.9)

        self.TRACK_BORDER = utils.scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
        self.TRACK_BORDER_MASK = pygame.mask.from_surface(self.TRACK_BORDER)

        self.FINISH = pygame.image.load("imgs/finish.png")
        self.FINISH_MASK = pygame.mask.from_surface(self.FINISH)
        self.FINISH_POSITION = (130, 250)

        self.RED_CAR = utils.scale_image(pygame.image.load("imgs/red-car.png"), 0.25)
        self.WIDTH, self.HEIGHT = self.TRACK.get_width(), self.TRACK.get_height()
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Racing Game!")

        self.MAIN_FONT = pygame.font.SysFont("comicsans", 44)

        self.FPS = 60

        self.score = 0

        self.run = True
        self.clock = pygame.time.Clock()
        self.images = [(self.GRASS, (0, 0)), (self.TRACK, (0, 0)),
                (self.FINISH, self.FINISH_POSITION), (self.TRACK_BORDER, (0, 0))]
        self.player_car = PlayerCar(self.RED_CAR, 4, 4)

        self.game_info = utils.GameInfo()

        self.collision_point_list = []
        self.target = 0

    def play_game(self, move):

        reward, done = 0, 0

        self.target = 0

        self.clock.tick(self.FPS)

        self.player_car.circle_hit_check(self.TRACK_BORDER_MASK, self.WIN)

        self.collision_point_list = utils.draw(self.WIN, self.images, self.player_car, self.game_info, self.MAIN_FONT, self.WIDTH, self.HEIGHT, self.TRACK_BORDER_MASK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    pygame.quit()

        utils.move_player(self.player_car, move)

        done = utils.handle_collision(self.player_car, self.game_info, self.TRACK_BORDER_MASK, self.FINISH_MASK, self.FINISH_POSITION)

        reward , self.target = CheckPoint.check_distance(self.player_car)

        if self.player_car.vel < 0.5:
            # print("vel < 0.5")
            reward -= 10

        if self.score <= -100:
            done = True

        if done is True:
            reward -= 100
        # print(f"angle: {self.target}")
        
        self.score += reward

        # print(self.score)

        return reward, done, self.score

    def reset(self):
        global current_point
        current_point = 0
        self.game_info.reset()
        self.player_car.reset()
        self.score = 0

        
