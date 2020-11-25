import os
from item import Item

class Seed(Item):
	def __init__(self, name, desc, value, growthDuration, price, quality, radiation, beauty, love):
		super().__init__(name, desc, value)
		self.growthDuration = growthDuration
		self.price = price
		self.quality = quality
		self.radiation = radiation 
		self.beauty = beauty 
		self.love = love
	
	def becomePlant(self):
		# user.items.remove(self)
		# self.loc = None
		plant = Plant(self.name, self.growthDuration, self.price, self.quality, self.radiation, self.beauty, self.love)
		return plant

class Plant:
	def __init__(self, name, growthDuration, price, quality, radiation, beauty, love):
		self.name = name
		self.growthDuration = growthDuration
		self.size = 1
		
		self.price = price
		self.quality = quality
			#	The 3 below variables all influence quality
		self.radiation = radiation
		self.beauty = beauty
		self.love = love
		
		self.age = 0
		self.fullyGrown = False
		self.fertilized = False	#	Makes growth duration lower if the soil it's planted in is fertilized
		self.watered = False
		
	def grow(self):
		if self.watered and not self.fullyGrown:
			if self.age < self.growthDuration:
				self.age += 1
			else:
				self.fullyGrown = True
			
	
