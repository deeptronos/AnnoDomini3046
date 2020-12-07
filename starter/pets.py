from item import Item
from plant import clamp, mapRange
import events
import updater

import random
import os

#	TODO: add value calculation; add some way to sell pets?

class PetFood(Item):
	def __init__(self, name, desc, value):
		super().__init__(name, desc, value)

class PetEgg(Item):
	def __init__(self, name, desc, value, petType):
		super().__init__(name, desc, value)
		self.petType = petType
	def hatch(self):
		petName = input("What would you like to name your new pet? ").strip()
		
		pet = Pet(petName, self.petType, 3)	#	Pets hatched from egg have default currentSoul of "neutral"
		pet.loc = self.loc
		
		return pet

class Pet():
	def __init__(self, name, petType, currentSoul):
		self.name = name
		self.type = petType	#	Superficial str only used when displaying info about pet. Has no effect on its attributes or methods or anything 
		self.loc = None
		
		self.alive 		= True
		self.overfed 	= False
		
		self.stages 		= ["baby", "teen", "adult"]
		self.currentStage 	= 0	#	Pet initializes as baby
		
		self.souls 			= ["wretched", "rude", "mischievous", "neutral", "kind", "gallant", "sweetie pie"]
		self.currentSoul 	= currentSoul	#	Used, mainly, to calculate value if selling pet
		
		self.age 		= 0
		self.strikes 	= 0 	#	Get enough (self.strikeMax) strikes and the pet will die
		self.strikeMax 	= 6
		
		#	v Stats are ints. in a range of 1-5
		self.health 	= 5		
		self.connection = 2
		self.stomach 	= 3	
		self.bathroom 	= 1	#	Bathroom > 3 means pet is dirty
		self.happiness 	= 3
		self.mainAttributes = [self.health, self.connection, self.stomach, self.bathroom, self.happiness]
		
		#	v Stats are ints in a range of 1-10
		self.care = 5	#	Unused; would be implemented to determine evolution if an evolution system were implemented for pets
		
		self.myRoomEvent = None	#	For use in die()
		updater.dailyUpdateRegister(self)	#	Make the pet run its dailyUpdate() function when the updater updates everything's dailyUpdate()
		
	
	def dailyUpdate(self):
		self.age += 1
		
		for i in self.mainAttributes:	#	Loop through each attribute stored in mainAttributes...
			i = clamp(i, 1, 5)	#	ensure they're constrained between 1 and 5
		
		self.checkStrikes()
		self.adjustStats()
		self.lifeUpdate()
		# print("Pet Life Update")
		# for i in self.mainAttributes:
		# 	print("attribute " + str(i))
	
	
	def adjustStats(self):
		
		if self.stages[self.currentStage] == "baby":	#	Baby
			healthDecrement = 2
			self.happiness = 1	#	Happiness is set to lowest each day while baby
			stomachDecrement = 2
			self.bathroom = 5	#	Bathroom is set to highest each day while baby
			connectionDecrement = 0
		elif self.stages[self.currentStage] == "teen":	#	Teen
			healthDecrement = 1
			happinessDecrement = 1
			stomachDecrement = 2
			connectionDecrement = 2
		elif self.stages[self.currentStage] == "adult":	#	Adult
			healthDecrement = 1
			happinessDecrement = 1
			stomachDecrement = 1
			connectionDecrement = 1
			
		if self.health > healthDecrement:
			self.health -= healthDecrement
		else:
			#self.alive = False	#	ATTENTION: This seems a lil extreme!
			self.strikes += 1
		
		if self.stomach > stomachDecrement:
			self.stomach -= stomachDecrement
		else:
			self.stomach = 1
		
		if self.connection > connectionDecrement:
			self.connection -= connectionDecrement
		
		if self.stages[self.currentStage] != "baby":
			if self.happiness > happinessDecrement:
				self.happiness -= happinessDecrement

	def checkStrikes(self):
		if self.overfed == True:
			self.strikes += 1
			self.connection -= 1
			
		if self.happiness == 5 and self.bathroom == 1 and self.stomach >= 4:
			if self.strikes > 0:
				self.strikes -= 1	#	Add some leniency - If the pet has full happiness, and doesn't need to use the bathroom, and is mostly full, we'll remove a strike
			
		if self.strikes == self.strikeMax:
			self.alive = False
			self.die()
			print("STRIEK MAX ACHEIEVED, PET ELIMINATED")
			input("cotinue?")
	
	def lifeUpdate(self):
		if self.age < 7 and self.currentStage != 0:	#	Baby lasts from age 0-6
			self.currentStage = 0
		elif self.age >= 7 and self.age <= 21 and self.currentStage != 1:	#	Teen lasts from age 7-21
			self.currentStage = 1
		elif self.age > 21 and self.currentStage !=2 :		#	Adult is age 21+
			self.currentStage = 2	
		
	def returnPetInfoVisualization(self):
		self.mainAttributes = [self.health, self.connection, self.stomach, self.bathroom, self.happiness]
		wDim = os.get_terminal_size()[0]
		attributeNames = ["Health","Connection","Stomach","Bathroom","Happiness"]
		statWLen = len(max(attributeNames, key=len)+ " ")	#	Get the longest stat name
		def returnVisualMeterStr(num, max):
			visStr = "⎨"
			for i in range(max):
				if i <= num - 1:
					visStr += "◼︎"
				else:
					visStr += "◻︎"
			visStr += "⎬"
			return visStr
		
		outStr = "Your pet " + self.type + ", " + self.name.capitalize() +"\n\n"
		#	Creating and appending the attribute meter strings:
		for i in range(len(attributeNames)):	#	For each string in attributeNames...
			attrMeterStr = ""	#	Make a new str
			for j in range(statWLen):	#	For each char j in the longest attribute name...
				if j < len(attributeNames[i]):	#	If the current string position j is less then the length of the current string i in attributeNames...
					attrMeterStr += attributeNames[i][j]	#	Append the character at the current string position j to attrMeterStr
				else:	#	Otherwise (Ie, if the current string position j is GREATER than the length of the current string i in attributeNames)..
					attrMeterStr += " "	#	Append a space
			attrMeterStr += returnVisualMeterStr(self.mainAttributes[i], 5)	#	Append the visual attribute meter
			outStr += attrMeterStr + "\n"	#	Append attrMeterStr and a newline to the output string
		
		outStr += "\n"
		return outStr
	
	def die(self):
		self.loc.removeRoomEvent("pet", self.myRoomEvent)
		updater.dailyUpdateDeregister(self)
		self.loc = None
		print
		
	def feed(self):
		if self.stomach < 5:
			self.stomach += 1	#	Increase stomach
			
			if self.bathroom < 5:	#	Increase bathroom
				self.bathroom += 1
				
			if self.happiness < 5 and self.stomach > 3:	#	Increase happiness
				self.happiness += 1
			return True	
			
		elif self.stomach == 5:	
			self.overfed = True
			
			if self.health > 1:	#	Decrease health
				self.health -= 1
			return False
			
	def play(self):
		if self.stomach > 1:	#	Decrease stomach
			self.stomach -= 1
		else:	#	Cannot play with pet if it's too hungry
			return False
		
		if self.happiness < 5:	#	Increase happiness
			self.happiness += 1
		
		if self.connection < 5:	#	Increase connection
			self.connection += 1
			
		if self.bathroom < 5:
			self.bathroom += 1
			
		return True
	def clean(self):
		if self.bathroom > 1:
			
			if self.bathroom > 3 and self.happiness < 5:	#	Increase happiness if cleaned while dirty
				self.happiness += 1
				
			if self.overfed == True:
				self.overfed = False
				
			self.bathroom = 1
			return True
		else:	#	Cannot clean if pet doesn't need cleaning
			return False
	
	def hug(self):
		if self.happiness < 5:
			if self.currentStage == 0:	#	If pet is a baby...
				self.happiness += 1
				
				if self.connection < 5:
					self.connection += 1
					
			else:	#	It pet is not a baby...
				self.happiness += 0.5
			return True
		else:	#	Cannot hug if happiness is full
			return False