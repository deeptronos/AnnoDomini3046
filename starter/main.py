from room import Room
from player import Player
from item import Item, HealingItem, DirtPlotEffector
from monster import Monster

from plant import Plant, Seed, CompletedPlant, plantGrades
from garden import Garden
from gametime import GameTime
import events

import os
import updater
import json

player = Player()
gT = GameTime()
#seeds = {}


#    TODO: make more seeds/plants in seeds.json; go through JSON -> seed -> plant -> CompletePlant process and check for bugs; add some sort of field office functionality; make farmer's market only open on weekends (?); add some sort of reward for rare plants (rudimentary exhibitions? maybe an internet forum :D!!); debug all inputs; make EVERYTHING more intuitive (write guide? maybe just for this beta)


def createWorld():

   bedtime = events.SleepEvent(gT) #   Initializing this here, not in events.py, because we need to refer to gT

   #House Rooms:
   br = Room("Your Bedroom")
   lr = Room("Your Living Room")
   #bY = Room("Your Backyard. It contains a modest g is 6x2 feet large. ")
   bY = Room("Your Backyard")
   g = Garden(6, 2)
   g.putInRoom(bY)
   defaultBackyardGardenEvent = events.GardenEvent(g)
   bY.addRoomEvent("garden", defaultBackyardGardenEvent)
   #bY.roomEventTitles = ["garden"]
   #bY.roomEvents = [defaultBackyardGardenEvent]
   
   bed = Room("In Your Bed")
   bed.roomEventTitles = ["sleep"]
   bed.roomEvents = [bedtime]

   #External Rooms:
   outside         = Room("Outside")   #   Generic 'outside' location, to tie together all of the colony's accessible locations
    
   farmersMarket   = Room("The farmer's market")
   farmersMarketEvent = events.MarketEvent()
  # farmersMarket.roomEventTitles = ["market"]
   farmersMarket.addRoomEvent("market", farmersMarketEvent)
   #farmersMarket.roomEvents = [farmersMarketEvent]
   farmersMarketEvent.marketName = "the farmer's market"
    
   gardenSupply    = Room("'Gardener's Delight' Garden Supply Emporium")
   gardenSupply.roomEventTitles = ["vendor"]   #   We can buy stuff in the garden supply
   gardenSupply.roomEvents = [events.gardenSupplyVendor]

   fieldOffice     = Room("Wasteland Field Office")


   Room.connectRooms(br, "living room",  lr, "bedroom")
   Room.connectRooms(br, "to bed", bed, "out of bed") #   Bed is a "room" that advances the day when you enter it
   Room.connectRooms(lr, "backyard", bY, "living room")
   Room.connectRooms(lr, "outside", outside, "inside")

   Room.connectRooms(bed, "backyard", bY, "bed")   #   FOR TESTING

   Room.connectRooms(outside, "farmers market", farmersMarket, "home")
   Room.connectRooms(outside, "garden supply", gardenSupply, "home")
   Room.connectRooms(outside, "field office", fieldOffice, "home")

   i = Item("Macbook", "This is your 3019 16-Inch Macbook Oh.")
   
   
   h = HealingItem("Juicebox", "a bit of juice always helps")
   h.healthRestore = 100
   h.putInRoom(lr)
   #tS = Seed("test seed", "Seeds that grow into a beautiful hydrangea plant", 1, 1, 5, 25, 2)    #    test Seed
   # tS = Seed("Panicled Hydrangea Seed", "Seeds that grow into a beautiful hydrangea plant", 1, 15, 5, 25, 2)
       #   Seed init: def __init__(self, name, desc, value, growthDuration, price, plantPrice, radiation, exotic=False):
  # tS.putInRoom(bY),tS.putInRoom(bY),tS.putInRoom(bY)
   tF = DirtPlotEffector("Fertilizer", "Makes the amount of time required for a seed to grow 2/3rds of its original duration!", 10)   #   test Fertilizer
   tCP = CompletedPlant("Test", "test description", 25, 3, "test")  #   test CompletedPlant
   potato = CompletedPlant("Potato", "A beautiful delicious potato", 5, 0, "crop")  #   testing potato
   tCP.putInRoom(bY), potato.putInRoom(bY),potato.putInRoom(bY)
   
   tF.effect="fertilized"
   tF.putInRoom(bY)
   #i = Item("Rock", "This is just a rock.")
   #i.putInRoom(b)
   player.location = bY
   i.putInRoom(br), i.putInRoom(br)
  # player.pickup(tS), player.pickup(tS), player.pickup(tS), player.pickup(tF)
   player.pickup(tCP), player.pickup(potato),player.pickup(potato)
   #player.location = farmersMarket
   # player.pickup(i), player.pickup(i)    #Pickup two macbooks
   #Monster("Bob the monster", 20, b)


def header():
    title = "Anno Domini 3049: Newcomer Gardening Exhibition (Radiation Hell Fantasy)"
    date = gT.formattedDate()
    currency = "L$ " + str(player.lindenDollars)
    wDim = os.get_terminal_size()[0]

    iterant = 0
    line1, line2, line3, output = "", "", "", ""
    for i in range(wDim):   #   For loop to make a line of text the width of the terminal with the title centered in the middle
        if i < (wDim // 2) - (len(title)//2) or i >= (wDim // 2) + (len(title)//2):
            line1 += " "
        elif i >= (wDim // 2) - (len(title)//2):
            line1 += title[i - (wDim // 2) - (len(title)//2)]

    for i in range(wDim):   #   For loop that makes a line of text with the date, then fills, to the window width minus the length of the currency string, with a symbol, then inserts the currency string
        if (i) < len(date) + 2 and i > 1:
            line2 += date[i - 2]
        elif i > len(date) + 2 and i < wDim - len(currency) - 1:
            line2 += "𖡻"
        elif i >= wDim - len(currency):   #
           line2 += currency[i - (wDim - len(currency))]
        else:
            line2 += " "

    for i in range(wDim):   #   For loop that fills a string to window width with a symbol
        line3 += "𝍅"

    for i in range(3):  #   Puts all these different strings into one, separating them by new lines
        if i == 0:
            output += line1
        elif i == 1:
            output += line2
        elif i == 2:
            output += line3
        output += "\n"

    return output

def vendor(event):
   player.visitedToday[event] = True   #   Functionality not implemented, ignore this :P

   event.vendorItems = seeds[gT.currentSeason]   #   The vendor is selling the current season's seeds
   #else:
   #return event.vendorItems
   
   clear()
   print(header())
   print(event.greeting)
   print(visualizeContainer(len(event.greeting), "down"))
   
   for i in event.vendorItems:
     print(i.name,", '" ,i.desc,"' - price: L$", i.value)
   
   print(visualizeContainer(len(event.greeting), "up"))
   
   commandSuccess = False
   while not commandSuccess:
     commandSuccess = True
     command = input("What would you like to do? ('buy [item name]'; 'return') ")
     commandWords = command.split()
   
     if commandWords[0].lower() == "buy":
         if event.vendorHasItem(command[4:]):
             item = event.getVendorItemByName(command[4:])
             bought = player.buy(item)
             commandSuccess = False
             
     elif commandWords[0].lower() == "return":
         break
      

def accessGarden(event):
   playing = True
   while playing and player.alive:
      clear()
      print(header())
      print(event.eventGarden.returnGardenInfoString())
       
      commandSuccess = False
      while not commandSuccess:
         commandSuccess = True
         command = input("What would you like to do? ('plant [seed name]'; 'fertilize #'; 'check #'; 'water #'; 'harvest #'; 'return') ")
         commandWords = command.split()
         
         if commandWords == []:   #   Allows us to have multi-word directions without causing an index error
           commandWords = ["nothing"]
         
         if commandWords[0].lower() == "plant":
            if event.hasSeedInInventory(player, command[6:]):
               seed = player.prepareSeedForPlanting(command[6:])
               event.eventGarden.plantFromSeed(seed)
            else:
               print("You don't have that in your inventory, or the object you're referring to isn't a seed.")
               #commandSuccess = False
            commandSuccess = False
               
         elif commandWords[0].lower() == "fertilize":   #   command is "fertilize ###" to fertilize a specific plot
            plotTargetNumber= command[10:]
            plot = event.eventGarden.getPlotByNumber(plotTargetNumber)
            if plot:
               fertilized = event.eventGarden.fertilizePlot(player, plot)
               if not fertilized:
                  print("You don't have any fertilizer!")
               else:
                  print("Fertilized plot " + plotTargetNumber)
                  
            commandSuccess = False
                  
         elif commandWords[0].lower() == "check":   #   command is "check ###" to check a specific plot
            plotTargetNumber = command[6:]
            plotTargetNumber = str(int(plotTargetNumber) - 1)   #   Make "check 1" refer to the first plot, ie, plot 0. This is a QOL thing to make it intuitive to non-programmers
            plot = event.eventGarden.getPlotByNumber(plotTargetNumber)
            if plot:
               plotInfo = event.eventGarden.returnPlotInfo(plot)
               if plotInfo[2] != []:
                  plotEffects = ", "
                  plotEffects = plotEffects.join(plotInfo[2])   #   Make the statusEffects on the plot, stored in plotInfo[1], into a string formatted for display to the player
               else:
                  plotEffects = "Nothing"
               
               displayStr = "Plot #" + str(int(plotTargetNumber) + 1) +": \n"
               displayStr += "   Growing " + str(plotInfo[0]) + "\n"
               displayStr += "   Plant age: " + str(plotInfo[1]) + "\n"
               displayStr += "   Fully Grown: " + str(plotInfo[3]) + "\n"
               displayStr += "   Current effects: " + plotEffects + "\n"
            
               clear()
               print(header())
               print(displayStr)
               input("Press enter to continue...")
         
         elif commandWords[0].lower() == "water":
            plotTargetNumber = command[6:]
            plotTargetNumber = str(int(plotTargetNumber) - 1)   #   Make "water 1" refer to the first plot, ie, plot 0. Again, a QOL thing.
            plot = event.eventGarden.getPlotByNumber(plotTargetNumber)
            
            watered = event.eventGarden.waterPlot(plot)
            if not watered:
               print("There's nothing planted in that plot!")
            commandSuccess = False
            
         elif commandWords[0].lower() == "harvest":
            plotTargetNumber = command[8:]
            plotTargetNumber = str(int(plotTargetNumber) - 1)   #   Make "harvest 1" refer to the first plot, ie, plot 0. Again, a QOL thing.
            plot = event.eventGarden.getPlotByNumber(plotTargetNumber)
            
            harvested = event.eventGarden.harvestPlot(plot)
            if not harvested:   #   if harvestPlot() returns False...
               print("That plot does not contain a harvestable plant!")
            else:
               harvested.loc = player
               player.items.append(harvested)    #   If harvestPlot() isn't False, harvested will be be a CompletedPlant item.
               #player.pickup(harvested)  
            commandSuccess = False
         elif commandWords[0].lower() == "return":   #   Is there a way to just make code to navigate back to the main loop, which doesn't require two inputs from the player? Ie, a way to have the player just type "back" to return, instead of "back" and using an input prompt to return
            #   Basically, I'm wondering how to do what the input prompt is doing (returning us to the main loop) without actually making the code use an input()?
            #input("Press enter to continue...")
            #break   #   Is this the best practice?
            playing = False
            
         else:
            commandSuccess = False

def accessFarmersMarket(event):
   playing = True
   event.__init__()
   event.marketName = "The farmer's market"
   
   while playing and player.alive:
      clear()
      print(header())
      print("Welcome to " + event.marketName +"!")
      print("Ready to sell your goods? Here's what you've got that'll sell here:")
      sellableGoods = player.returnSellableMarketGoods([CompletedPlant], ["crop", "flower", "test"])
      for i in sellableGoods:
         print(i)
      if event.sellerItemsList != []:
         print("Here's what you're currently planning to sell:")
         stackedSellItems = stackItemList(event.sellerItemsList)
         for i in stackedSellItems: print(i)
      
      commandSuccess = False
      while not commandSuccess:
         commandSuccess
         command = input("What would you like to do? (Commands: 'sell [item name]'; 'check'; 'clear'; 'finalize'; 'return') ")
         commandWords = command.split()
         if commandWords == []:   #   Allows us to have multi-word directions without causing an index error
           commandWords = ["nothing"]
           
         if commandWords[0].lower() == "sell":   #   'sell [itemname]' will make all items in your inventory with that name be sellable 
            sellTargetName = command[5:]
            sellTargets = player.getMultipleInventoryItemsByName(sellTargetName)
            
            if sellTargets != False and sellTargets[0] not in event.sellerItemsList:
               for i in sellTargets:
                  event.addOnToSellerItemsList(i)
                  
               commandSuccess = True
               
            elif sellTargets[0] in event.sellerItemsList:
               print("You're already planning to sell all of those!")
   
         elif commandWords[0].lower() == "finalize":   #   Finalize what they're selling
            if event.sellerItemsList != []:
               event.finalizeSellerItems()
               results = event.sellAllItems(player)
               print(results)
               print("Your new balance is L$ " + str(player.lindenDollars))
               #event.sellItems()
               input("Press enter to continue...")
               commandSuccess = True
               playing = False
               # clear()
               # print()
               # input("press enter")
            else:
               print("You haven't marked anything for sale!")
               commandSuccess = False
           
         elif commandWords[0].lower() == "clear":   #   Reset the variables containing what we're planning to sell
            event.sellerItemsList = []
            event.sellerItems = {"crop":[], "flower":[], "illicit":[], "rare":[], 'test':[]}   #   organized by plant type
            commandSuccess = True
            
         elif commandWords[0].lower() == "return":   #   Return out of the "market" sub-menu
            if event.sellerItemsList != []:   #   Player cannot leave the market unless they aren't selling anything
               print("Wait! You still have items marked for sale. Please 'clear' them to exit the market.")
               commandSuccess = False
               continue
               
            commandSuccess = True
            playing = False   #   Yes the player is still playing, but this variable is used here to contain/exit the super-loop that it's contained in/
         else:
            print("Not a valid command")
            commandSuccess = False

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def stackItemList(inList):
   returnList, countedItems = [], []
   for i in inList:
      if i not in countedItems:
         countedItems.append(i)
         count = str(inList.count(i))
         displayStr = i.name
         displayStr += (' x' + count)
         returnList.append(displayStr)
   
   return returnList
   
{"crop":[], "flower":[], "illicit":[], "rare":[], 'test':[]}

def readItemsFromJSON(file, itemType):   #UNUSED - I'm specializing each item's JSON importing methods, this is just a template.
   outDict = {}
      #   using seeds.json organization as example for following comments:
      
   for i in file:   #   "seeds"
      for j in file[i]:   #   "crop", "flower", "illicit", "rare", "test"
         categoryContainer = []
         for k in file[i][j]:   #   "lavender", "rose"
            newItemProps = []
            for a in file[i][j][k]:   #   "plantName", "desc", "value", "growthDuration", "seedPrice", etc.
               #outDict[j]
               newItemProps.append(file[i][j][k][a])
            newItem = itemType(newItemProps)
            categoryContainer.append()

def readSeedsFromJSON(file):
   outDict = {"spryng":[], "otom":[], "season":[]}   #   "season" is default category
      #   using seeds.json organization as example for following comments:
   with open('seeds.json') as f:
      data = json.load(f)
      
   for i in data:   #   "seeds"
      for j in data[i]:   #   "crop", "flower", "illicit", "rare", "test"
         for k in data[i][j]:   #   "lavender", "rose"
            newItemProps = []
            for a in data[i][j][k]:   #   "plantName", "desc", "value", "growthDuration", "seedPrice", etc.
               newItemProps.append(data[i][j][k][a])
               
            plantName = newItemProps[0]
            desc   = newItemProps[1]
            value = newItemProps[2]
            growthDuration = newItemProps[3]
            seedPrice = newItemProps[4]
            plantPrice = newItemProps[5]
            radiation = newItemProps[6]
            exotic = newItemProps[7]
            plantType = newItemProps[8]
            season = newItemProps[9].lower()
            
            newSeed = Seed(plantName + " seed", desc, value, growthDuration, seedPrice, plantPrice, radiation, exotic, plantType)
            outDict[season].append(newSeed)
            
   return outDict
seeds = readSeedsFromJSON('seeds.json')


def printSituation():
    clear()
    print(header())

    print(player.location.desc)
    print()
    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can do the following things in this room:")
    for e in player.location.exitNames():
        print(e)

    if player.location.hasEvents():
        print("You can do the following interactions:")
        for i in player.location.roomEventTitles:
            print(i)
    print()

def showHelp():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print("drop <item> -- Drop an item from your inventory")
    print("sleep -- In areas that contain a sleepable bed of some sort, use this to go to bed")
    print("vendor -- In areas in which a vendor resides, use this to browse and purchase their wares")
    print("wait -- Wait a cycle")
    print("heal <item> -- Uses a healing <item> from your inventory to increase your health. Be mindful - they're often single use.")
    print("inspect <item> -- Inspect an <item>")
    print("me -- See the current state of your stats and Linden Dollars")
    print()
    input("Press enter to continue...")

def showPlayerStats():
    clear()
    print("Let's take a look at you:")
    print(visualizeContainer(26, "down"))
    for i in player.attributes: #   For each string in the list player.attributes...
        player.displayStat(i)   #   Display that stat
    print(visualizeContainer(26, "up"))
    input("Press enter to continue...")

def visualizeContainer(width, direction):
    output = ""
    charList = ["╶", "╴", "╭","╮","╰","╯","━", "─"]
    for i in range(width):
        if i == 0:
            if direction == "up":
                output += charList[4]
            elif direction == "down":
                output += charList[2]
        elif i == width - 1:
            if direction == "up":
                output += charList[5]
            elif direction == "down":
                output += charList[3]
        else:
            output += charList[7]
    return output

createWorld()
playing = True
while playing and player.alive:
    printSituation()
    commandSuccess = False
    timePasses = False

    while not commandSuccess:
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()
        
        if commandWords == []:   #   Allows us to have multi-word directions without causing an index error
           commandWords = ["nothing"]
           
        if commandWords[0].lower() == "go":   #CAN handle multi-word directions now that we're using goDirection on the sliced input string
            player.goDirection(command[3:])
            timePasses = True

        elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                print("No such item.")
                commandSuccess = False

        elif commandWords[0].lower() == "drop":
            targetName = command[5:]
            target = player.getInventoryItemByName(targetName)
            if target != False: #   If getInventoryItemByName doesn't return false...
                player.drop(target)
            else:
                print("No such item.")
                commandSuccess = False

        elif commandWords[0].lower() == "inspect":
            targetName = command[8:]
            player.inspectItem(targetName)

        elif commandWords[0].lower() == "me":
            showPlayerStats()
        elif commandWords[0].lower() == "inventory":
            player.showInventory()
        elif commandWords[0].lower() == "help":
            showHelp()
        elif commandWords[0].lower() == "exit":
            playing = False
        elif commandWords[0].lower() == "attack":
            targetName = command[7:]
            target = player.location.getMonsterByName(targetName)
            if target != False:
                player.attackMonster(target)
            else:
                print("No such monster.")
                commandSuccess = False

        elif commandWords[0].lower() == "vendor":
            for i in range(len(player.location.roomEventTitles)):
                if player.location.roomEventTitles[i] == "vendor":
                    vendor(player.location.roomEvents[i])

        elif commandWords[0].lower() == "sleep":
            for i in range(len(player.location.roomEventTitles)):
                if player.location.roomEventTitles[i] == "sleep":
                    player.bedtime()
                    player.location.roomEvents[i].sleep()
                    clear()
                    print(header())
                    print("Good morning! It's ", gT.formattedDate(), sep="")
                    input("Press enter to continue...")
                    updater.updateAll()
                    updater.dailyUpdateAll()

        elif commandWords[0].lower() == "heal":
            targetName = command[5:]
            target = player.getInventoryItemByName(targetName)
            if target != False: #   If getInventoryItemByName doesn't return false...
                target.heal(player)
            else:
                print("No such item.")
                commandSuccess = False

        elif commandWords[0].lower() == "wait":
            timePasses = True
            
        elif commandWords[0].lower() == "garden":
            for i in range(len(player.location.roomEventTitles)):
             if player.location.roomEventTitles[i] == "garden":
                 accessGarden(player.location.roomEvents[i])
         
        elif commandWords[0].lower() == "market":
           for i in range(len(player.location.roomEventTitles)):
              if player.location.roomEventTitles[i] == "market":
                  accessFarmersMarket(player.location.roomEvents[i])
        else:
            print("Not a valid command")
            commandSuccess = False

    if timePasses == True:
        updater.updateAll()
