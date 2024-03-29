import os
import updater

from plant import Seed

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
	
class Garden:
	def __init__(self, dirtW_Amnt, dirtH_Amnt, name="Your Garden"):
		self.name = name
		self.loc = None
		self.dirtW_Amnt, self.dirtH_Amnt = dirtW_Amnt, dirtH_Amnt
		self.dirtAmnt= self.dirtW_Amnt * self.dirtH_Amnt
		self.dirtPlots = []
		for i in range(self.dirtAmnt):
			self.dirtPlots.append(dirtPlot())
			
		updater.dailyUpdateRegister(self)
	
	def dailyUpdate(self):
		for i in self.dirtPlots:
				
			if "watered" in i.statusEffects:	#	"watered" has a duration of 1 day, and is basically just a status to tell the player whether they've watered that plant today
				i.statusEffects.remove("watered")
		
	def putInRoom(self, room):
		self.loc = room
		#room.addInteractable(self) #	Not using "interactables" system anymore, using "room events" now
		
	def getPlotByNumber(self, plotNumStrInput):
		plotNum = int(plotNumStrInput)	#	Convert player input, captured as a string, to an integer
		for i in range(len(self.dirtPlots)):
			if i == plotNum:
				return self.dirtPlots[i]
				
		return False
	
	def returnGardenInfoString(self):	#	Returns a string of info about the garden, formatted for display to the player
		growingList = []
		returnStr = ""
		returnStr += self.name + ":\n"
		returnStr += str(self.dirtW_Amnt) + "x" + str(self.dirtH_Amnt) + " of growing space, for a total of " + str(self.dirtAmnt) + " plots.\n"
		returnStr += "It currently looks like this: \n"
		returnStr += self.visualizeGarden()
		returnStr += "\nThe following plots contain fully grown plants, ready for harvesting:\n"
		nothingGrown = True
		for i in range(len(self.dirtPlots)):
			if self.dirtPlots[i].growing != None:
				if self.dirtPlots[i].growing.fullyGrown:
					nothingGrown = False
					returnStr += "  Plot " + str(i + 1) + " contains a fully grown " + self.dirtPlots[i].growing.name + "\n"
		if nothingGrown:
			returnStr += "  None\n"
		
		return returnStr
		
	def visualizeGarden(self):	#	returns a string that contains an intuitive text-based "visualization" of the garden
		plants = []
		for i in self.dirtPlots:
			if i.growing != None:
				plants.append(str(i.growing.name))
			else:
				plants.append(str(i.growing))
		plants.sort(reverse=True, key=(lambda x:len(x)))
		textMaxW = len("Plot ####: ") + len(plants[0]) + len(" (W)")	#	Get sum of plant name display prefix and the longest plant-name to get the max width of text in a box
		
		returnStr = ""
		returnStr += ("-" * ((textMaxW + 2) * self.dirtW_Amnt)) + "\n"
		
		for i in range(len(self.dirtPlots)):	#	Loop through each dirt plot
			returnStr += "┊"
			
			plantTitle = "Plot #" + str(i + 1) + ": "
			if self.dirtPlots[i].growing != None:
				plantTitle += str(self.dirtPlots[i].growing.name)
				if self.dirtPlots[i].growing.wateredToday:
					plantTitle += " (W)"
			else:
				plantTitle += str(self.dirtPlots[i].growing)
				
			while len(plantTitle) < textMaxW:
				plantTitle += " "
			returnStr += plantTitle
			returnStr += "┊"
			
			if (i + 1) % self.dirtW_Amnt == 0:	#	If we reach the "end" of a "horizontal row" of the garden, add a newline and a divider bar
				returnStr += "\n"
				returnStr += ("-" * ((textMaxW + 2) * self.dirtW_Amnt)) + "\n"
			
		return returnStr
		
	def plantFromSeed(self, seedObject):
		plant = seedObject.becomePlant()
		for i in range(len(self.dirtPlots)):
			if self.dirtPlots[i].growing == None:
				self.dirtPlots[i].growing = plant
				break
			
	def fertilizePlot(self, callingEntity, plot):
		fertilizer = callingEntity.getInventoryItemByName("fertilizer")
		if fertilizer:
			plot.statusEffects.append(fertilizer.effect)
			callingEntity.items.remove(fertilizer)
			fertilizer.loc = None
			return True
		else:
			return False
			
	def waterPlot(self, plot):
		plot.statusEffects.append("watered")
		if plot.growing != None:
			plot.growing.watered()
			return True
		return False
		
	def harvestPlot(self, plot):
		if plot.growing != None:
			completedPlant = plot.growing.returnCompletedPlant()
			plot.growing = None
			return completedPlant	#	Can either return a new completed plant item, or can return False
		return False
		
	def returnPlotInfo(self, plot):
		if plot.growing != None:	#	If there's a plant, with a name, in plot.growing...
			return[plot.growing.name, plot.growing.age, plot.statusEffects, plot.growing.fullyGrown]
		else:	#	If not (ie, plot.growing is None)...
			return[plot.growing, plot.growing, plot.statusEffects, False]
		
class dirtPlot:
	def __init__(self):
		self.growing = None
		self.statusEffects = []
	
	
	