import pygame

from textures import TextureManager
from game_config import GameConfig
from util import clamp_distance


class Cursor:
    def __init__(self, gc: GameConfig):
        self.gc = gc

        self.x = 0
        self.y = 0

        self.real_x = 0
        self.real_y = 0

        self.player_x = 0
        self.player_y = 0

        self.max_distance = 5

    def render(self, screen, tm:TextureManager, cam_x, cam_y):

        texture = tm.textures[543]

        screen.blit(texture, (
            int((self.x * self.gc.base_tile_size) * self.gc.render_scale - cam_x),
            int((self.y * self.gc.base_tile_size) * self.gc.render_scale - cam_y)
        ))
        if self.gc.debug:
            pygame.draw.circle(screen, (255, 0, 0), (self.gc.block_to_px(self.real_x)-cam_x, self.gc.block_to_px(self.real_y)-cam_y), 5)
            pygame.draw.circle(screen, (255, 0, 0),
                               (self.gc.block_to_px(self.player_x) - cam_x, self.gc.block_to_px(self.player_y) - cam_y),
                               self.gc.block_to_px(self.max_distance), 2
                               )

    def update(self, player_pos, mouse_pos, cam_x, cam_y):
        """

        :param player_pos:
        :param mouse_pos:
        :param cam_y:
        :param cam_x:
        :return:
        """

        self.player_x,self.player_y = self.gc.gu_to_block_float(player_pos[0]), self.gc.gu_to_block_float(player_pos[1])

        self.real_x = self.gc.px_to_block_float(mouse_pos[0]+cam_x)
        self.real_y = self.gc.px_to_block_float(mouse_pos[1]+cam_y)
        self.real_x, self.real_y = clamp_distance((self.real_x, self.real_y), (self.player_x,self.player_y), self.max_distance)
        self.x, self.y = round(self.real_x-0.5), round(self.real_y-0.5)

        print(self.real_x, self.real_y)

