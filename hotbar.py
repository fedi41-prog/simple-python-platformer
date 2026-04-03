import pygame

from blocks import BLOCKS
from game_config import GameConfig
from textures import TextureManager


class BlockHotbar:
    def __init__(self, gc:GameConfig, block_types:list[int]):
        self.block_types = block_types
        self.index = 0

        self.gc = gc

    def get_block(self):
        return self.block_types[self.index]

    def on_scroll(self, direction):
        self.index += direction
        self.index %= len(self.block_types)

    def render(self, screen, tm:TextureManager):

        block = self.block_types[self.index]
        texture = pygame.transform.scale_by(tm.textures[BLOCKS[block].texture], 1.5    )

        texture_rect = texture.get_rect()
        texture_rect.center = (self.gc.screen_width/2, self.gc.screen_height - texture_rect.height)

        screen.blit(
            texture,
            (texture_rect.x, texture_rect.y)
        )