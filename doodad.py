import libtcodpy as libtcod

class Doodad(object):
    def __init__(self, x, y, colors=None, tileSize=1):
        self.x = x
        self.y = y
        self.character = None
        self.tileSize = tileSize
        if colors is not None:
            self.color = colors[libtcod.random_get_int(0,0, len(colors) - 1)] 
    def draw(self, con, theMap, blocks, blockSight):
        tileSize = None
        if self.tileSize != 1:
            tileSize = self.tileSize / 2
        else:
            tileSize = self.tileSize
        for x in range(tileSize):
            for y in range(tileSize):
                if self.x + x > theMap.x2 - 1 or self.y + y > theMap.y2 - 1:
                    continue
                if libtcod.map_is_in_fov(theMap.fovMap, self.x + x, self.y + y):
                    libtcod.console_set_default_foreground(con, self.color)
                    libtcod.console_put_char(con, self.x + x, self.y + y, self.character, libtcod.BKGND_NONE)


class Grass(Doodad):

    def __init__(self, x, y, tileSize=1):
        colors = [libtcod.light_green, libtcod.lighter_green, libtcod.light_yellow, libtcod.lighter_yellow]
        self.deadColor = libtcod.gray
        self.tileSize = tileSize
        super(Grass, self).__init__(x, y, colors=colors, tileSize=self.tileSize)
        self.character = '\''
        self.blocks = False
        self.blockSight = False

    def draw(self, con, fovMap=None):
        super(Grass, self).draw(con, fovMap, self.blocks, self.blockSight)

class Tree(Doodad):

    def __init__(self, x, y, tileSize=4):
        colors = [libtcod.dark_amber, libtcod.dark_green, libtcod.dark_lime]
        self.deadColor = libtcod.gray
        self.tileSize = tileSize
        super(Tree, self).__init__(x, y, colors=colors, tileSize=self.tileSize)
        self.blocks = True
        self.blockSight = True
        self.character = 'O'

    def draw(self, con, theMap):
        super(Tree, self).draw(con, theMap, self.blocks, self.blockSight)

class Lake(Doodad):

    def __init__(self, x, y):
        colors = [libtcod.blue]
        self.tileSize = libtcod.random_get_int(0, 4, 8)
        super(Lake, self).__init__(x, y, colors=colors, tileSize=self.tileSize)
        self.blockSight = False
        self.blocks = True
        self.character = '~'

    def draw(self, con, theMap):
        super(Lake, self).draw(con, theMap, self.blocks, self.blockSight)
