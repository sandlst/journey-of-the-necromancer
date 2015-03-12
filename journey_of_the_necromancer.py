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
#DARK_FLOOR = libtcod.Color(50, 50, 150)
DARK_FLOOR = libtcod.Color(70,70,70)
#LIGHT_FLOOR = libtcod.Color(200, 180, 50)
LIGHT_FLOOR = libtcod.Color(0, 0, 0)

#Monster Generator File
MAX_MONSTER_LEVEL = 3
LINES_PER_MONSTER = 10
MONSTER_FILE = "monsters.data"

class MonsterGenerator:

    def __init__(self):
        # load monsters from monster file
        currentMonster = {}
        self.loadedMonsters = []
        currentMonsterIndex = 0

        with open(MONSTER_FILE) as f:
            for line in f:
                if currentMonsterIndex == 0:
                    currentMonster['Name'] = line.strip()
                elif currentMonsterIndex == 1:
                    currentMonster['Character'] = line.strip()
                elif currentMonsterIndex == 2:
                    currentMonster['Color'] = line.strip()
                elif currentMonsterIndex == 3:
                    currentMonster['Level'] = line.strip()
                elif currentMonsterIndex == 4:
                    currentMonster['Strength'] = line.strip()
                elif currentMonsterIndex == 5:
                    currentMonster['Dex'] = line.strip()
                elif currentMonsterIndex == 6:
                    currentMonster['Con'] = line.strip()
                elif currentMonsterIndex == 7:
                    currentMonster['Int'] = line.strip()
                elif currentMonsterIndex == 8:
                    currentMonster['Wis'] = line.strip()
                elif currentMonsterIndex == 9:
                    currentMonster['Cha'] = line.strip()
                elif currentMonsterIndex == 10:
                    currentMonster['AI'] = line.strip()
                else:
                    self.loadedMonsters.append(currentMonster)
                    currentMonsterIndex = 0
                    currentMonster = {}
                    continue
                currentMonsterIndex = currentMonsterIndex + 1

    def loadMonster(self, level):
        targetMonsters = []
        for monster in self.loadedMonsters:
            if monster['Level'] == level:
                targetMonsters.append(monster)

        if len(targetMonsters) == 0:
            return None

        else:
            selectedMonster = targetMonsters[libtcod.random_get_int(0,0, len(targetMonsters) - 1)]
            return creature.Creature(selectedMonster['Name'], 0, 0, selectedMonster['Character'], eval(selectedMonster['Color']), monster=True, ai=eval('creature.'+selectedMonster['AI']+'(currentMap)'))


###
# renderAll() - draws characters to the screen
###
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
    for creature in deadCreatures:
        if libtcod.map_is_in_fov(currentMap.fovMap, creature.x, creature.y):
                libtcod.console_set_default_foreground(con, creature.color)
                libtcod.console_put_char(con, creature.x, creature.y, creature.character, libtcod.BKGND_NONE)
    for creature in creatures:
        if libtcod.map_is_in_fov(currentMap.fovMap, creature.x, creature.y):
                libtcod.console_set_default_foreground(con, creature.color)
                libtcod.console_put_char(con, creature.x, creature.y, creature.character, libtcod.BKGND_NONE)

    libtcod.console_blit(con, 0, 0, currentMap.x2, currentMap.y2, 0, 0, 0)

def handleKeys():
    global player, fovRecompute
    key = libtcod.console_wait_for_keypress(True)

    #special keys
    if libtcod.console_is_key_pressed(libtcod.KEY_ESCAPE):
        return 'exit'
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        if player.moveOrAttack(0, -1, currentMap):
            fovRecompute = True
        else:
            return
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        if player.moveOrAttack(0, 1, currentMap):
            fovRecompute = True
        else:
            return
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        if player.moveOrAttack(-1, 0, currentMap):
            fovRecompute = True
        else:
            return
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        if player.moveOrAttack(1, 0, currentMap):
            fovRecompute = True
        else:
            return
    else:
        return 'didnt-take-turn'
    
    for theCreature in creatures:
        if theCreature == player:
            continue
        else:
            theCreature.ai.takeTurn(theCreature.lookAround(creatures))
            if theCreature.isDead:
                creatures.remove(theCreature)
                deadCreatures.append(theCreature)
def newMap(level):
    currentMap = Map.Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    playerPlaced = False
    for x in range(currentMap.x2):
        for y in range(currentMap.y2):
            if currentMap.theMap[x][y].blocked:
                continue
            else:
                player.x = x
                player.y = y
                playerPlaced = True
                break
        if playerPlaced:
            break
# main

#create console
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Journey of the Necromancer', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
#create first map
currentMap = Map.Map(SCREEN_WIDTH, SCREEN_HEIGHT)
#load monsters from file
monsterGenerator = MonsterGenerator()
#some debug creatures and items
sword = item.Weapon("sword", 's', 1, 6)
player = creature.Creature("player", 0,0, '@', libtcod.white, hp=20)
player.weapon = sword
#npc = creature.Creature("Toad", 3,2, 'T', libtcod.green, monster=True, hp=20)
npc = monsterGenerator.loadMonster('1')
npc.x = 3
npc.y = 3
npc.makeHostile(player)
npc.weapon = item.Weapon('handaxe', 'a', 1, 6)
player.makeHostile(npc)
newMap(0)
#list of all creatures in the current map
creatures = [player]
creatures.append(npc)
#list of all dead creatures in the current map
deadCreatures = []
fovRecompute = True
playerAction = None

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(con, libtcod.white)
    renderAll()
    libtcod.console_flush()
    for creature in creatures:
        libtcod.console_put_char(con, creature.x, creature.y, ' ', libtcod.BKGND_NONE)
    playerAction = handleKeys()
    if playerAction == 'exit':
        break
    if player.isDead:
        print "GAME OVER!"
        break
