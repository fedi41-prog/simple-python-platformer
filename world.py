import random
from multiprocessing.pool import worker

import pygame

from blocks import BLOCKS
from textures import TextureManager, GameConfig
from util import get_neighbors8, get_mask4


class WorldLayer:
    def __init__(self):
        None

class World:
    def __init__(self, height:int, width:int, gc:GameConfig):
        self.blocks: list[list[int]] = [[0 for _ in range(height)] for _ in range(width)]
        self.height = height
        self.width  = width
        self.gc = gc

        self.block_animation_tick = 0
        
    def render(self,
                screen,
                tm: TextureManager,
                cam_x, cam_y,
        ):


        start_x = max(self.gc.px_to_block(cam_x)-1, 0)
        start_y = max(self.gc.px_to_block(cam_y)-1, 0)
        end_x = min(self.width, start_x + self.gc.px_to_block(self.gc.screen_width) + 2)
        end_y = min(self.height, start_y + self.gc.px_to_block(self.gc.screen_height) + 2)


        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):

                block_type = BLOCKS[self.blocks[x][y]]
                if not block_type.visible: continue
                texture = block_type.texture

                if block_type.texture_mode == "connect":
                    t, r, b, l, tl, tr, bl, br = get_neighbors8(self.blocks, x, y, self.blocks[x][y])
                    mask = get_mask4(t, r, b, l)

                    if mask != 15: texture = block_type.texture_map[mask]
                    elif not tl: texture = block_type.corner_textures["tl"]
                    elif not tr: texture = block_type.corner_textures["tr"]
                    elif not bl: texture = block_type.corner_textures["bl"]
                    elif not br: texture = block_type.corner_textures["br"]
                    else: texture = block_type.texture_map[15]
                if block_type.texture_mode == "function4-animated":
                    t, r, b, l, tl, tr, bl, br = get_neighbors8(self.blocks, x, y, self.blocks[x][y])
                    texture = block_type.texture_function(t, r, b, l, self.block_animation_tick)

                screen.blit(
                    tm.textures[texture],
                    (
                        int((x * self.gc.base_tile_size) * self.gc.render_scale - cam_x),
                        int((y * self.gc.base_tile_size) * self.gc.render_scale - cam_y)
                    )
                )
                if self.gc.debug:
                    pygame.draw.rect(
                        screen,
                        (0,255,0),
                        pygame.Rect(
                            (x-start_x)*self.gc.base_tile_size,
                            (y-start_y)*self.gc.base_tile_size,
                            self.gc.base_tile_size,
                            self.gc.base_tile_size
                        )
                    )

        self.block_animation_tick += 1
        if self.block_animation_tick == 16: self.block_animation_tick = 0
            
    def setBlock(self,x:int,y:int,block_id:int):
        if x >= self.width or x < 0 or y < 0 or y >= self.height: return
        self.blocks[x][y] = block_id
    def isSolid(self, x:int, y:int):
        if x >= self.width or x < 0 or y < 0 or y >= self.height: return False
        return BLOCKS[self.blocks[x][y]].solid

def generate_blocks(world):

    h = world.height - world.height // 8
    for x in range(world.width):
        for y in range(0, world.height):
            if y >= h:
                world.setBlock(x, y, random.choice([1,2]))
            elif y > world.height // 2:
                world.setBlock(x, y, 3)
        h += random.randint(-3, 3)
        if h > world.height: h = world.height
        if h < 0: h = 0






def get_colliding_tiles(rect, is_solid, block_size):
    tiles = []

    x1 = rect.left // block_size
    x2 = rect.right // block_size
    y1 = rect.top // block_size
    y2 = rect.bottom // block_size

    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if is_solid(x, y):
                tiles.append(pygame.Rect(
                    x * block_size,
                    y * block_size,
                    block_size,
                    block_size
                ))
    return tiles
