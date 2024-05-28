import pygame
import time
import math
from checkPoint import CheckPoint, current_point

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width() /
                      2, win.get_height()/2 - render.get_height()/2))
    
def polar_to_cartesian(theta_degrees, r):
    # 將角度從度轉換為弧度
    theta_radians = math.radians(theta_degrees)
    
    # 計算直角坐標
    x = r * math.cos(theta_radians)
    y = r * math.sin(theta_radians)
    
    return x, y

def draw(win, images, player_car, game_info, MAIN_FONT, WIDTH, HEIGHT, TRACK_BORDER_MASK):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(
        f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(
        f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    CheckPoint.draw_current_checkpoint(win)

    collision_point_list = player_car.circle_hit_check(TRACK_BORDER_MASK, win)

    player_car.draw(win)
    pygame.display.update()

    return collision_point_list



def move_player(player_car, keys):
    moved = False
    if keys == [1, 0, 1, 0]:
        player_car.rotate(left=True)
        moved = True
        player_car.move_forward()
    elif keys == [0, 1, 1, 0]:
        player_car.rotate(right=True)
        moved = True
        player_car.move_forward()
    elif keys == [1, 0, 0, 1]:
        player_car.rotate(left=True)
        moved = True
        player_car.move_backward()
    elif keys == [0, 1, 0, 1]:
        player_car.rotate(right=True)
        moved = True
        player_car.move_backward()
    elif keys == [1, 0, 0, 0]:
        player_car.rotate(left=True)
    elif keys == [0, 1, 0, 0]:
        player_car.rotate(right=True)
    elif keys == [0, 0, 1, 0]:
        moved = True
        player_car.move_forward()
    elif keys == [0, 0, 0, 1]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, game_info, TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.reset()
        CheckPoint.reset()
        print(f"check point: {current_point}")
        return True

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()

    return False

def distance(a_x, a_y, b_x, b_y):
    return math.sqrt((b_x - a_x) ** 2 + (b_y - a_y) ** 2)

def calculate_angle(player_car, check_point):
    delta_x = player_car.x - check_point[0]
    delta_y = player_car.y - check_point[1]
    
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)

    return angle_deg


class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)
    
    