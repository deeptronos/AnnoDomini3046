import os
import random
from item import Item
import updater

#	Plant Types: Crop, Flower, Illicit, Rare, Test (non-obtainable in game)

def clamp(n, minN, maxN):
	return max(min(maxN, n), minN)

def mapRange(n, inMaxN, rangeMaxN):	#	Maps n (a number between 0 and inMaxN) to a number between 0 and rangeMaxN
	return (n / float(inMaxN) * rangeMaxN)

class Seed(Item):	#	Making a seed item
	def __init__(self, name, desc, value, growthDuration, price, plantPrice, radiation, exotic=False, plantType="Crop"):
		super().__init__(name, desc, value)
		self.growthDuration = growthDuration
		self.price = price
		self.radiation = radiation 
		self.exotic = exotic
		self.plantPrice = plantPrice	#	The price of the fully-grown plant
		self.plantType = plantType
		
	def becomePlant(self):
		def nameProcess(seedName):	#	Turn the seed's name in to a proper plant name (just by removing the "seed" at the end of the seed's name)
			split = seedName.split()
			split.pop(len(split) - 1)
			returnStr = ""
			for i in split:
				returnStr += i.capitalize() + " "
			return returnStr
			
		plantName = nameProcess(self.name)
		
		plant = Plant(plantName, self.growthDuration, self.price, self.plantPrice, self.radiation, self.exotic, self.plantType)
		return plant

class Plant:
	def __init__(self, name, growthDuration, price, maxPrice, radiation, exotic, plantType):
		self.name = name
		self.growthDuration = growthDuration	#	Maximum is 45 days
		self.size = 1
		
		self.price = price	#	Price will initially be the same as the seed item's price
		self.plantMaxValue = maxPrice	#	The maximum value of the plant
		self.grades = ['poor', 'average', 'good', 'excellent', 'divine']
		self.currentGrade = 1 #	currentGrade has a default of 'average'
		self.plantType
			#	The 4 below variables all influence grade
		self.radiation = clamp(radiation, 1, 10)	#	radiation is int between 1 and 10
		self.beauty = 0	#	Initializing with 0 beauty; beauty is int between 0 and 10
		self.love = 50	#Initializing with 50 love; love is int between 0 and 100
		self.exotic = exotic	#Bool
		
		self.age = 0	#	Duration of game days alive
		self.daysWatered = 0	#	Amount of days on which the plant was watered - used in conjunction with age to calculate love
		self.fullyGrown = False
		self.fertilized = False	#	Makes growth duration lower if the soil it's planted in is fertilized
		self.waterable, self.wateredToday = True, False
		self.luck = random.randint(1, 10) * self.radiation	#	Future: Maybe make min of luck a variable? Add leveling system for player which includes increasing the min of a plant's possible luck?
			#	Max: 10 * 10 = 100
			#	Min: 1 * 1 = 1
		self.luck = round(mapRange(self.luck, 100, 10))	#	Map self.luck from a number between 0 and 100 to a number between 0 and 10
		
		updater.dailyUpdateRegister(self)
		
	def dailyUpdate(self):	#	Happens at the end of every day
		self.grow()
		if self.age > 2:	#	Grade only calculates when plant is more than 2 days old
			self.calculateGrade()
		self.wateredToday = False
		
	def calculateGrade(self):
		self.love = self.daysWatered * (self.daysWatered / self.age)	#	Calculate love based player's care of plant
			#	Max of the possible values: self.age * (self.age / self.age)  = self.age >>> Scenario if player has watered the plant every day since it's been planted
		if self.wateredToday:
			self.love += self.luck
		self.love = mapRange(self.love, self.age + self.luck, 100)	#	Map love from a number, between 0 and the sum of the age of the plant and the plant's luck, to a number between 0 and 100
		#	^	This intentionally rewards both a lucky random.randint() and caring for the plant daily
		
		self.beauty = (self.love * self.age)/self.radiation		#	Age will probably be more than radiation
			#	Max of the values in this calculation: (100 * 45)/10 = 450
			#	Max possible calculation: (100 * 45) / 1 = 4500 >>>> therefore, self.love * self.age is max 
			#	Min of the values in this calculation/Min possible calculation: (0 * 0) /1 = 0
		self.beauty = mapRange(self.beauty, (self.love * self.age), 100)	#	Map beauty from a number between 0 and the product of love and age to a number between 0 and 100
		self.currentGrade = (self.beauty + self.luck)
			#	Max possible values in this calculation: (100 + self.luck)
		self.currentGrade = int(mapRange(self.currentGrade, (100 + self.luck), 4))	#	Map currentGrade from a number, between 0 and the sum of the maximum possible beauty and the plant's luck, to a number (integer) between 0 and 4
		
	def grow(self):
		print("grow()")
		input("press enter...")
		if self.watered and not self.fullyGrown:
			if self.age < self.growthDuration:
				self.age += 1
			else:
				self.fullyGrown = True
				self.waterable = False
				
	def watered(self):
		if self.waterable and not self.wateredToday:
			self.daysWatered += 1
			self.wateredToday = True
		
	def returnCompletedPlant(self):
		if self.fullyGrown:
			return CompletedPlant(self.name, "test desc", self.price, self.currentGrade, self.plantType)
		return False
	
class CompletedPlant(Item):
	def __init__(self, name, desc, value, grade, type):
		super().__init__(name, desc, value)
		self.grade = grade
		self.type = type
	
