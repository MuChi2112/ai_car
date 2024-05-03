

class CheckPoint():
    def __init__(self, CHECK_POINT):
        IMG = CHECK_POINT
        self.counter = 0
        self.touch_once = False

    def check_point_check(self, player_car, check_point_mask):
        collision_point = player_car.collide(check_point_mask, 0, 0)

        if collision_point is None and self.touch_once is False:
            return
        
        if collision_point is not None and self.touch_once is False:
            self.touch_once = True
            return
        
        if collision_point is  None and self.touch_once is True:
            self.counter += 1
            print(f"check point {self.counter}")
            self.touch_once = False
            return
