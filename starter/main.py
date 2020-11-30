from room import Room
from player import Player
from item import Item, HealingItem, DirtPlotEffector
from monster import Monster

from plant import Plant, Seed, CompletedPlant
from garden import Garden
from gametime import GameTime
import events

import os
import updater

player = Player()
gT = GameTime()

#    TODO: make plants be harvestable

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
    bY.roomEventTitles = ["garden"]
    bY.roomEvents = [defaultBackyardGardenEvent]
   
    bed = Room("In Your Bed")
    bed.roomEventTitles = ["sleep"]
    bed.roomEvents = [bedtime]

    #External Rooms:
    outside         = Room("Outside")   #   Generic 'outside' location, to tie together all of the colony's accessable location
    farmersMarket   = Room("The farmer's market")
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

    tS = Seed("test seed", "Seeds that grow into a beautiful hydrangea plant", 1, 1, 5, 25, 2)    #    test Seed
   # tS = Seed("Panicled Hydrangea Seed", "Seeds that grow into a beautiful hydrangea plant", 1, 15, 5, 25, 2)
       #   Seed init: def __init__(self, name, desc, value, growthDuration, price, plantPrice, radiation, exotic=False):
    tS.putInRoom(bY),tS.putInRoom(bY),tS.putInRoom(bY)
    tF = DirtPlotEffector("Fertilizer", "Makes the amount of time required for a seed to grow 2/3rds of its original duration!", 10)   #   test Fertilizer
    tCP = CompletedPlant("Test", "test description", 25, 3)  #   test CompletedPlant
    tCP.putInRoom(bY)
    tF.effect="fertilized"
    tF.putInRoom(bY)
    #i = Item("Rock", "This is just a rock.")
    #i.putInRoom(b)
    player.location = bY
    i.putInRoom(br), i.putInRoom(br)
    player.pickup(tS), player.pickup(tS), player.pickup(tS), player.pickup(tF)
    player.pickup(tCP)
   # player.pickup(i), player.pickup(i)    #Pickup two macbooks
    #Monster("Bob the monster", 20, b)

def header():
    title = "Anno Domini 3049: Newcomer Gardening Exhibition (Radiation Hell Fantasy)"
    date = gT.formattedDate()
    wDim = os.get_terminal_size()[0]

    iterant = 0
    line1, line2, line3, output = "", "", "", ""
    for i in range(wDim):   #   For loop to make a line of text the width of the terminal with the title centered in the middle
        if i < (wDim // 2) - (len(title)//2) or i >= (wDim // 2) + (len(title)//2):
            line1 += " "
        elif i >= (wDim // 2) - (len(title)//2):
            line1 += title[i - (wDim // 2) - (len(title)//2)]

    for i in range(wDim):   #   For loop that makes a line of text with the date, then fills to the window width with a symbol
        if (i) < len(date) + 2 and i > 1:
            line2 += date[i - 2]
        elif i > len(date) + 2:
            line2 += "𖡻"
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
    clear()
    print(header())
    print(event.greeting)
    print(visualizeContainer(len(event.greeting), "down"))

    for i in event.vendorItems:
        print(i.name,", '" ,i.desc,"' - price: ", i.value)

    print(visualizeContainer(len(event.greeting), "up"))

    commandSuccess = False
    while not commandSuccess:
        commandSuccess = True
        command = input("What would you like to do? ")
        commandWords = command.split()

        if commandWords[0].lower() == "buy":
            if event.vendorHasItem(command[4:]):
                item = event.getVendorItemByName(command[4:])
                player.buy(item)

def accessGarden(event):
   #while playing and player.alive:
      clear()
      print(header())
      print(event.eventGarden.returnGardenInfoString())
       
      commandSuccess = False
      while not commandSuccess:
         commandSuccess = True
         command = input("What would you like to do? ")
         commandWords = command.split()
           
         if commandWords[0].lower() == "plant":
            if event.hasSeedInInventory(player, command[6:]):
               seed = player.prepareSeedForPlanting(command[6:])
               event.eventGarden.plantFromSeed(seed)
               
         elif commandWords[0].lower() == "fertilize":   #   command is "fertilize ###" to fertilize a specific plot
            plotTargetNumber= command[10:]
            plot = event.eventGarden.getPlotByNumber(plotTargetNumber)
            if plot:
               fertilized = event.eventGarden.fertilizePlot(player, plot)
               if not fertilized:
                  clear()
                  print(header())
                  print("You don't have any fertilizer!")
                  input("Press enter to continue...")
                  
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
               input("Press enter to continue...")
         
         elif commandWords[0].lower() == "harvest":
            plotTargetNumber = command[8:]
            plotTargetNumber = str(int(plotTargetNumber) - 1)   #   Make "harvest 1" refer to the first plot, ie, plot 0. Again, a QOL thing.
            plot = event.eventGarden.getPlotByNumber(plotTargetNumber)
            
            harvested = event.eventGarden.harvestPlot(plot)
            if not harvested:   #   if harvestPlot() returns False...
               print("That plot does not contain a harvestable plant!")
               input("Press enter to continue...")
            else:
               harvested.loc = player
               player.items.append(harvested)    #   If harvestPlot() isn't False, harvested will be be a CompletedPlant item.
               #player.pickup(harvested)  
            
         elif commandWords[0].lower() == "back":   #   Is there a way to just make code to navigate back to the main loop, which doesn't require two inputs from the player? Ie, a way to have the player just type "back" to return, instead of "back" and using an input prompt to return
            #   Basically, I'm wondering how to do what the input prompt is doing (returning us to the main loop) without actually making the code use an input()?
            #input("Press enter to continue...")
            break   #   Is this the best practice?


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


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
    print("me -- See the current state of your stats and currency")
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
        else:
            print("Not a valid command")
            commandSuccess = False

    if timePasses == True:
        updater.updateAll()
