class BlockType:
    def __init__(self,
                 name:str,
                 texture:int|None,
                 #TAGS
                 solid: bool = True,
                 rect_collide: bool = True,
                 visible: bool = True,
                 #OTHER
                 texture_mode:str = "normal", # connect | function | function4
                 #TEXTURES
                 texture_map: dict[int, int] = None,
                 corner_textures: dict[str, int] = None,
                 texture_function = None,
                 connects_to=None
                 ):

        if connects_to is None:
            connects_to = []
        self.solid = solid
        self.rect_collide = rect_collide
        self.visible = visible

        self.texture_mode = texture_mode
        self.texture_map = texture_map
        self.corner_textures = corner_textures
        self.texture_function = texture_function
        self.connects_to = connects_to

        self.name = name
        self.texture = texture
def water_texture(t, r, b, l, a):
    if not t:
        return 57 if a<8 else 74
    return 94


#0  = allein                                    0
#1  = oben
#2  = rechts                                    2
#3  = oben + rechts
#4  = unten                                     4
#5  = oben + unten
#6  = rechts + unten                            6
#7  = oben + rechts + unten
#8  = links                                     8
#9  = oben + links
#10 = links + rechts                            10
#11 = oben + links + rechts
#12 = unten + links                             12
#13 = oben + unten + links
#14 = unten + links + rechts                    14
#15 = alle Seiten

#tl, tr, bl, br

BLOCKS = {
    0: BlockType("air", None, solid=False, visible=False),  # Air
    1: BlockType(
        "grass_block",
        24,
        texture_mode="connect",
        texture_map=
    {
        0: 24,
        1: 161,
        2: 25,
        3: 162,
        4: 44,
        5: 141,
        6: 45,
        7: 142,
        8: 27,
        9: 164,
        10: 26,
        11: 163,
        12: 47,
        13: 144,
        14: 46,
        15: 143
    },
        corner_textures=
    {
        "tl": 49,
        "tr": 48,
        "bl": 29,
        "br": 28
    },
        connects_to=["desert_grass_block"]
                 ),
    2: BlockType(
        "desert_grass_block",
        64,
        texture_mode="connect",
        texture_map=
    {
        0: 64,
        1: 161,
        2: 65,
        3: 162,
        4: 81,
        5: 141,
        6: 82,
        7: 142,
        8: 67,
        9: 164,
        10: 66,
        11: 163,
        12: 84,
        13: 144,
        14: 83,
        15: 143
    },
        corner_textures=
    {
        "tl": 49,
        "tr": 48,
        "bl": 29,
        "br": 28
    },
        connects_to=["grass_block"]
                 ),
    3: BlockType(
        "water",
        145,
        solid=False,
        texture_mode="function4-animated",
        texture_function=water_texture
    )
}

