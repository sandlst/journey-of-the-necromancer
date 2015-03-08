import libtcodpy as libtcod
class Map:

    def __init__(self, width, height):
        self.x1 = 0
        self.y1 = 0
        self.x2 = width
        self.y2 = height
        self.houses = [None]
        self.theMap = [[ Tile(False) for y in range(self.y2)] for x in range(self.x2)]
        for y in range (self.y2):
            self.theMap[self.x1][y].blocked = True
            self.theMap[self.x2 - 1][y].blocked = True
        for x in range (self.x2):
            self.theMap[x][self.y1].blocked = True
            self.theMap[x][self.y2 - 1].blocked = True

        self.fovMap = libtcod.map_new(width, height)
        for y in range(height):
            for x in range(width):
                libtcod.map_set_properties(self.fovMap, x, y, not self.theMap[x][y].block_sight, not self.theMap[x][y].blocked)


    def placeHouse(self, inhabitants):
        #each 'person' who is in the house gets at least a 3x3 area, as much as 6x6 
        while(True):
            house_x1 = libtcod.random_get_int(0, self.x1, self.x2)
            house_y1 = libtcod.random_get_int(0, self.y1, self.y2)
            house_length = libtcod.random_get_int(0, 3 * inhabitants, 6 * inhabitants)
            house_width = libtcod.random_get_int(0, 3 * inhabitants, 6 * inhabitants)
            blocked = False
            if house_x1 + house_length > self.x2:
                continue
            if house_y1 + house_width > self.y2:
                continue
            for x in range(house_x1, house_x1 + house_length):
                if theMap[x][house_y1].blocked or theMap[x][house_y1 + house_width].blocked:
                    blocked = True
                    break
            if blocked:
                continue
            for y in range(house_y1, house_y1 + house.width):
                if theMap[house_x1][y].blocked or theMap[house_x1 + house_length][y].blocked:
                    blocked = True
                    break
            if blocked:
                continue

        self.houses.append(House(house_x1, house_y1, house_length, house_width))
        for x in range(house_x1, house_x1 + house_length):
            theMap[x][house_y1].blocked = True
            theMap[x][house_y1 + house_width].blocked = True
        for y in range(house_y1, house_y1 + house.width):
            theMap[house_x1][y].blocked = True
            theMap[house_x1+ house_length][y].blocked = True

    def fovRecompute(self, playerX, playerY, torchRadius, lightWalls, fovAlgo):
        libtcod.map_compute_fov(self.fovMap, playerX, playerY, torchRadius, lightWalls, fovAlgo)

class House:
    
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def createDoor(x, y):
        pass

    def getDimensions(self):
        return {
                'x1': self.x1,
                'x2': self.x2,
                'y1': self.y1,
                'y2': self.y2
                }


class Tile:

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        if blocked:
            self.block_sight = True
        else:
            self.block_sight = block_sight
        self.explored = False
        
