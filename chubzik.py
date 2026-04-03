from time import sleep

import pygame
from pygame.sprite import Sprite


from textures import TextureManager
from game_config import GameConfig
from world import get_colliding_tiles


class Chubzik:
    def __init__(self, x, y, gc:GameConfig):

        self.rect = pygame.Rect(x, y, 16, 16)
        self.gc = gc

        # Bewegung
        self.vel_x = 0
        self.vel_y = 10

        self.direction = -1

        self.speed = 2
        self.dash_speed = 10
        self.max_dash_time = 10
        self.dash_time_left = 0
        self.default_dash_cooldown = 40
        self.dash_cooldown = 0
        self.jump_strength = 7
        self.gravity = 0.5
        self.max_fall = 30

        self.animation_tick = 0

        self.max_jump_increment_time = 7
        self.jump_hold_time = 0

        self.on_ground = False
        self.jumped = False
        self.is_holding_jump = False

        # Rendering
        self.textures = {}
        self.texture_key = "stand"

    def load_textures(self, tm:TextureManager, stand=178, jump=179):
        self.textures["stand"] = tm.textures[stand]
        self.textures["stand-flipped"] = pygame.transform.flip(tm.textures[stand], True, False)
        self.textures["jump"] = tm.textures[jump]
        self.textures["jump-flipped"] = pygame.transform.flip(tm.textures[jump], True, False)


    # -------------------------
    # INPUT
    # -------------------------
    def handle_input(self, keys):
        self.vel_x = 0

        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.direction = -1
        if keys[pygame.K_d]:
            self.vel_x = self.speed
            self.direction = 1

        if self.gc.hack:
            self.vel_y = 0
            if keys[pygame.K_UP]:
                self.vel_y = -self.speed
            if keys[pygame.K_DOWN]:
                self.vel_y = self.speed

            return

        if keys[pygame.K_SPACE]:
            if (not self.is_holding_jump or not self.on_ground) and ((not self.jumped) or 0 < self.jump_hold_time < self.max_jump_increment_time):
                self.vel_y = -self.jump_strength
                self.jump_hold_time += 1
                self.jumped = True
            self.is_holding_jump = True
        else:
            self.is_holding_jump = False
            self.jump_hold_time = 0

        if keys[pygame.K_LSHIFT]:
            self.vel_y += 10

        if keys[pygame.K_e] and (self.dash_cooldown == 0 or self.dash_time_left > 0):
            if self.dash_time_left == 0:
                self.dash_time_left = self.max_dash_time

            self.vel_x += self.dash_speed * self.direction
            self.vel_y = 0

            self.dash_cooldown = self.default_dash_cooldown
            self.dash_time_left -= 1
        else:
            self.dash_time_left = 0



    # -------------------------
    # PHYSIK
    # -------------------------
    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall:
            self.vel_y = self.max_fall



    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, world):
        if self.gc.hack:
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.update_texture()

            return

        self.apply_gravity()

        # X Bewegung
        self.rect.x += self.vel_x
        self.resolve_collisions(world, "x")

        # Y Bewegung
        self.rect.y += self.vel_y
        self.on_ground = False
        self.resolve_collisions(world, "y")

        if self.on_ground and self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        self.update_texture()

    # -------------------------
    # KOLLISION
    # -------------------------
    def resolve_collisions(self, world, axis):
        tiles = get_colliding_tiles(self.rect, world.isSolid, self.gc.base_tile_size)

        for tile in tiles:
            if self.rect.colliderect(tile):
                if axis == "x":
                    if self.vel_x > 0:
                        self.rect.right = tile.left
                    elif self.vel_x < 0:
                        self.rect.left = tile.right
                    self.vel_x = 0

                elif axis == "y":
                    if self.vel_y > 0:
                        self.rect.bottom = tile.top
                        self.on_ground = True
                        self.jumped = False
                    elif self.vel_y < 0:
                        self.rect.top = tile.bottom
                    self.vel_y = 0

    # -------------------------
    # RENDER
    # -------------------------
    def render(self, screen, tm:TextureManager, cam_x, cam_y):

        texture = self.textures[self.texture_key]

        render_rect = texture.get_rect()
        render_rect.midbottom = (self.rect.midbottom[0] * self.gc.render_scale, self.rect.midbottom[1] * self.gc.render_scale)


        screen.blit(
            texture,
            (render_rect.x - cam_x, render_rect.y - cam_y)
        )

        #if self.gc.debug:
        #    pygame.draw.rect(
        #        screen,
        #        (255, 0, 0),
        #        pygame.Rect(
        #            self.gc.px_to_gu(cam_x) - self.rect.x,
        #            self.gc.px_to_gu(cam_y) - self.rect.y,
        #            self.rect.width,
        #            self.rect.height
        #        )
        #    )

    def update_texture(self):
        if self.on_ground:
            if self.vel_x != 0:
                self.animation_tick += 1
                if self.animation_tick == 5:
                    self.animation_tick = 0
                    if self.texture_key.startswith("stand"): self.texture_key = "jump"
                    else: self.texture_key = "stand"
            else:
                self.texture_key = "stand"
                self.animation_tick = 0
        else:
            self.texture_key = "jump"


        if self.direction == 1:
            if self.texture_key == "stand": self.texture_key = "stand-flipped"
            if self.texture_key == "jump": self.texture_key = "jump-flipped"
        #else:
        #    if self.texture_key == "stand-flipped": self.texture_key = "stand"
        #    if self.texture_key == "jump-flipped": self.texture_key = "jump"




