class Item(object):

    def __init__(self, name, character):
        self.name = name
        self.character = character

class Weapon(Item):

    def __init__(self, name, character, minDamage, maxDamage, twoHanded=False, attackBonus=0, damageBonus=0, criticalThreat=0):
        self.twoHanded=twoHanded
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.attackBonus = attackBonus
        self.damageBonus = damageBonus
        self.criticalThreat = criticalThreat
        super(Weapon, self).__init__(name, character)

class Armor(Item):

    def __init__(self, name, character, armorClass, strReq):

        self.armorClass = armorClass
        self.strReq = strReq
        super(Armor, self).__init__(name, character)

class Inventory:

    def __init__(self, owner):
        items = None

    def addItem(item):
        items.append(item)

    def removeItem(item):
        items.remove(item)
