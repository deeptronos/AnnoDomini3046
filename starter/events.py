import random
from gametime import GameTime
from item import Item
from garden import Garden
from plant import plantGrades, Seed, CompletedPlant
from NPC import BountyHunter
from fieldOffice import FieldOffice
from pets import PetEgg

class Event:
    def __init__(self):
        self.actionCost = 0
        self.daysAvailable = []

class VendorEvent(Event):
    def __init__(self):
        super().__init__()
        self.vendorItems = []
        self.vendorItemCategories = []
        self.greeting = None
        self.goodbye = None
        self.purchaseMessage = None
    def displayVendorItems(self):
        for i in range(len(self.vendorItems)):
            print(i.name)

    def vendorHasItem(self, itemName):
        for i in self.vendorItems:
            if i.name.lower() == itemName:
                return True
        return False
    def getVendorItemByName(self, itemName):
        for i in self.vendorItems:
            if i.name.lower() == itemName:
                return i
        return False

class SleepEvent(Event):
    def __init__(self, gameTimeObject):
        super().__init__()
        self.gameTimeObject = gameTimeObject

    def sleep(self):
        self.gameTimeObject.advanceDate()

class GardenEvent(Event):
    def __init__(self, eventGarden):
            super().__init__()
            self.eventGarden = eventGarden
    def hasSeedInInventory(self, subject, seed):
        if subject.getInventoryItemByName(seed):
            if type(subject.getInventoryItemByName(seed)) == Seed:
                 return True
        return False
        
class MarketEvent(Event):
    def __init__(self):
        super().__init__()
        self.marketName = ""
        self.sellerItemsList = []
        self.sellerItems = {"crop":[], "flower":[], "illicit":[], "rare":[], 'test':[]}
        self.preferredTypes = []    #    Use this to distinguish markets. IE, farmer's market prefers "Crop" and "Flower" items; while black market would prefer "Illicit" and maybe "Rare"
        self.finalized = False
    def returnMarketInfo(self):
        return[self.marketName, self.perferredTypes]
        
    def addOnToSellerItemsList(self, item):
        self.sellerItemsList.append(item)
        
    def returnListedItemsTotalValue(self):
        returnVal = 0
        for i in self.sellerItemsList:
            returnVal += i.value
            
        return returnVal
        
    def finalizeSellerItems(self):
        for i in self.sellerItemsList:
            self.sellerItems[i.type].append(i)    #    Add each item the player wants to sell to their respective type-category in the sellerItems dict, based on the "type" property of the item
            
        self.sellerItemsList = []
        
    def sellAllItems(self, playerRef):
        results = ""
        for i in self.sellerItems:
            for j in self.sellerItems[i]:
                if j.grade == 0:    #    If plant is of 'poor' grade...
                    j.value = j.value - ((1/3) * j.value)    #    the plant's value is 2/3rds of its normal price!
                resultText = "Your " + plantGrades[j.grade] + " " + j.name + ' sold for L$' + str(j.value) + "\n"
                playerRef.sell(j)
                results += resultText

            self.sellerItems[i] = []
        return results
        
class FieldOfficeEvent(Event):
    def __init__(self, eventFieldOffice):
        super().__init__()
        self.eventFieldOffice = eventFieldOffice

class PetEvent(Event):
    def __init__(self, eventPet):
        super().__init__()
        self.eventPet = eventPet
    
gardenSupplyVendor = VendorEvent()
gardenSupplyVendor.vendorItems = [Item("Sheers", "A specialized tool for trimming your plants.", 25 ), Item("Vita-Fertilizer", "Maintains the health of your plants 50% better.", 10), Item("Lavender Seed", "Grows a single lavender plant.", 2)]    #    These aren't actually what the vendor will sell in-game
gardenSupplyVendor.greeting = "Welcome to Gardener's Delight! I'm Gardener, and I would be delighted to sell you some gardening supplies!"
gardenSupplyVendor.goodbye = "Come back soon!"
#gardenSupplyVendor.purchaseMessage = "Enjoy it!"

petStoreVendor = VendorEvent()
petStoreVendor.vendorItems = [PetEgg("Puppy Egg", "a cute little pet dog", 100, "dog"), PetEgg("Kitten Egg", "a sweet little newborn kitten", 100, "cat"), PetEgg("Gremling Egg", "an odd yet charming little creature", 120, "gremlin"), PetEgg("Rat Egg", "a playful, handsome little rat", 80, "rat"), PetEgg("Alien Egg", "a strange being that looks unlike anything you've seen before", 250, "Alien"), CompletedPlant("Pet Food", "food for a healthy pet", 5, 3, "nonplant") ]
petStoreVendor.greeting = "Welcome to my pet store! Please browse what friends we have available :)"
petStoreVendor.goodbye = "See ya around!"

