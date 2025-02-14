import random
from os import system
from time import sleep
import math

def clear():
    system('cls')

global rbiomedata

#extracting data
rdata = open("gamedata.txt", "r").read().split("//")
rbiomedata = rdata[0].strip("//").split("\n")
ritemdata = rdata[1].strip("//").split("\n")
rentitydata = rdata[2].strip("//").split("\n")

#getting entity data
global entities
entities = {}
rentitydata.remove('')
rentitydata.remove('')
for i in rentitydata:
    temp = i.split(":")
    name = temp[0]
    temp2 = temp[1].split(",")
    temp2 = [n.split(";") for n in temp2]
    temp2 = [[n[0],int(n[1])] for n in temp2]
    tempdict = {}
    for i in temp2:
        tempdict[i[0]] = i[1]
    entities[name] = tempdict

#getting biomes
rbiomedata.remove('')
rbiomedata = [i.strip("\n").split(":") for i in rbiomedata]
biomes = rbiomedata.pop(-1)
biomes = biomes[1]
biomes = biomes.split(",")

#getting item data
ritemdata.remove('')
ritemdata.remove('')
ritemdata = [n.split(":") for n in ritemdata]
global items
items = {}
for i in ritemdata:

    temp = i[1].split(",")
    temp = [n.split(";") for n in temp]
    if [""] in temp:    
        temp.remove([""])
    temp = [[n[0],int(n[1])] for n in temp]
    tempdict = {}
    for f in temp:
        tempdict[f[0]] = f[1]
    items[i[0]] = tempdict

#getting biome description data
data = {}
for i in rbiomedata:
    data[i[0]] = i[1]

#map related things
class GameMap:
    def __init__(self,biomes):
        self.gmap = {(0,0):random.choice(biomes)}
        self.leveltobiome = {}
        self.biometolevel = {}
        self.biomeslist = []
        biome_level = 0
        for i in biomes:
            self.leveltobiome[biome_level] = i
            self.biometolevel[i] = biome_level
            self.biomeslist.append(i)
            biome_level += 1
        self.max_level = biome_level - 1

    def LoadChunk(self,xcor,ycor):
        '''
        Loads a chunk if it was already generated, and generates a chunk if it has not been generated
        '''
        if (xcor,ycor) in self.gmap.keys():
            return self.gmap[(xcor,ycor)]
        else:
            adj_cords = [(xcor-1,ycor),(xcor+1,ycor),(xcor,ycor-1),(xcor,ycor+1)]
            adj_levels = []
            for i in adj_cords:
                if i in self.gmap.keys():
                    adj_levels.append(self.biometolevel[self.gmap[i]])
            if adj_levels == []:
                outputbiome = random.choice(self.biomeslist)
                self.gmap[(xcor,ycor)] = outputbiome
            else:
                possible_levels = []
                for i in adj_levels:
                    possible_levels.append(i)
                    if i > 0:
                        possible_levels.append(i-1)
                    if i < self.max_level:
                        possible_levels.append(i+1)
                outputbiome = self.leveltobiome[random.choice(possible_levels)]
                self.gmap[(xcor,ycor)] = outputbiome
            return outputbiome
        
    def GenerateDesc(self,xcor,ycor,night):
        '''
        Generates description based on the biomes around the player.
        '''
        left=self.LoadChunk(xcor-1,ycor)
        right=self.LoadChunk(xcor+1,ycor)
        up=self.LoadChunk(xcor,ycor+1)
        down=self.LoadChunk(xcor,ycor-1)
        current=self.LoadChunk(xcor,ycor)
        templist = {"\33[1;49;36m To your left \33[0;49;37m":data[left+"Adj"],
                    "\33[1;49;36m To your right \33[0;49;37m":data[right+"Adj"],
                    "\33[1;49;36m Further in front of you \33[0;49;37m":data[up+"Adj"],
                    "\33[1;49;36m Further behind you \33[0;49;37m":data[down+"Adj"]}
        descstr = ""
        if night == False:
            descstr+=data[current+random.choice(["","2"])]
        elif night == True:
            descstr+=data[current+"N"]
        shared = []
        not_shared = list(templist.keys())
        while len(not_shared) > 1:
            i = not_shared[0]
            other = not_shared[1:]
            temp = [i]
            for n in other:
                if templist[i] == templist[n]:
                    temp.append(n)
            for n in temp:
                not_shared.remove(n)
            shared.append(temp)
        if len(not_shared) == 1:
            shared.append([not_shared[0]])
        for n in shared:
            for m in range(len(n)):
                if m == 0:
                    descstr += n[m]
                elif m == len(n)-1:
                    descstr += f"and{n[m].lower()}"
                else:
                    descstr+=f",{n[m].lower()}"
            descstr+=templist[n[0]]
                

        return descstr

#time related things
class Timer:
    def __init__(self):
        self.time = random.randint(5,8)
        self.timeperiod = "morning"
    
    def update(self,val):
        '''
        Changes the time and time period according to the value given
        '''
        self.time = val
        if self.time >=3 and self.time <=4:
            self.timeperiod = "dawn"
        
        elif self.time >= 5 and self.time <= 11:
            self.timeperiod = "morning"
        
        elif self.time == 12:
            self.timeperiod = "noon"

        elif self.time >= 13 and self.time <= 17:
            self.timeperiod = "afternoon"
        
        elif self.time >= 18 and self.time <= 20:
            self.timeperiod = "evening"

        elif self.time >= 21 and self.time <= 23:
            self.timeperiod = "night"

        elif self.time == 0:
            self.timeperiod = "midnight"

        else:
            self.timeperiod = "night"

    def tick(self):
        '''
        passes 1 hour
        '''
        if self.time == 23:
            self.time=-1
        self.update(self.time+1)

    def timebasedmessage(self):
        '''
        displays the current in-game time
        '''
        if self.timeperiod == "night":
            return "\33[1;49;31m You should probably find shelter. \33[0;49;37m"
        
        elif self.timeperiod == "midnight":
            return "\33[1;49;31m Find shelter NOW. \33[0;49;37m"
        
        elif self.timeperiod == "dawn":
            return "\33[1;49;33m After a long, sleepless night, you feel a creeping sense of hope. \33[0;49;37m"
        
        elif self.timeperiod == "morning":
            return "\33[1;49;33m The morning comes, a new hope after a dark night. \33[0;49;37m"
        
        elif self.timeperiod == "noon":
            return "\33[1;49;37m The midday sun illuminates the world, and you feel a temporary sense of peace. \33[0;49;37m"
        
        elif self.timeperiod == "afternoon":
            return "\33[1;49;37m The day starts to close, you should start heading for shelter now. \33[0;49;37m"
        
        elif self.timeperiod == "evening":
            return "\33[1;49;33m The day draws to a close and the noises grow closer. You should find shelter soon. \33[0;49;37m"

    def displaytime(self):
        return f"{self.time}00 ({self.timeperiod})"

#player related things
class Player:
    def __init__(self,biome):
        self.xcor = 0
        self.ycor = 0
        self.currentbiome = biome 
        self.inventory = {}
        self.searchtimes = 5

    def Move(self,dir):
        '''
        Moves the player in a certain direction
        '''
        if dir == "left":
            self.xcor -= 1
        elif dir == "right":
            self.xcor += 1
        elif dir == "up":
            self.ycor += 1
        elif dir == "down":
            self.ycor -= 1

    def Search(self):
        '''
        Randomly selects  an item out of the current biome item lootpool
        '''
        lootpool = items[self.currentbiome]
        obtained = []
        for t in range(self.searchtimes):
            lootpossibility = []
            for i in lootpool.keys():
                for n in range(lootpool[i]):
                    lootpossibility.append(i)
            obtained.append(random.choice(lootpossibility))
        return obtained
    
    def GainItems(self,items):
        '''
        Takes a list of items and adds them to player inventory
        '''
        for i in items:
            print(f"+{i}")
            if i in self.inventory.keys():
                self.inventory[i] = self.inventory[i]+1
            else:
                self.inventory[i] = 1

    def CheckInventory(self):
        '''
        Displays the player's inventory
        '''
        print("~INVENTORY~")
        for i in self.inventory.keys():
            print(f"{self.inventory[i]}x {i}")

    def PerformAction(self,inp):
        '''
        Performs an action according to the input
        '''
        if inp in ["up","down","left","right"]:
            self.Move(inp)

        elif inp in ["search"]:
            items = self.Search()
            self.GainItems(items)

        elif inp in ["inv","checkinventory","inventory"]:
            self.CheckInventory()

#game text related things
class GSys:
    def __init__(self):
        self.gamestage = 0

    def notif(self, text, continuetext="<PRESS ENTER TO CONTINUE>"):
        print(text)
        input(continuetext)
        clear()

#entity encounter related things
class EntitySys:
    def __init__(self):
        pass

    def generate_encounter(self,time,biomelevel):
        encounterchance = biomelevel*time
        nothingchance = 24*4-encounterchance
        val = random.randint(int(nothingchance))
        if val <= encounterchance:
            point_alloc = abs(12-time)
            if point_alloc < 6:
                point_alloc = math.ceil(point_alloc/2)
            point_alloc = int(math.floor(int(point_alloc*biomelevel)*random.choice([0.5,1,2])))
            possible_entities = entities.keys()
            spawned_entities = []
            while point_alloc > 0:
                for i in possible_entities:
                    if entities[i]['spawn'] > point_alloc:
                        possible_entities.remove(i)
                spawned_entities.append(random.choice(possible_entities))
            return possible_entities
        else:
            return []



#initiating classes
M = GameMap(biomes)
P = Player(M.gmap[(0,0)])
T = Timer()
G = GSys()


#introduction
#main gameplay
while True:
    print(T.displaytime())
    print(M.GenerateDesc(P.xcor,P.ycor,False))
    print(T.timebasedmessage())
    action = input(">> ").lower()
    P.PerformAction(action)
    T.tick()