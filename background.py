from textures import TextureManager, GameConfig


class Background:
    def __init__(self, gc: GameConfig):
        self.textures = [0, 9, 16]
        self.gc = gc

    def render(self, screen, tm:TextureManager):
        texture_top = tm.textures[self.textures[0]]
        texture_middle = tm.textures[self.textures[1]]
        texture_bottom = tm.textures[self.textures[2]]

        width, height = texture_top.get_size()

        w, h = self.gc.screen_width % width, self.gc.screen_height % height

        for y in range(h+1):
            for x in range(w+1):
                screen.blit(
                    texture_top,
                    (x*width,y*height)
                )

