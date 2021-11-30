import os
import updater


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.health = 50
        self.alive = True
        self.lindenDollars = 10
        self.dailyPoints = 10
        self.dailyPointsLimit = 10    #    These aren't used at the moment
        self.attributes = ["self.health", "self.lindenDollars"]#, "self.dailyPoints"]     #   For use in displaying current status ("me" command)
        self.visitedToday = {}
        self.firstTime = True
        
        self.myPet = None
        
        updater.dailyUpdateRegister(self)
        
    def dailyUpdate(self):
        self.bedtime() 
        for i in self.visitedToday:
            self.visitedToday[i] = False
        
    def goDirection(self, direction):
        dir =  self.location.getDestination(direction)
        if not dir:
            return False
        else:
            self.location = self.location.getDestination(direction)
            return True

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
        
    def getMultipleInventoryItemsByName(self, name):    #    Get a list of items from your inventory by their shared name
        returnList = []
        for i in self.items:
            if i.name.lower().strip() == name.lower().strip():
                returnList.append(i)  
                
        if returnList != []:
            return returnList
        return False
        
    def inspectItem(self, name):
        item = self.getInventoryItemByName(name)    #   Tries to find item in player inventory
        
        loc = "your inventory"
        if not item:    #   If it isn't in player inventory...
            item = self.location.getItemByName(name)
            loc = self.location.desc.lower()

        clear()
        print(item.name.capitalize().strip() + ":")
        print(item.desc)
        print("It is currently located in ", loc,".", sep='' )
        print()
        input("Press enter to continue...")
        
    # def stackItemList(inList):
    #        returnList, countedItems = [], []
    #        for i in inList:
    #           if i not in countedItems:
    #              
    #              count = str(inList.count(i))
    #              displayStr = i.name
    #              displayStr += (' x' + count)
    #              returnList.append(displayStr)
    #              countedItems.append(i)
    #        
    #        return returnList
           
    def showInventory(self):
        inventoryDisplayList, itemNames, countedItemNames = [], [], []
        
        for i in self.items:
            itemNames.append(i.name)
        
        for i in self.items:
            if i.name not in countedItemNames:
                count = str(itemNames.count(i.name))
                displayStr = i.name
                displayStr += (" x" + count)
                inventoryDisplayList.append(displayStr)
                countedItemNames.append(i.name)
        clear()
        print("You are currently carrying:")
        print()
        
        for i in inventoryDisplayList:
            print(i)
        print()
        input("Press enter to continue...")
        
    def returnSellableMarketGoods(self, goodClasses, goodTypes):
        #returnList, countedItems = [], []
        returnList = []
        for i in self.items:
            if type(i) in goodClasses and i.type in goodTypes:    #    Yes, type(i) and i.type are entirely different things, but their naming sorta makes sense. type(i) is the class of the item i, and i.type is the property of item i that defines what type of plant it is.
                
                # count = str(self.items.count(i))
                # displayStr = i.name
                # displayStr += ( " x" + count)
                #returnList.append(displayStr)
                returnList.append(i)
                #countedItems.append(i)
                
        return returnList
        
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
        if self.lindenDollars >= cost:
            self.lindenDollars -= cost
            self.items.append(purchaseTarget)
            purchaseTarget.loc = self
            print("Your new balance is L$", self.lindenDollars)
            #input("Press enter to continue...")
            return True
        else:
            #clear()
            print("You don't have enough Linden Dollars :<")
            #input("Press enter to continue...")
            return False
    def sell(self, item):
        value = item.value
        self.lindenDollars += value
        self.lindenDollars = round(self.lindenDollars, 2)
        self.items.remove(item)
        item.loc = None
        
    def prepareSeedForPlanting(self, seedName):
        seed = self.getInventoryItemByName(seedName)
        self.items.remove(seed)
        seed.loc = None
        return seed
        
    def prepareEggForHatching(self, egg):    #    This is very very similar to prepareSeedForPlanting, however it's a distinct function for the sake of debugging :P
        self.items.remove(egg)
        egg.loc = None
        return egg
        
    def checkValueAgainstPlayerLindendollars(self, value):    #    Newer function than many, so it isn't implemented very widely yet.
        if value <= self.lindenDollars:
            return True
        return False
    
    def bedtime(self):
        self.dailyPoints = self.dailyPointsLimit #  Refresh daily points for a new day
