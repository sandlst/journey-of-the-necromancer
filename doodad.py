import libtcodpy as libtcod

class Doodad(object):
    def __init__(self, x, y, colors=None, tileSize=1, blocks=True):
        self.x = x
        self.y = y
        self.blocks = blocks
        self.blockSight = blocks
        self.character = None
        if self.colors is not None:
            self.color = colors[libtcod.random_get_int(0,0, len(colors) - 1)] 
    def draw(self, con, fovMap=None):
        if fovMap == None:
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.character, libtcod.BKGND_NONE)
        else:
            if libtcod.map_is_in_fov(fovMap, self.x, self.y):
                libtcod.console_set_default_foreground(con, self.color)
                libtcod.console_put_char(con, self.x, self.y, self.character, libtcod.BKGND_NONE)


class Grass(Doodad):

    def __init__(self, x, y, tileSize=1, blocks=True):
        self.colors = [libtcod.light_green, libtcod.lighter_green, libtcod.light_yellow, libtcod.lighter_yellow]
        self.deadColor = libtcod.gray
        super(Grass, self).__init__(x, y, colors=self.colors, tileSize=tileSize, blocks=blocks)
        self.character = '\''

    def draw(self, con, fovMap=None):
        super(Grass, self).draw(con, fovMap)

class Tree(Doodad):

    def __init__(self, x, y, tileSize=4, blocks=False):
        self.colors = [libtcod.dark_amber, libtcod.dark_green, libtcod.dark_lime]
        self.deadColor = lilbtcod.gray
        self.character = 'O'
        super(Tree, self).__init__(x, y, colors=self.colors, tileSize=tileSize, blocks=blocks)

    def draw(self, con, fovMap=None):
        super(Tree, self).draw(con, fovMap)

class Lake(Doodad):

    def __init__(self, x, y, blocks=True):
        self.colors = {libtcod.blue}
        tileSize = libtcod.random_get_int(0, 4, 8)
        character = '~'
        super(Lake, self).__init__(x, y, colors=self.colors, tileSize=tileSize, blocks=blocks)
        self.blockSight = False

    def draw(self, con, fovMap=None):
        super(Lake, self).draw(con, fovMap)
