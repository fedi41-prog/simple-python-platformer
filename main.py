import sys
import subprocess

from background import Background
from camera import Camera
from chubzik import Chubzik
from cursor import Cursor
from hotbar import BlockHotbar
from textures import TextureManager
from game_config import GameConfig



def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try: 
    import pygame
    from pygame.locals import *
except ImportError:
    install("pygame")
    import pygame
    from pygame.locals import *
    
import textures
from world import World, generate_blocks

BLOCK_SIZE = 16

gc = GameConfig(50
                , BLOCK_SIZE, 1200, 800, False, False)

def main():
    pygame.init()

    #WORLD
    world = World(1000, 1000, gc)
    generate_blocks(world)


    # +++++++++++++++
 
    fps = 60
    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((gc.screen_width, gc.screen_height))



    # TEXTURE LOADING
    tm: TextureManager = TextureManager(gc)
    tm.load_all_texture_packs()

    background = Background(gc)

    player = Chubzik(500*gc.base_tile_size, 1000, gc)
    player.load_textures(tm)

    cursor = Cursor(gc)
    hotbar = BlockHotbar(gc, [1,2,3,4,5,6])

    camera = Camera()

 
    # Game loop.
    while True:
        screen.fill((17, 167, 242))
  
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.MOUSEWHEEL:
                hotbar.on_scroll(event.y)

        # events
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        pressed_buttons = pygame.mouse.get_pressed()

        if pressed_buttons[0]:
            world.placeBlock(cursor.x, cursor.y, 0)
        elif pressed_buttons[2]:
            world.placeBlockIfAir(cursor.x, cursor.y, hotbar.get_block())

        #testing
        if keys[pygame.K_h]:
            gc.hack = not gc.hack
        if keys[pygame.K_o]:
            world.setBlock(player.rect.center[0]//gc.base_tile_size, player.rect.center[1]//gc.base_tile_size, 1)
        if keys[pygame.K_p]:
            camera.update(player.rect.center[0] * gc.render_scale - gc.screen_width / 2, player.rect.center[1] * gc.render_scale - gc.screen_height / 2)

        #update

        player.handle_input(keys)

        player.update(world)
        camera.move_smooth(player.rect.center[0] * gc.render_scale - gc.screen_width / 2,
                           player.rect.center[1] * gc.render_scale - gc.screen_height / 2, 20,
                           gc.render_tile_size*1
                           ,
                           gc.render_tile_size*1
                           )

        cursor.update(player.rect.center, mouse, camera.x, camera.y)

        #camera.update(
        #    player.rect.center[0]*gc.render_scale-width/2,
        #    player.rect.center[1]*gc.render_scale-height/2
        #)

        # Draw.
        #background.render(screen, tm)
        world.render(screen, tm, camera.x, camera.y)
        player.render(screen, tm, camera.x, camera.y)
        cursor.render(screen, tm, camera.x, camera.y)
        hotbar.render(screen, tm)

        # DEBUG
        if gc.debug:

            pygame.draw.rect(screen, (255,0,0),
                               (
                                   0,
                                   0,
                                   gc.px_to_gu(gc.screen_width),  # + gc.screen_width / gc.render_scale / 2,
                                   gc.px_to_gu(gc.screen_height)  # + gc.screen_width / gc.render_scale / 2,
                               ), 2, 2
                               )
    
    
  
        pygame.display.flip()
        fpsClock.tick(fps)

if __name__ == "__main__":
    main()

    