import pygame
import math

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

def draw(win, images, player_car, game_info, x_offset, y_offset, main_font, height, mask):
    win.fill((0, 0, 0))
    for img, pos in images:
        win.blit(img, (pos[0] + x_offset, pos[1] + y_offset))

    level_text = main_font.render(f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, height - level_text.get_height() - 70))

    time_text = main_font.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, height - time_text.get_height() - 40))

    vel_text = main_font.render(f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, height - vel_text.get_height() - 10))
    player_car.draw(win, x_offset, y_offset)
    
    player_car.circle_hit_check(x_offset, y_offset, win, mask)

    pygame.display.update()

def handle_collision(player_car, game_info, track_border_mask, finish_mask, finish_position):
    collision_point = player_car.collide(track_border_mask, 0, 0)
    # if collision_point is not None:
    #     # player_car.bounce()
    #     game_info.reset()
    #     player_car.reset()

    # player_finish_poi_collide = player_car.collide(finish_mask, *finish_position)
    # if player_finish_poi_collide is not None:
    #     if player_finish_poi_collide[1] == 0:
    #         # player_car.bounce()
    #         game_info.reset()
    #         player_car.reset()
    #     else:
    #         game_info.next_level()
    #         player_car.reset()
    #         print(f"Advanced to next level: {game_info.level}")

def polar_to_cartesian(theta_degrees, r):
    # 將角度從度轉換為弧度
    theta_radians = math.radians(theta_degrees)
    
    # 計算直角坐標
    x = r * math.cos(theta_radians)
    y = r * math.sin(theta_radians)
    
    return x, y