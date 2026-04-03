class GameConfig(object):
    def __init__(self, render_tile_size, base_tile_size, screen_width, screen_height, debug=False, hack=False):
        self.base_tile_size = base_tile_size
        self.render_scale = render_tile_size / base_tile_size
        self.render_tile_size = render_tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.debug = debug
        self.hack = hack

        print(self.base_tile_size, self.render_scale, self.render_tile_size)

    def px_to_block(self, a):
        return round(a / self.render_scale / self.base_tile_size)
    def px_to_gu(self, a):
        return a / self.render_scale
    def gu_to_block(self, a):
        return a // self.base_tile_size
    def gu_to_block_float(self, a):
        return a / self.base_tile_size
    def gu_to_px(self, gu):
        return gu * self.render_scale
    def block_to_px(self, b):
        return b * self.base_tile_size * self.render_scale

    def px_to_block_float(self, p):
        return p / self.base_tile_size / self.render_scale