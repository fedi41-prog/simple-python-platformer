import pygame

from textures import TextureManager, GameConfig


class Cursor:
    def __init__(self, gc: GameConfig):
        self.gc = gc

        self.x = 0
        self.y = 0

        self.real_x = 0
        self.real_y = 0

        self.max_distance = 5

    def render(self, screen, tm:TextureManager, cam_x, cam_y):

        texture = tm.textures[543]

        screen.blit(texture, (
            int((self.x * self.gc.base_tile_size) * self.gc.render_scale - cam_x),
            int((self.y * self.gc.base_tile_size) * self.gc.render_scale - cam_y)
        ))
        if self.gc.debug:
            pygame.draw.circle(screen, (255, 0, 0), (self.real_x-cam_x, self.real_y-cam_y), 5)

    def update(self, player_pos, mouse_pos, cam_x, cam_y):
        """

        :param player_pos:
        :param mouse_pos:
        :param cam_y:
        :param cam_x:
        :return:
        """


        self.real_x = mouse_pos[0]+cam_x
        self.real_y = mouse_pos[1]+cam_y
        self.x, self.y = self.gc.px_to_block(self.real_x-self.gc.base_tile_size), self.gc.px_to_block(self.real_y-self.gc.base_tile_size)

        print(self.x, self.y)

