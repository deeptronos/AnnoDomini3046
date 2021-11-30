from plant import mapRange, clamp
import random

class BountyHunter():
	def __init__(self, name, maxPrice, reliability=5, age=20):
	
		self.name = name
		self.location =  None
		self.age = age
		
		self.maxPrice = maxPrice
		self.reliability = reliability	#	int between 1 and 10. Determines how likely they are to not betray you (lower reliability = more likely to betray)
		
		self.itemObtained = False
		self.items = []
		
	def prepareStatsForHunt(self, wager):
		adjustedWager = clamp(wager, 1, self.maxPrice)	#	Restrict wager to be between 1 and the maximum price of the hunter
		wagerProbability = round(mapRange(adjustedWager, self.maxPrice, 100), 2)	#	Map the restricted wager from a value between 0 and self.maxPrice to a value between 0 and 100, to get the percentage chance that the hunter will succeed.
		
		#	The more fully you fund a bounty hunter, the more reliable they become.
		if wagerProbability >= 90:
			adjustedReliability = 10
		elif wagerProbability >= 75: 
			adjustedReliability = clamp(self.reliability + ((10 - self.reliability)/2), self.reliability, 10)	#	decrease unreliability by 50% and clamp it into acceptable zone
		elif wagerProbability >= 50:
			adjustedReliability = clamp(self.reliability + ((10 - self.reliability)/3), self.reliability, 10)	#	decrease unreliability by ~33% and clamp it into acceptable zone
		elif wagerProbability >= 35:
			adjustedReliability = clamp(self.reliability + ((10 - self.reliability)/4), self.reliability, 10)	#	decrease unreliability by 25% and clamp it into acceptable zone
		else:
			adjustedReliability = self.reliability
		
		adjustedReliability = round(adjustedReliability, 2)	
		return[wagerProbability, adjustedReliability]
		
	def hunt(self, wagerProbability, adjustedReliability):
		
		huntPotentials = ["Nothing", "Success"]
		
		#huntResult = random.choices(huntPotentials, weights=[(100 - wagerProbability), wagerProbability], k=100)
		#huntResult = random.choice(huntResult)	#	I think you may be able to make choice() redundant by runnning choices() without the 'k' parameter set, but I haven't tested it thouroughly enough to be confident in that working, so we're doing this for now.
		huntResult = random.choices(huntPotentials, weights=[(100 - wagerProbability), wagerProbability])[0]
		if huntResult== "Success":
			
			reliabilityPotentials = ["Betrayal","Loyal"]
		#betrayal = random.choices(reliabilityPotentials, weights=[(10 - adjustedReliability), adjustedReliability], k = 10)
		#betrayal = random.choice(betrayal)	#	Again, running choice() on choices() may be redundant, but see above.
			betrayalResult = random.choices(reliabilityPotentials, weights=[(10 - adjustedReliability), adjustedReliability])[0]	#	Ignore the above comments, I think this'll work :P
			
			return [wagerProbability, adjustedReliability, huntResult, betrayalResult]
		else:
			return False
	