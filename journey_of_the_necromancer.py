import libtcodpy as libtcod
import map as Map
import doodad
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
#LIGHT_FLOOR = libtcod.Color(200, 180, 50)
LIGHT_FLOOR = libtcod.Color(0, 0, 0)

def renderAll():
    global fovRecompute
    if fovRecompute:
        fovRecompute = False;
        currentMap.fovRecompute(player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
    for y in range(currentMap.y2):
        for x in range(currentMap.x2):
            visible = libtcod.map_is_in_fov(currentMap.fovMap,x,y)
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
    for theDoodad in currentMap.doodads:
        theDoodad.draw(con, currentMap)
    for creature in creatures:
        if libtcod.map_is_in_fov(currentMap.fovMap, creature.x, creature.y):
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
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        if moveOrAttack(0, -1, player):
            fovRecompute = True
        else:
            return
    if libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        if moveOrAttack(0, 1, player):
            fovRecompute = True
        else:
            return
    if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        if moveOrAttack(-1, 0, player):
            fovRecompute = True
        else:
            return
    if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        if moveOrAttack(1, 0, player):
            fovRecompute = True
        else:
            return

def moveOrAttack(dx, dy, creature):
    if currentMap.theMap[player.x + dx][player.y + dy].blocked:
        return False
    for otherCreature in creatures:
        if not otherCreature.blocks:
            break
        if otherCreature.x == creature.x + dx and otherCreature.y == creature.y + dy:
            if creature.isHostile(otherCreature):
                #TODO: use actual weapon instead of placeholder
                creature.attack(otherCreature, sword)
                return True
            else:
                #TODO: present confirmation dialog for attacking neutral creature
                #for the player
                return False

    creature.move(dx, dy)
    return True
# main

#create console
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Journey of the Necromancer', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
#create first map
currentMap = Map.Map(SCREEN_WIDTH, SCREEN_HEIGHT)
#some debug creatures and items
sword = item.Weapon("sword", 's', 1, 6)
playerPlaced = False
for x in range(currentMap.x2):
    for y in range(currentMap.y2):
        if currentMap.theMap[x][y].blocked:
            continue
        else:
            player = creature.Creature("player", x,y, '@', libtcod.white)
            playerPlaced = True
            break
    if playerPlaced:
        break

npc = creature.Creature("Toad", 3,2, 'T', libtcod.green, monster=True, hp=20)
player.makeHostile(npc)
#list of all creatures in the current map
creatures = [player]
creatures.append(npc)
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
