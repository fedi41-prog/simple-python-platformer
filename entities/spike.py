from textures import GameConfig


class Spike(Entity):


    def __init__(self, x, y, gc):
        self.x = x
        self.y = y
        self.gc = gc


    def on_player_collide(self):


