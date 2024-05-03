import pygame
from utils import scale_image, blit_text_center, draw, handle_collision
from playerCar import PlayerCar
from gameInfo import GameInfo
from checkPoint import CheckPoint


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

if __name__ == "__main__":
    
    rate = 1

    pygame.font.init()

    TRACK = scale_image(pygame.image.load("imgs/track.png"), 1 * rate)
    TRACK_BORDER = scale_image(pygame.image.load("imgs/border.png"), 1 * rate)
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = pygame.transform.rotate(scale_image(pygame.image.load("imgs/finish.png"), 3), 155 * rate)
    CHECK_POINT = scale_image(pygame.image.load("imgs/checkPoint.png"), 1 * rate)
    CHECK_POINT_MASK = pygame.mask.from_surface(CHECK_POINT)

    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (14600  * rate, 11345 * rate)
    START_POS = (14561 * rate, 11548  * rate)

    current_check_point = 0

    CHECK_POINTS = []
    CHECK_POINTS_MASK = []
    for i in range(1, 6):
        CHECK_POINTS.append(scale_image(pygame.image.load(f"imgs/checkPoint({i}).png"), 1))
        CHECK_POINTS_MASK.append(pygame.mask.from_surface(CHECK_POINTS[i-1]))

    RED_CAR = scale_image(pygame.image.load("imgs/car.png"), 0.4 * rate)
    CIRCLE = scale_image(pygame.image.load("imgs/circle.png"), 200 * rate)

    # WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIDTH, HEIGHT = 1000, 925
    print(f"{WIDTH * 20} ,  {HEIGHT * 20}") 
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game!")

    MAIN_FONT = pygame.font.SysFont("comicsans", 44)
    FPS = 60

    run = True
    clock = pygame.time.Clock()
    images = [(TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0)), (CHECK_POINT, (0, 0))]

    player_car = PlayerCar(100, 4, RED_CAR, START_POS)
    game_info = GameInfo()
    check_point = CheckPoint(CHECK_POINTS[current_check_point], CHECK_POINTS_MASK[current_check_point])

    while run:
        clock.tick(FPS)
        x_offset, y_offset = PlayerCar.calculate_offset(player_car, WIDTH, HEIGHT)
        # print(f"x_offset: {x_offset},  y_offset: {y_offset}")
        
        draw(WIN, images, player_car, game_info, x_offset, y_offset, MAIN_FONT, HEIGHT)
        

        if not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        move_player(player_car)
        handle_collision(player_car, game_info, TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION)
        if(check_point.check_point_check(player_car, CHECK_POINTS_MASK[current_check_point])):
            current_check_point += 1
            print(f"current_check_point: {current_check_point}")
            if(current_check_point == 5):
                current_check_point = 0
                
            check_point = CheckPoint(CHECK_POINTS[current_check_point], CHECK_POINTS_MASK[current_check_point])

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()