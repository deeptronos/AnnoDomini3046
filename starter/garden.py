import os

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
	

class Garden:
	def __init__(self, dirtW_Amnt, dirtH_Amnt, name="Your Garden"):
		self.name = name
		self.loc = None
		self.dirtW_Amnt, self.dirtH_Amnt = dirtW_Amnt, dirtH_Amnt
		self.dirtAmnt = self.dirtW_Amnt * self.dirtH_Amnt
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
		for i in self.dirtPlots:
			if i.growing != None:
				returnStr += str(i.growing.name) + "\n"
			else:
				returnStr += str(i.growing) + "\n"
		return returnStr
		
	def visualizeGarden(self):	#	returns a string that contains an intuitive text-based "visualization" of the garden
		plants = []
		for i in self.dirtPlots:
			if i.growing != None:
				plants.append(str(i.growing.name))
			else:
				plants.append(str(i.growing))
		plants.sort(reverse=True, key=(lambda x:len(x)))
		textMaxW = len(plants[0])	#	Get longest plant-name
		
		returnStr = ""
		returnStr += ("-" * ((textMaxW + 2) * self.dirtW_Amnt)) + "\n"
		for h in range(self.dirtH_Amnt):
			for w in range(self.dirtW_Amnt):
				returnStr += "┊"
				if self.dirtPlots[w+h].growing != None:
					plantTitle = str(self.dirtPlots[w+h].growing.name)
				else:
					plantTitle = str(self.dirtPlots[w+h].growing)
					
				while len(plantTitle) < textMaxW:
					plantTitle += " "
				returnStr += plantTitle
				returnStr += "┊"
				
			returnStr += "\n"
			returnStr += ("-" * ((textMaxW + 2) * self.dirtW_Amnt)) + "\n"
			
		return returnStr
		
	def plantFromSeed(self, seedObject):
		plant = seedObject.becomePlant()
		for i in range(len(self.dirtPlots)):
			clear()
			print("jajaja")
			if self.dirtPlots[i].growing == None:
				self.dirtPlots[i].growing = plant
				break
			input()
		
class dirtPlot:
	def __init__(self):
		self.growing = None
		self.statusEffects = []
	
	