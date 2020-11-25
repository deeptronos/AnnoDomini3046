import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.health = 50
        self.alive = True
        self.currency = 100
        self.dailyPoints = 10
        self.dailyPointsLimit = 10
        self.attributes = ["self.health", "self.currency", "self.dailyPoints"]     #   For use in displaying current status ("me" command)

    def goDirection(self, direction):
        self.location = self.location.getDestination(direction)

    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.removeItem(item)

    def drop(self, item):
        print("item: ", item)
        print("self.items: ", self.items)
        self.items.remove(item)
        item.loc = self.location
        self.location.addItem(item)

    def displayStat(self, statName):    #   Function code concept credit to https://stackoverflow.com/a/32001042
        print(statName, '=', repr(eval(statName)))

    def getInventoryItemByName(self, name): #   Get item in inventory by name
        for i in self.items:
            if i.name.lower() == name.lower():
                return i

        return False

    def inspectItem(self, name):
        item = self.getInventoryItemByName(name)    #   Tries to find item in player inventory
        loc = "your inventory"
        if not item:    #   If it isn't in player inventory...
            item = self.location.getItemByName(name)
            loc = self.location.desc.lower()

        clear()
        print(item.name.capitalize(), ":")
        print(item.desc)
        print("It is currently located in ", loc,".", sep='' )
        print()
        input("Press enter to continue...")

    def showInventory(self):
        inventoryDisplayList, countedItems = [], []
        for i in self.items:
            if i not in countedItems:
                count = str(self.items.count(i))
                displayStr = i.name
                displayStr += ( " x" + count)
                inventoryDisplayList.append(displayStr)
                countedItems.append(i)
        clear()
        print("You are currently carrying:")
        print()
        for i in inventoryDisplayList:
            print(i)
        print()
        input("Press enter to continue...")
        
    def attackMonster(self, mon):
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        if self.health > mon.health:
            self.health -= mon.health
            print("You win. Your health is now " + str(self.health) + ".")
            mon.die()
        else:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")

    def buy(self, purchaseTarget):
        cost = purchaseTarget.value
        if self.currency >= cost:
            self.currency -= cost
            self.items.append(purchaseTarget)
            purchaseTarget.loc = self
            print("your new balance is ", self.currency)
            input("Press enter to continue...")
        else:
            clear()
            print("You don't have enough currency :<")
            input("Press enter to continue...")
            return False
            
    def prepareSeedForPlanting(self, seedName):
        seed = self.getInventoryItemByName(seedName)
        self.items.remove(seed)
        seed.loc = None
        return seed
        
    def bedtime(self):
        self.dailyPoints = self.dailyPointsLimit #  Refresh daily points for a new day
