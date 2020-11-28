import os

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
			
	def putInRoom(self, room):
		self.loc = room
		room.addInteractable(self)
		
	def returnInfoString(self):	#	Returns a string of info about the garden, formatted for display to the player
		growingList = []
		returnStr = ""
		returnStr += self.name + ":\n"
		returnStr += str(self.dirtW_Amnt) + "x" + str(self.dirtH_Amnt) + " of growing space, for a total of " + str(self.dirtAmnt) + " plots.\n"
		returnStr += "It currently looks like this: \n"
		returnStr += self.visualizeGarden()

		return returnStr
		
	def visualizeGarden(self):	#	returns a string that contains an intuitive text-based "visualization" of the garden
		plants = []
		for i in self.dirtPlots:
			if i.growing != None:
				plants.append(str(i.growing.name))
			else:
				plants.append(str(i.growing))
		plants.sort(reverse=True, key=(lambda x:len(x)))
		textMaxW = len("Plot ####: ") + len(plants[0])	#	Get sum of plant name display prefix and the longest plant-name to get the max width of text in a box
		
		returnStr = ""
		returnStr += ("-" * ((textMaxW + 2) * self.dirtW_Amnt)) + "\n"
		
		for i in range(len(self.dirtPlots)):	#	Loop through each dirt plot
			returnStr += "┊"
			
			plantTitle = "Plot #" + str(i + 1) + ": "
			if self.dirtPlots[i].growing != None:
				plantTitle += str(self.dirtPlots[i].growing.name)
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
		
class dirtPlot:
	def __init__(self):
		self.growing = None
		self.statusEffects = []
	
	