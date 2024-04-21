import pygame
from utils import scale_image, blit_text_center, draw, handle_collision
from playerCar import PlayerCar
from gameInfo import GameInfo

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
    
    

    pygame.font.init()

    TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.1)
    TRACK_BORDER = scale_image(pygame.image.load("imgs/border.png"), 0.1)
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = pygame.transform.rotate(scale_image(pygame.image.load("imgs/finish.png"), 0.6), 42)
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (350, 700)
    START_POS = (374 * 20, 723 * 20)

    RED_CAR = scale_image(pygame.image.load("imgs/car.png"), 0.4)

    # WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIDTH, HEIGHT = 1000, 925
    print(f"{WIDTH * 20} ,  {HEIGHT * 20}") 
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game!")

    MAIN_FONT = pygame.font.SysFont("comicsans", 44)
    FPS = 60

    run = True
    clock = pygame.time.Clock()
    images = [(TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
    player_car = PlayerCar(4, 4, RED_CAR, START_POS)
    game_info = GameInfo()

    while run:
        clock.tick(FPS)
        x_offset, y_offset = PlayerCar.calculate_offset(player_car, WIDTH, HEIGHT)

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

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()