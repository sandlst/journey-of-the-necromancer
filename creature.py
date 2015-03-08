import libtcodpy as libtcod

DEAD_COLOR = libtcod.darkest_gray

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

    ###
    # setName
    ###
    def setName(self, newName):
        self.name = newName

    ###
    # move 
    ###
    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    ###
    # chase - move towards something
    ###
    def chase(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        #vector to find distance
        distance = math.sqrt(dx ** 2 + dy ** 2)
        #normalize, then round and convert
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

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
    # getAttackRange
    ###
    def getAttackRange(self):
        return self.attackRange

    ###
    # setAttackRange
    ###
    def setAttackRange(self, newAttackRange):
        self.attackRange = newAttackRange

    ###
    # isAttackable
    ###
    def canAttack(self, targetCreature):
        if abs(self.x - targetCreature.x) > attackRange:
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
            else:
                #TODO: handle miss
                pass
        print "Attack roll: "+str(attack)
        print "Damage: "+str(damage)
        targetCreature.hp = targetCreature.hp - damage
        if targetCreature.hp < 1:
            targetCreature.blocks = False
            targetCreature.isDead = True
            targetCreature.color = DEAD_COLOR
            print("The "+targetCreature.name+" died!")
    ###
    # getSightRadius
    ###
    def getSightRaius(self):
        return self.sightRadius

    ###
    # lookAround - return a list of all creatures in sight range
    ###
    #FIXME: should be a circle instead of a square
    def lookAround(self, creatures):
        for creature in creatures:
            if creature.x > self.x + self.sightRadius and creature.x < self.x - self.sightRadius:
                continue
            if creature.y > self.y + self.sightRadius and creature.y < self.y - self.getSightRaius:
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
    def takeTurn(self):
        sightedCreatures = owner.lookAround()
        for creature in sightedCreatures:
            if owner.isHostile(creature):
                targetCreature = creature
                if owner.canAttack(creature):
                    break
        if targetCreature:
            if owner.canAttack(targetCreature):
                owner.attack(targetCreature)
                return
            else:
                owner.chase(targetCreature.x, targetCreature.y)
                return
        # no hostile creature found; wander around
        #50% chance of not moving anywhere
        if libtcod.random_get_int(0, 0, 100) > 50:
            return
        else:
            owner.move(libtcod.random_get_int(0,0,1), libtcod.random_get_int(0,0,1))
            return
