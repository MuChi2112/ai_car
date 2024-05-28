import math

class CheckPoint():
    def __init__(self, current_check_point, check_point_mask):
        IMG = current_check_point
        self.x, self.y = self.calculate_mask_position(check_point_mask)
        self.counter = 0
        self.touch_once = False

    def calculate_mask_position(self, mask):
        bounding_rects = mask.get_bounding_rects()
        if bounding_rects:

            min_x, min_y, max_x, max_y = bounding_rects[0]
        else:
            # 处理没有发现边界框的情况，例如可以设置为默认值或者跳过当前的处理步骤
            min_x, min_y, max_x, max_y = 0, 0, 0, 0  # 例如，设置为默认值
            print("nothing")
            # 或者可以使用 continue 或 return 来跳过后续代码

        x = (min_x+max_x)/2
        y = (min_y+max_y)/2
        print(f"x:{x}, y: {y}")
        return x, y
    
    def calculate_check_point_distance(self, car_x, car_y):
        return math.sqrt((car_x - self.x)**2 + (car_y - self.y)**2)
    
    def relativelyPoint(self, car_x, car_y):
        temp_list = []
        if (car_x - self.x) > 0:
            temp_list.append(0)
        else:
            temp_list.append(1)

        if (car_y - self.y) > 0:
            temp_list.append(0)
        else:
            temp_list.append(1)
        
        return temp_list

    def check_point_check(self, player_car, check_point_mask):
        collision_point = player_car.collide(check_point_mask, 0, 0)

        if collision_point is None and self.touch_once is False:
            return False
        
        if collision_point is not None and self.touch_once is False:
            self.touch_once = True
            return False
        
        if collision_point is  None and self.touch_once is True:
            self.counter += 1
            print(f"check point {self.counter}")
            self.touch_once = False
            return True

    def draw(self, win, current_check_point):
        win.blit([current_check_point], (0, 0))