updates = []
dailyUpdates = []    #    Separate list of updates that only occur when an in-game "day" ends.

def updateAll():
    for u in updates:
       # print("UPDATE")
        u.update()
    #input("Press enter to continue...")

def register(thing):
    updates.append(thing)

def deregister(thing):
    updates.remove(thing)

def dailyUpdateAll():
    for du in dailyUpdates:
        du.dailyUpdate()
        
def dailyUpdateRegister(thing):
    dailyUpdates.append(thing)

def deregister(thing):
    dailyUpdates.remove(thing)