import math

from blocks import BLOCKS


def normalize(x, y):
    length = math.sqrt(x * x + y * y)

    if length == 0:
        return (0, 0)  # oder Fehler werfen, je nach use-case

    return (x / length, y / length)

def get_mask4(up, right, down, left):
    """
    für die 4 Nachbarn, gibt ein texture id aus
    """

    mask = 0
    if up:    mask |= 1   # 0001
    if right: mask |= 2   # 0010
    if down:  mask |= 4   # 0100
    if left:  mask |= 8   # 1000

    return mask

def can_connect(block_type1:int, block_type2:int):
    if block_type1 == block_type2: return True
    if BLOCKS[block_type1].name in BLOCKS[block_type2].connects_to or BLOCKS[block_type2].name in BLOCKS[block_type1].connects_to:
        return True
    return False

def get_neighbors8(world, x, y, block_type):
    def same(nx, ny):
        return (
            0 <= ny < len(world[0]) and
            0 <= nx < len(world) and
            can_connect(block_type, world[nx][ny])
        )

    t  = same(x, y-1)
    r  = same(x+1, y)
    b  = same(x, y+1)
    l  = same(x-1, y)

    # 🔥 diagonalen nur wenn beide seiten da sind
    tl = same(x-1, y-1) if t and l else False
    tr = same(x+1, y-1) if t and r else False
    bl = same(x-1, y+1) if b and l else False
    br = same(x+1, y+1) if b and r else False

    return t, r, b, l, tl, tr, bl, br

