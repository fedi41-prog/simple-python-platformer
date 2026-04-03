import json
import os
import pygame

from game_config import GameConfig


def load_img(path:str, scale:float, convert_to_alpha=True):
    img = pygame.image.load(path)
    if convert_to_alpha: img = img.convert_alpha()
    img = pygame.transform.scale_by(img, scale)
    return img


class TextureManager:
    def __init__(self, gc:GameConfig):
        self.textures:dict[int,pygame.Surface] = {}
        self.gc = gc

    def load_all_texture_packs(self, texture_packs_config: str = "texturepacks.json"):
        with open(texture_packs_config, "r") as f:
            texture_packs = json.load(f)["texturepacks"]

        for t in texture_packs:
            folder = t["folder"]
            tile_size = t["tile_size"]
            print(folder, tile_size)

            scale = self.gc.render_tile_size / tile_size

            self.load_texture_pack(folder, scale)


    def load_texture_pack(self, folder:str, scale:float):
        files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for f in files:
            i = int(f[:4])
            self.textures[i] = load_img(os.path.join(folder, f), scale)
            #print(f"loading texture ({i} : {f} : {self.textures[i].get_size()})")



if __name__ == "__main__":
    tm:TextureManager = TextureManager()
    tm.load_all_texture_packs()

