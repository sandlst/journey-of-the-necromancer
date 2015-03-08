import libtcodpy as libtcod
import map as Map
import item
import creature

#SCREEN CONSTANTS
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 60

#FOV Constants
FOV_ALGO = 0 #default defined in libtcod
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

#Tile Colors
DARK_WALL = libtcod.Color(0, 0, 100)
LIGHT_WALL = libtcod.Color(130, 110, 50)
DARK_FLOOR = libtcod.Color(50, 50, 150)
LIGHT_FLOOR = libtcod.Color(200, 180, 50)

def renderAll():
    global fovMap, fovRecompute
    if fovRecompute:
        fovRecompute = False;
        libtcod.map_compute_fov(fovMap, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
    for y in range(currentMap.y2):
        for x in range(currentMap.x2):
            visible = libtcod.map_is_in_fov(fovMap,x,y)
            wall = currentMap.theMap[x][y].block_sight
            if not visible:
                #outside the player's fov
                if currentMap.theMap[x][y].explored == True:
                    wall = currentMap.theMap[x][y].block_sight
                    if wall:
                        libtcod.console_set_char_background(con, x, y, DARK_WALL, libtcod.BKGND_SET) 
                    else:
                        libtcod.console_set_char_background(con, x, y, DARK_FLOOR, libtcod.BKGND_SET) 
            else:
                #tile is visible
                if wall:
                    libtcod.console_set_char_background(con, x, y, LIGHT_WALL, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, LIGHT_FLOOR, libtcod.BKGND_SET)
                currentMap.theMap[x][y].explored = True
    for creature in creatures:
        if libtcod.map_is_in_fov(fovMap, creature.x, creature.y):
                libtcod.console_set_default_foreground(con, creature.color)
                libtcod.console_put_char(con, creature.x, creature.y, creature.character, libtcod.BKGND_NONE)
    libtcod.console_blit(con, 0, 0, currentMap.x2, currentMap.y2, 0, 0, 0)

def handleKeys():
    global player, fovRecompute
    key = libtcod.console_wait_for_keypress(True)

    #special keys
    if key.vk == libtcod.KEY_ESCAPE:
        return 'exit'
    #movement keys
    if key.vk == libtcod.KEY_UP:
        player.move(0, -1)
        fovRecompute = True
    if key.vk == libtcod.KEY_DOWN:
        player.move(0, 1)
        fovRecompute = True
    if key.vk == libtcod.KEY_LEFT:
        player.move(-1, 0)
        fovRecompute = True
    if key.vk == libtcod.KEY_RIGHT:
        player.move(1, 0)
        fovRecompute = True
# main

#create console
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Journey of the Necromancer', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
#create first map
currentMap = Map.Map(SCREEN_WIDTH, SCREEN_HEIGHT)
#some debug creatures and items
sword = item.Weapon("sword", 's', 1, 6)
player = creature.Creature("player", 0,0, '@', libtcod.white)
npc = creature.Creature("Toad", 0,1, 'T', libtcod.green, monster=True, hp=20)
#list of all creatures in the current map
creatures = [player]
creatures.append(npc)
#create FOV map
#TODO: move to map.py
fovMap = libtcod.map_new(SCREEN_WIDTH, SCREEN_HEIGHT)
for y in range(SCREEN_HEIGHT):
    for x in range(SCREEN_WIDTH):
        libtcod.map_set_properties(fovMap, x, y, not currentMap.theMap[x][y].block_sight, not currentMap.theMap[x][y].blocked)
fovRecompute = True

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(con, libtcod.white)
    renderAll()
    libtcod.console_flush()
    for creature in creatures:
        libtcod.console_put_char(con, creature.x, creature.y, ' ', libtcod.BKGND_NONE)
    playerAction = handleKeys()
    if playerAction == 'exit':
        break
