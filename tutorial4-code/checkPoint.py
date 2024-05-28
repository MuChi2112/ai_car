import utils
import pygame

CHECK_POINTS = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521),(507, 475), (600, 551), (613, 715), (736, 713), (734, 399), (611, 357), (409, 343),(433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]
current_point = 0


class CheckPoint:

    @staticmethod  
    def check_distance(player_car, threshold=50):
        global current_point 
        
        if current_point < len(CHECK_POINTS):
            check_point = CHECK_POINTS[current_point]
            distance = utils.distance(check_point[0], check_point[1], player_car.x , player_car.y)

            target = (player_car.angle + utils.calculate_angle(player_car, check_point) -90)

            if target < 0:
                target *= -1
                target %= 360
                target *= -1
            else:
                target %= 360

            if target < 5 or target > -5:
                target = 0
            else:
                target = 1

            if distance < threshold:
                current_point += 1
                print(f"Reached checkpoint {current_point - 1}")
                return 100, target
            else:
                return 0, target
        else:
            print("All checkpoints reached.")

    @staticmethod
    def draw_current_checkpoint(screen, radius=50):
        global current_point
        if current_point < len(CHECK_POINTS):
            check_point = CHECK_POINTS[current_point]
            # Draw a semi-transparent circle
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)  # Create a surface with alpha channel
            pygame.draw.circle(circle_surface, (128, 128, 128, 204), (radius, radius), radius)  # Gray color with 80% opacity
            screen.blit(circle_surface, (check_point[0] - radius, check_point[1] - radius))

    @staticmethod
    def reset():
        global current_point
        current_point = 0
        print("Current point reset to 0")