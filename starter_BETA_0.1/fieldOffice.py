from NPC import BountyHunter
import updater

import math, random

class FieldOffice():
	def __init__(self, name):
		self.loc = None
		self.fieldOfficeName = name
		self.possibleSeeds = []
		self.hunter = None	#	There is one "new" hunter generated randomly every day
		self.playerWager = 0
		updater.dailyUpdateRegister(self)
		
	def dailyUpdate(self):
		self.generateHunter()
		self.playerWager = 0
		
	def putInRoom(self, room):
		self.loc = room
		
	def generateHunter(self):
		possibleNames = ["Keith","Skid", "Bartholemew", "Homer", "Marjorie", "Lisa", "Balthazar", "Nima", "Hassan", "Bora", "Ari", "Stanislova"]
		name = random.choice(possibleNames)
		maxPrice = random.randint(1500, 4500)
		reliability = random.randint(1, 10) 
		age = random.randint(4, 90)
		newHunter = BountyHunter(name, maxPrice, reliability, age)
		self.hunter = newHunter
		
	def returnFieldOfficeInfo(self):
		if self.hunter != None:
			trust = ["Unreliable", "Sly", "Suspicous", "Reliable", "Pure-hearted"]
			trustIndex = int( ( (self.hunter.reliability - 1)/len(trust) ) * (len(trust)/2) )
			returnStr = "Today, we have "
			returnStr += self.hunter.name + " working for us. They are a " + trust[trustIndex] + " hunter.\n"
			returnStr += self.hunter.name +" says you'll have to put up L$" + str(self.hunter.maxPrice) + " to guarantee a return, but putting up less will still give you an appropriately reduced chance at getting something from their expedition."
			return returnStr
		else:
			return "There isn't a hunter working today. Come back another time!"
	
	def putUpWager(self, amount):
		self.playerWager = amount
	def cancelWager(self):
		self.playerWager = 0
		
	def doHunt(self):
		stats = self.hunter.prepareStatsForHunt(self.playerWager)	#	list containing [wagerProbability, adjustedReliability]
		results = self.hunter.hunt(stats[0], stats[1])
		
		if not results:
			print("Hunt was unsuccessful.")
		else:
			loyalty = results[3]
			huntedSeed = random.choice(self.possibleSeeds)
			print("Wow! " + self.hunter.name + " identified a " + huntedSeed.name +" in the wasteland outside the colony!")
			if loyalty == "Loyal":
				# you get teh seed
				print(self.hunter.name + " brought it safely back to you.")
				return huntedSeed
			elif loyalty == "Betrayal":
				print("...but they asconded with it for themselves!")
				return False
				
			print(stats)
			print(results)
