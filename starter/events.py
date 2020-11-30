import random
from gametime import GameTime
from item import Item
from garden import Garden

class Event:
    def __init__(self):
        self.actionCost = 0

class VendorEvent(Event):
    def __init__(self):
        super().__init__()
        self.vendorItems = []
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
            return True
        return False
        
class MarketEvent(Event):
    def __init__(self):
        super().__init__()
        self.sellerItems = []
    def sellItems(self):
        
    

gardenSupplyVendor = VendorEvent()
gardenSupplyVendor.vendorItems = [Item("Sheers", "A specialized tool for trimming your plants.", 25 ), Item("Vita-Fertilizer", "Maintains the health of your plants 50% better.", 10), Item("Lavender Seed", "Grows a single lavender plant.", 2)]
gardenSupplyVendor.greeting = "Welcome to Gardener's Delight! I'm Gardener, and I would be delighted to sell you some gardening supplies!"
gardenSupplyVendor.goodbye = "Come back soon!"
#gardenSupplyVendor.purchaseMessage = "Enjoy it!"


