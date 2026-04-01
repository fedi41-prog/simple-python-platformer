from util import normalize


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, x, y):
        self.x = x
        self.y = y

    def move_smooth(self, x, y, speed, x_range, y_range):
        #dx, dy = normalize(x - self.x,  y - self.y)
#
        #self.x += dx * speed
        #self.y += dy * speed
        dx, dy = x-self.x, y-self.y
        if abs(dx) > x_range:
            self.x += dx / speed
        if abs(dy) > y_range:
            self.y += dy / speed

