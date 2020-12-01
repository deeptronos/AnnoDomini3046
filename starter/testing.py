import json
# def plantFromSeed(self, seedObject):
# 	plant = seedObject.becomePlant()
# 	for i in range(len(self.dirtPlots)):
# 		if self.dirtPlots[i].growing == None:
# 			self.dirtPlots[i].growing = plant
# 			break
# 			
def testFunc():
	for i in range(12):
		print("jaja")
		if i%2 == 0:
			break

with open('seeds.json') as f:
	data = json.load(f)
	
for i in data:
	
	for j in data[i]:
		for k in data[i][j]:
			for a in data[i][j][k]:
				print(a)
				#print(data[i][j][k]["desc"])
		print()
#print(data["seeds"]["crop"]["democrop"])