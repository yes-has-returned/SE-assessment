import random
from os import system
from time import sleep
import math
import pygame

def clear():
    system('cls')

global rbiomedata

#extracting data
sample_tile = pygame.transform.scale_by(pygame.image.load("Sample Tile.png"),3)
plains_tile = pygame.transform.scale_by(pygame.image.load("Plains Tile.png"),3)
lforest_tile = pygame.transform.scale_by(pygame.image.load("LForest Tile.png"),3)
forest_tile = pygame.transform.scale_by(pygame.image.load("Forest Tile.png"),3)
dforest_tile = pygame.transform.scale_by(pygame.image.load("DForest Tile.png"),3)
player_pointer = pygame.transform.scale_by(pygame.image.load("Player Pointer.png"),3)
player_outliner = pygame.transform.scale_by(pygame.image.load("Player Outliner.png"),3)
inventory_background = pygame.image.load("Inventory Background.jpg")
exit_button = pygame.transform.scale_by(pygame.image.load("Inventory Exit Button.png"),3)
cursor = pygame.transform.scale_by(pygame.image.load("Cursor.png"),3)
pygame.Surface.set_alpha(inventory_background,50)
rdata = open("gamedata.txt", "r").read().split("//")
rbiomedata = rdata[0].strip("//").split("\n")
ritemdata = rdata[1].strip("//").split("\n")
rentitydata = rdata[2].strip("//").split("\n")

#getting entity data
global entities
entities = {}
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
global itemsd
itemsd = {}
for i in ritemdata:

    temp = i[1].split(",")
    temp = [n.split(";") for n in temp]
    if [""] in temp:    
        temp.remove([""])
    temp = [[n[0],int(n[1])] for n in temp]
    tempdict = {}
    for f in temp:
        tempdict[f[0]] = f[1]
    itemsd[i[0]] = tempdict

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
        self.biomegraphics = {
            "Plains":plains_tile,
            "LForest":lforest_tile,
            "Forest":forest_tile,
            "DForest":dforest_tile
        }
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
        
    def GenerateSurroundings(self,xcor,ycor):
        '''
        Generates surroundings of player
        '''
        self.LoadChunk(xcor-1,ycor)
        self.LoadChunk(xcor+1,ycor)
        self.LoadChunk(xcor,ycor+1)
        self.LoadChunk(xcor,ycor-1)
        self.LoadChunk(xcor,ycor)
    
    
    def GenerateTile(self,tilex,tiley,playerx,playery,originx,originy,tile):
        '''
        Generates an image for a tile at tilex,tiley
        '''
        if tilex == playerx and tiley == playery:
            return [tile,originx,originy,0,0]
        
        else:
            addedy = 0
            addedx = 0
            xqueue = 0
            yqueue = 0
            tempx = tilex
            tempy = tiley
            if tilex > playerx:
                while tempx > playerx:
                    addedx += 60
                    addedy += 30
                    tempx -= 1


            elif tilex < playerx:
                while tempx < playerx:
                    addedx -= 60
                    addedy -= 30
                    tempx += 1


            if tiley > playery:
                while tempy > playery:
                    addedx -= 60
                    addedy += 30
                    tempy -= 1

            elif tiley < playery:
                while tempy < playery:
                    addedx += 60
                    addedy -= 30
                    tempy += 1
            return [tile,originx+addedx,originy+addedy]
        
    def GenerateMap(self,playerx,playery):
        todolist = []
        for i in self.gmap.keys():
            tilex = i[0]
            tiley = i[1]
            temp = self.GenerateTile(tilex,tiley,playerx,playery,640,360,self.biomegraphics[self.gmap[i]])
            todolist.append(temp)
        todolist.sort(key = lambda x:x[2])   
        return todolist


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
        if dir == "a":
            self.xcor -= 1
        elif dir == "d":
            self.xcor += 1
        elif dir == "w":
            self.ycor += 1
        elif dir == "s":
            self.ycor -= 1

    def Search(self):
        '''
        Randomly selects  an item out of the current biome item lootpool
        '''
        lootpool = itemsd[self.currentbiome]
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
        return items

    def CheckInventory(self):
        '''
        Displays the player's inventory
        '''
        return self.inventory

    def PerformAction(self,inp):
        '''
        Performs an action according to the input
        '''
        if inp in ["w","a","s","d"]:
            self.Move(inp)

        elif inp in ["e"]:
            items = self.Search()
            ilist = self.GainItems(items)
            return ilist

        elif inp in ["q"]:
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
pygame.init()
events = pygame.event.get()
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
blackbackground = pygame.Color(0,0,0,50)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("LibreBaskerville-Regular.ttf",12)
cursor = pygame.cursors.Cursor((93, 93), cursor)
pygame.mouse.set_cursor(cursor)
running = True
show_inventory = False

xcor = 640
ycor = 360

#introduction
#main gameplay
s = False
time_elapsed = 0
current_item_displayed = ""
idict = {}
while running:
    if current_item_displayed == "":
        time_elapsed = 0
        if idict != {}:
            item = list(idict.keys())[0]
            current_item_displayed = f"found: {idict[item]}x {item}"
            idict.pop(item)

    if time_elapsed > 2:
        if idict != {}:
            item = list(idict.keys())[0]
            current_item_displayed = f"found: {idict[item]}x {item}"
            idict.pop(item)
            time_elapsed = 0
        else:
            current_item_displayed = ""
            time_elapsed = 0

    item_notif = font.render(current_item_displayed, False, white, black)
    
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] == True:
        P.PerformAction("w")
        T.tick()
        s = True
    elif keys[pygame.K_s] == True:
        P.PerformAction("s")
        T.tick()
        s = True
    elif keys[pygame.K_a] == True:
        P.PerformAction("a")
        T.tick()
        s = True
    elif keys[pygame.K_d] == True:
        P.PerformAction("d")
        T.tick()
        s = True
    elif keys[pygame.K_e] == True:
        items = P.PerformAction("e")
        for i in items:
            if i in idict:
                idict[i] = idict[i] + 1
            else:
                idict[i] = 1
        T.tick()
        s = True
    elif keys[pygame.K_q] == True:
        inv = P.PerformAction("q")
        s = True
        if show_inventory == True:
            show_inventory = False
        elif show_inventory == False:
            show_inventory = True
    M.GenerateSurroundings(P.xcor,P.ycor)
    t = M.GenerateMap(P.xcor,P.ycor)
    for i in t:
        screen.blit(i[0],(i[1],i[2]))
    screen.blit(player_outliner,(xcor,ycor))
    screen.blit(player_pointer,(xcor,ycor-60))
    screen.blit(item_notif,(1100,600))
    if show_inventory == True:
        screen.blit(inventory_background,(0,0))
        screen.blit(exit_button,(1185,0))
    
    pygame.display.update()
    sleep(0.01)
    time_elapsed += 0.01
    if s == True:
        sleep(0.1)
        time_elapsed += 0.1
    screen.fill(black)