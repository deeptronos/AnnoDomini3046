import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, value=None):
        self.name = name
        self.desc = desc
        self.loc = None
        self.value = value
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)

class Weapon(Item):
    def __init__(self, name, desc, value=None):
        super().__init__()
        self.damage = 0

class Gun(Weapon):
    def __init__(self, name, desc, value=None):
        super().__init__()
        self.ammoCapacity = 0
        self.accuracy = 100

class HealingItem(Item):
    def __init__(self, name, desc, value=None):
        super().__init__(name, desc, value)
        self.healthRestore = 0
        self.usable = True
    def heal(self, target):
        if self.usable:
            target.health += self.healthRestore
            target.items.remove(self)
            self.loc = None
            

