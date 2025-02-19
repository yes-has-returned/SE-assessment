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
inventory_entry = pygame.image.load("Inventory Entry Button.png")
inventory_entryh = pygame.image.load("Inventory Entry Button Highlighted.png")
item_background = pygame.image.load("Item Background.png")
title_screen = pygame.transform.scale_by(pygame.image.load("Game intro screen.png"),10)
campfire_button = pygame.image.load("Light campfire button.png")
campfire_buttonh = pygame.image.load("Light campfire button hover.png")
global item_graphics
item_graphics = {
    "grass":pygame.transform.scale_by(pygame.image.load("grass.png"),3),
    "rock":pygame.transform.scale_by(pygame.image.load("rock.png"),3),
    "flint":pygame.transform.scale_by(pygame.image.load("flint.png"),3),
    "fertile soil":pygame.transform.scale_by(pygame.image.load("fertile soil.png"),3),
    "iron ore":pygame.transform.scale_by(pygame.image.load("iron ore.png"),3),
    "pebble":pygame.transform.scale_by(pygame.image.load("pebble.png"),3),
    "soil":pygame.transform.scale_by(pygame.image.load("soil.png"),3),
    "stick":pygame.transform.scale_by(pygame.image.load("stick.png"),3),
    "iron nugget":pygame.transform.scale_by(pygame.image.load("Iron Nugget.png"),1.5),
    "energy sword":pygame.transform.scale_by(pygame.image.load("Energy Sword.png"),1.5),
    "green energy sword":pygame.transform.scale_by(pygame.image.load("Green Energy Sword.png"),1.5),
    "hefty stone":pygame.transform.scale_by(pygame.image.load("Hefty Stone.png"),3),
    "pointy stick":pygame.transform.scale_by(pygame.image.load("Pointy Stick.png"),1.7),
    "scythe":pygame.transform.scale_by(pygame.image.load("Scythe.png"),3),
    "dagger":pygame.transform.scale_by(pygame.image.load("Dagger.png"),3),
    "rudimentary spear":pygame.transform.scale_by(pygame.image.load("Rudimentary spear.png"),1.5),
    "rudimentary dagger":pygame.transform.scale_by(pygame.image.load("Rudimentary dagger.png"),1.5),
    "sawdust":pygame.transform.scale_by(pygame.image.load("Sawdust.png"),1.5)
}

cursor = pygame.transform.scale_by(pygame.image.load("Cursor.png"),3)
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

craftingdata = open("craftingdata.txt","r").read().split("\n")
craftingdata = [n.strip("\n") for n in craftingdata]
craftingdata = [n.split(":") for n in craftingdata]
craftingdata = [[n[0],n[1].split(",")] for n in craftingdata]
global craftingdict
craftingdict = {}
for i in craftingdata:
    craftingdict[i[0]] = i[1]



for i in craftingdict.keys():
    temp = []
    for j in craftingdict[i]:
        templist = j.split("x")
        templist[0] = int(templist[0])
        temp.append(templist)
    craftingdict[i] = temp



def button(top_leftx,top_lefty,bottom_rightx,bottom_righty,cursor_posx,cursor_posy):
    if cursor_posx >= top_leftx and cursor_posx <= bottom_rightx and cursor_posy >= top_lefty and cursor_posy <= bottom_righty:
        return True
    
    else:
        return False

def inv_button(top_leftx,top_lefty):
    pass


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
        self.inventory = {"pointy stick":1}
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

    def MakeCampfire(self, num_rocks, num_sticks, num_sawdust, num_clicks):
        campfire_threshold = num_rocks+num_sticks*2+num_sawdust*5+math.floor(num_clicks/10)
        campfire_outcome = random.randint(1,100)
        heat = num_sticks*4
        duration = num_sticks*5+num_rocks*3
        if campfire_threshold >= campfire_outcome:
            return True,heat,duration
        else:
            return False,heat,duration

#game text related things
class GSys:
    def __init__(self):
        self.gamestage = 0
        self.inventory_background = pygame.image.load("Inventory Background.jpg")
        self.exit_button = pygame.transform.scale_by(pygame.image.load("Inventory Exit Button.png"),3)
        self.exit_buttonh = pygame.transform.scale_by(pygame.image.load("Inventory Exit Button Hover.png"),3)
        self.item_display = pygame.transform.scale_by(pygame.image.load("inventory item display.png"),3)
        self.inv_up = pygame.transform.scale_by(pygame.image.load("Inventory Up Arrow.png"),3)
        self.inv_down = pygame.transform.scale_by(pygame.image.load("Inventory Down Arrow.png"),3)
        self.inv_uph = pygame.transform.scale_by(pygame.image.load("Inventory Up Arrow Highlighted.png"),3)
        self.inv_downh = pygame.transform.scale_by(pygame.image.load("Inventory Down Arrow Highlighted.png"),3)
        self.crafting_display = pygame.transform.scale_by(pygame.image.load("crafting item display.png"),3)
        self.crafting_displayh = pygame.transform.scale_by(pygame.image.load("crafting item displayh.png"),3)
        self.craftable_button = pygame.transform.scale_by(pygame.image.load("Craftable button.png"),3)
        self.craftable_buttonh = pygame.transform.scale_by(pygame.image.load("Craftable button hover.png"),3)
        self.uncraftable_button = pygame.transform.scale_by(pygame.image.load("Uncraftable button.png"),3)
        self.uncraftable_buttonh = pygame.transform.scale_by(pygame.image.load("Uncraftable button hover.png"),3)
        self.campfire_exit_button = pygame.transform.scale_by(pygame.image.load("Campfire Exit Button.png"),3)
        self.campfire_exit_buttonh = pygame.transform.scale_by(pygame.image.load("Campfire Exit Button Hover.png"),3)
        self.campfire_background = pygame.image.load("Campfire background.png")
        self.campfire_ui = pygame.image.load("Campfire UI.png")
        self.start_campfire_background = pygame.image.load("Start campfire overlay.png")
        self.recent_craft = None
        self.displaying = {}
        self.displayingcrafting = {}
        self.inv_contents = {}
        self.inv_reopened = True
        self.crafting_reopened = True
        self.campfire_reopened = True
        self.craftable = True
        pygame.Surface.set_alpha(self.start_campfire_background,150)
        pygame.Surface.set_alpha(self.inventory_background,50)

    def updateinventory(self,inv):
        self.inv_contents = inv
    
    def inventoryscreen(self,mouse_posx,mouse_posy,left_pressed):
        screen.blit(self.inventory_background,(0,0))
        starting_y = 50
        if self.inv_reopened == True:
            self.displaying = {}
            if self.inv_contents != {}:
                for i in self.inv_contents:
                    self.displaying[i] = starting_y
                    starting_y += 150
            self.craftable = True
            self.inv_reopened = False
        
        if self.displaying != {}:
            for i in self.displaying:
                
                screen.blit(self.item_display,(50,self.displaying[i]))
                screen.blit(item_graphics[i],(70,self.displaying[i]+20))
                itemtext = futurefont.render(f"{self.inv_contents[i]}x {i}",False,white)
                screen.blit(itemtext,(170,self.displaying[i]+20))
        highlighted = button(500,300,572,363,mouse_posx,mouse_posy)
        if highlighted == True:
            screen.blit(self.inv_uph,(500,300))
            if left_pressed == True:
                for i in self.displaying:
                    self.displaying[i] = self.displaying[i]+150
        else:
            screen.blit(self.inv_up,(500,300))
        highlighted = button(500,400,572,463,mouse_posx,mouse_posy)
        if highlighted == True:
            screen.blit(self.inv_downh,(500,400))
            if left_pressed == True:
                for i in self.displaying:
                    self.displaying[i] = self.displaying[i]-150
        else:
            screen.blit(self.inv_down,(500,400))



        starting_y = 50

        if self.crafting_reopened == True:
            self.displayingcrafting = {}
            if self.craftable == True:
                for i in craftingdict.keys():
                    craft = True
                    for n in craftingdict[i]:
                        if n[1] in self.inv_contents.keys():
                            if n[0] > self.inv_contents[n[1]]:
                                craft = False
                        else:
                            craft = False
                    if craft == True:
                        self.displayingcrafting[i] = starting_y
                        starting_y += 150
            elif self.craftable == False:
                for i in craftingdict.keys():
                    self.displayingcrafting[i] = starting_y
                    starting_y += 150
            self.crafting_reopened = False

        iterable = list(self.displayingcrafting.keys())
        iterable.sort()
        for i in iterable:
            highlighted = button(800,self.displayingcrafting[i],1130,self.displayingcrafting[i]+135,mouse_posx,mouse_posy)
            if highlighted == True:
                screen.blit(self.crafting_displayh,(800,self.displayingcrafting[i]))
                if left_pressed == True:
                    craftable = True
                    for n in craftingdict[i]:
                        if n[1] in self.inv_contents:
                            if n[0] > self.inv_contents[n[1]]:
                                craftable = False
                        else:
                            craftable = False
                    if craftable == True:
                        for n in craftingdict[i]:
                            self.inv_contents[n[1]] = self.inv_contents[n[1]] - n[0]
                            if self.inv_contents[n[1]] == 0:
                                self.inv_contents.pop(n[1])
                        if i in self.inv_contents:
                            self.inv_contents[i] = self.inv_contents[i] + 1
                        else:
                            self.inv_contents[i] = 1
                        self.crafting_reopened = True
                        self.inv_reopened = True
                    
            else:
                screen.blit(self.crafting_display,(800,self.displayingcrafting[i]))
            screen.blit(pygame.transform.scale_by(item_graphics[i],0.5),(800,self.displayingcrafting[i]))                
            screen.blit(futurefont.render(i,False,white),(820,self.displayingcrafting[i]+30))
            recipey = self.displayingcrafting[i]
            for n in craftingdict[i]:
                screen.blit(pygame.transform.scale_by(item_graphics[n[1]],0.4),(975,recipey))
                screen.blit(futurefontS.render(f"{n[0]}x {n[1]}",False,white),(1015,recipey+15))
                recipey += 20
        highlighted = button(700,300,772,363,mouse_posx,mouse_posy)
        if highlighted == True:
            screen.blit(self.inv_uph,(700,300))
            if left_pressed == True:
                for i in self.displayingcrafting:
                    self.displayingcrafting[i] = self.displayingcrafting[i] + 150
        else:                
            screen.blit(self.inv_up,(700,300))
        
        highlighted = button(700,400,772,463,mouse_posx,mouse_posy)
        if highlighted == True:
            screen.blit(self.inv_downh,(700,400))
            if left_pressed == True:
                for i in self.displayingcrafting:
                    self.displayingcrafting[i] = self.displayingcrafting[i] - 150
        else:
            screen.blit(self.inv_down,(700,400))


        highlighted = button(1200,200,1272,263,mouse_posx,mouse_posy)
        if self.craftable == True:
            if highlighted == True:
                screen.blit(self.craftable_buttonh,(1200,200))
                if left_pressed == True:
                    self.craftable = False
                    self.crafting_reopened = True
            else:
                screen.blit(self.craftable_button,(1200,200))
        
        elif self.craftable == False:
            if highlighted == True:
                screen.blit(self.uncraftable_buttonh,(1200,200))
                if left_pressed == True:
                    self.craftable = True
                    self.crafting_reopened = True
            else:
                screen.blit(self.uncraftable_button,(1200,200))
        sleep(0.1)
        highlighted = button(1260,0,1280,27,mouse_posx,mouse_posy)
        if highlighted == True:
            screen.blit(self.exit_buttonh,(1185,0))
            if left_pressed == True:
                self.inv_reopened = True
                self.crafting_reopened = True
                return False
                
            else:
                return True
        else:
            screen.blit(self.exit_button,(1185,0))
            return True

    def campfire_screen(self):
        if self.campfire_reopened == True:
            self.campfire_reopened = False
            self.fade_in(None,self.campfire_background,black)
        screen.blit(self.campfire_background,(0,0))

    def fade_in(self,img1,img2,backingcolor,mode="separate",xcor=0,ycor=0):
        img1copy = img1
        img2copy = img2
        img1alpha = 255
        img2alpha = 0
        secs = 3
        repeats = int(secs/0.01)
        alphachange = 255/repeats
        if mode == "separate":
            if img1 != None:
                for i in range(repeats):
                    pygame.event.pump()
                    screen.fill(backingcolor)
                    img1copy.set_alpha(img1alpha)
                    screen.blit(img1copy,(xcor,ycor))
                    img1alpha -= alphachange
                    pygame.display.update()
                    sleep(0.005)
                screen.fill(backingcolor)
            if img2 != None:
                for i in range(repeats):
                    pygame.event.pump()
                    screen.fill(backingcolor)
                    img2copy.set_alpha(img2alpha)
                    screen.blit(img2copy,(xcor,ycor))
                    img2alpha += alphachange
                    pygame.display.update()
                    sleep(0.005)
                screen.blit(img2,(xcor,ycor))
        elif mode == "together":
            for i in range(repeats):
                pygame.event.pump()
                screen.fill(backingcolor)
                img1copy.set_alpha(img1alpha)
                img2copy.set_alpha(img2alpha)
                img1alpha -= alphachange
                img2alpha += alphachange
                screen.blit(img1copy,(xcor,ycor))
                screen.blit(img2copy,(xcor,ycor))
                pygame.display.update()
                sleep(0.01)
            screen.blit(img2,(xcor,ycor))
    
    def start_campfire_UI(self,mouse_posx,mouse_posy,left_pressed):
        screen.blit(self.start_campfire_background,(0,0))
        highlighted = button(1260,0,1280,27,mouse_posx,mouse_posy)
        if highlighted == True:
            screen.blit(self.campfire_exit_buttonh,(1185,0))
            if left_pressed == True:
                return False
                
            else:
                return True
        else:
            screen.blit(self.campfire_exit_button,(1185,0))
            return True


        

        
        
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
battlebackground = pygame.Color(76,153,0)
blackbackground = pygame.Color(0,0,0,50)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("LibreBaskerville-Regular.ttf",12)
futurefont = pygame.font.Font("Netron .otf",12)
futurefontS = pygame.font.Font("Netron .otf",10)
futurefontL = pygame.font.Font("Netron .otf",15)
cursor = pygame.cursors.Cursor((93, 93), cursor)
pygame.mouse.set_cursor(cursor)
running = True
player_pointer_offset_change = -0.5
start_campfire_screen = False
lighting_campfire_screen = False
show_title = False


xcor = 640
ycor = 360

#Title screen


#introduction
frame1 = pygame.transform.scale_by(pygame.image.load("Intro frame 1.png"),3)
text1 = "Once upon a time, there was a land of only sky."
introduction = False

if show_title == True:
    G.fade_in(None,title_screen,black,)
else:
    print("The title screen loading animation has been blocked by show_title on line 679")

not_clicked = True
mode = "subtract"
shown = True
secs = 0
while not_clicked:
    screen.blit(title_screen,(0,0))
    if secs >= 0.2:
        if shown == True:
            shown = False
        elif shown == False:
            shown = True
        secs = 0
    if shown:
        continuetext = futurefontL.render("Click anywhere to continue:",False,white)
        screen.blit(continuetext,(500,650))

    pygame.event.pump()
    mousepress = pygame.mouse.get_pressed()
    if mousepress[0] == True:
        not_clicked = False
    sleep(0.01)
    secs += 0.01
    pygame.display.update()
    screen.fill(black)
while introduction:
    pass


#main gameplay
s = False
time_elapsed = 0
current_item_displayed = ""
idict = {}
displaying = None
inbattle = False
show_inventory = False
campfire_lit = False
player_pointer_offset = 0

G.updateinventory(P.inventory)
while running:
    if current_item_displayed == "":
        time_elapsed = 0
        if idict != {}:
            item = list(idict.keys())[0]
            current_item_displayed = f"found: {idict[item]}x {item}"
            displaying = item

            idict.pop(item)

    if time_elapsed > 2:
        if idict != {}:
            item = list(idict.keys())[0]
            current_item_displayed = f"found: {idict[item]}x {item}"
            idict.pop(item)
            time_elapsed = 0
            displaying = item
        else:
            current_item_displayed = ""
            displaying = None
            time_elapsed = 0

    item_notif = futurefont.render(current_item_displayed, False, white, black)
    
    pygame.event.pump()
    if campfire_lit == True:
        G.campfire_screen()
    else:
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
            G.updateinventory(P.inventory)
            T.tick()
            s = True
        elif keys[pygame.K_q] == True:
            inv = P.PerformAction("q")
            s = True
            if show_inventory == True:
                G.inv_reopened = True
                G.crafting_reopened = True
                show_inventory = False
            elif show_inventory == False:
                show_inventory = True
        M.GenerateSurroundings(P.xcor,P.ycor)
        t = M.GenerateMap(P.xcor,P.ycor)
        for i in t:
            screen.blit(i[0],(i[1],i[2]))
        screen.blit(player_outliner,(xcor,ycor))
        screen.blit(player_pointer,(xcor,ycor-60+player_pointer_offset))
        screen.blit(item_notif,(1100,650))
        if displaying != None:
            screen.blit(item_graphics[displaying],(1000,600))
        mousepos = pygame.mouse.get_pos()
        mousepress = pygame.mouse.get_pressed()
        leftbutton = mousepress[0]
        middlebutton = mousepress[1]
        rightbutton = mousepress[2]
        mousex = mousepos[0]
        mousey = mousepos[1]
        if show_inventory == True:
            show_inventory = G.inventoryscreen(mousex,mousey,leftbutton)
            P.inventory = G.inv_contents
        elif start_campfire_screen == True:
            start_campfire_screen = G.start_campfire_UI(mousex,mousey,leftbutton)
        elif lighting_campfire_screen == True:
            pass
        else:
            screen.blit(inventory_entry,(30,500))
            highlighted = button(30,504,140,546,mousex,mousey)
            if highlighted == True:
                screen.blit(inventory_entryh,(30,500))
                if leftbutton == True:
                    show_inventory = True
            else:
                screen.blit(inventory_entry,(30,500))
            highlighted = button(30,564,140,606,mousex,mousey)
            if highlighted == True:
                screen.blit(campfire_buttonh,(30,560))
                if leftbutton == True:
                    start_campfire_screen = True
            else:
                screen.blit(campfire_button,(30,560))
        
    player_pointer_offset += player_pointer_offset_change
        
    if player_pointer_offset <= -20 or player_pointer_offset >= 50:
        player_pointer_offset_change *= -1
    pygame.display.update()
    sleep(0.01)
    if s == True:
        sleep(0.09)
        s = False
        player_pointer_offset += 9*player_pointer_offset_change
    time_elapsed += 0.1
    screen.fill(black)