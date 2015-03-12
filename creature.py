import libtcodpy as libtcod
import math

DEAD_COLOR = libtcod.light_grey

class Creature:


    def __init__(self, name, x, y, character, color, monster=False, ai=None, stats=None, hp=1, sightRadius=5, attackRange=1, armorClass=10):
        self.name = name
        self.x = x
        self.y = y
        self.character = character
        self.color = color
        self.monster = monster
        self.ai = ai
        self.blocks = True
        self.isDead = False
        if self.ai:
            self.ai.owner = self
        self.stats = stats
        if self.stats:
            self.stats.owner = self
            self.hp = hp + self.stats.getConBonus() 
            self.armorClass = self.armorClass+self.stats.getDexBonus()
        else:
            self.stats = Stats()
            self.stats.owner = self
            self.hp = hp
            self.armorClass = armorClass
        self.sightRadius = sightRadius
        self.attackRange = attackRange
        self.hostileList = []
        self.weapon = None
    ###
    # setName
    ###
    def setName(self, newName):
        self.name = newName

    ###
    # moveOrAttack 
    ###
    def moveOrAttack(self, dx, dy, theMap):
        if theMap.theMap[self.x + dx][self.y + dy].blocked:
            return False
        else:
            for creature in self.hostileList:
                if creature.x == self.x + dx and creature.y == self.y + dy and not creature.isDead:
                    self.attack(creature, self.weapon)
                    return True
            self.x = self.x + dx
            self.y = self.y + dy
            return True

    ###
    # chase - move towards something
    ###
    def chase(self, target_x, target_y, theMap):
        dx = target_x - self.x
        dy = target_y - self.y
        #vector to find distance
        distance = math.sqrt(dx ** 2 + dy ** 2)
        #normalize, then round and convert
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.moveOrAttack(dx, dy, theMap)

    ###
    # isHostile - determines if the creature is hostile to another creature
    ###
    def isHostile(self, other):
        for creature in self.hostileList:
            if creature.name == other.name:
                return True
        return False

    ###
    # makeHostile
    ###
    def makeHostile(self, other):
        for creature in self.hostileList:
            if creature == other:
                return
        self.hostileList.append(other)

    ###
    # makeFriendly
    ###
    def makeFriendly(self, other):
        for creature in hostileList:
            if creature.name == other.name:
                hostileList.remove(creture)
                break
    ###
    # isMonster
    ###
    def isMonster(self):
        return self.monster

    ###
    # isAttackable
    ###
    def canAttack(self, targetCreature):
        if abs(self.x - targetCreature.x) > self.attackRange or abs(self.y - targetCreature.y) > self.attackRange:
            return False
        else:
            return True
    ###
    # attack - attack another creature. 
    ###
    def attack(self, targetCreature, weapon):
        attack = libtcod.random_get_int(0, 1, 20)
        damage = 0
        if attack == 0:
            #TODO: handle critical miss
            pass
        elif attack >= 20 - weapon.criticalThreat:
            #TODO: handle critical hit
            pass
        else:
            attack = attack + weapon.attackBonus + self.stats.getStrBonus()
            if attack >= targetCreature.armorClass:
                #hit!
                damage=libtcod.random_get_int(0, weapon.minDamage, weapon.maxDamage)
                damage=damage + self.stats.getStrBonus()
                print ('The '+ self.name+' hits the '+ targetCreature.name+' for '+str(damage))
            else:
                #TODO: handle miss
                pass
        targetCreature.hp = targetCreature.hp - damage
        if targetCreature.hp < 1:
            targetCreature.blocks = False
            targetCreature.isDead = True
            targetCreature.color = DEAD_COLOR
            print("The "+targetCreature.name+" died!")
    ###
    # lookAround - return a list of all creatures in sight range
    ###
    #FIXME: should be a circle instead of a square
    def lookAround(self, creatures):
        sightedCreatures = []
        for creature in creatures:
            if creature.x > self.x + self.sightRadius and creature.x < self.x - self.sightRadius:
                continue
            if creature.y > self.y + self.sightRadius and creature.y < self.y - self.sightRadius:
                continue
            sightedCreatures.append(creature)
        return sightedCreatures

class Stats:

    ###
    # DND Style!
    ###
    def __init__(self, strength=10, dex=10, con=10, wis=10, intelligence=10, cha=10):
        self.strength = strength
        self.dex = dex
        self.con = con
        self.wis = wis
        self.intelligence = intelligence
        self.cha = cha

    ###
    # get stat bonuses
    ###
    def getStrBonus(self):
        return int((self.strength - 10) / 2)
    def getDexBonus(self):
        return int((self.dex - 10) / 2)
    def getConBonus(self):
        return int((self.con - 10) / 2)
    def getWizBonus(self):
        return int((self.wis - 10) / 2)
    def getIntBonus(self):
        return int((self.intelligence - 10) / 2)
    def getChaBonus(self):
        return int((self.cha - 10) / 2)

    ###
    # Run when player type classes level up
    ###
    def levelUpFighter(self):
        strength = strength + 2
        dex = dex + 2
        con = con + 2
        wis = wis + 1
        intelligence = intelligence + 1
        cha = cha + 1
    def levelUpRogue(self):
        self.strength = self.strength + 1
        self.dex = self.dex + 3
        self.con = self.con + 1
        self.wis = self.wis + 1
        self.intelligence = self.intelligence + 1
        self.cha = self.cha + 3
    def levelUpCaster(self):
        self.strength = self.strength + 1
        self.dex = self.dex + 1
        self.con = self.con + 1
        self.wis = self.wis + 3
        self.intelligence = self.intelligence + 3
        self.cha = self.cha + 1

###
# default AI for monsters
###
class BasicMonster:

    def __init__(self, theMap):
        self.theMap = theMap

    def takeTurn(self, sightedCreatures):
        targetCreature = None
        for creature in sightedCreatures:
            if self.owner.isHostile(creature):
                targetCreature = creature
                if self.owner.canAttack(creature):
                    self.owner.attack(creature, self.owner.weapon)
                    return 
                else:
                    self.owner.chase(targetCreature.x, targetCreature.y, self.theMap)
                    return
        #if targetCreature:
            #if self.owner.canAttack(targetCreature):
            #    self.owner.attack(targetCreature, self.owner.weapon)
            #    return
            #else:
            #    self.owner.chase(targetCreature.x, targetCreature.y)
            #    return
        # no hostile creature found; wander around
        #50% chance of not moving anywhere
        if libtcod.random_get_int(0, 0, 100) > 50:
            return
        else:
            self.owner.moveOrAttack(libtcod.random_get_int(0,0,1), libtcod.random_get_int(0,0,1), self.theMap)
            return
