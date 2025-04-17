global item_graphics
global fading_in

import random
from os import system
from time import sleep
import math
import pygame
from pluralizer import Pluralizer
import classes


#extracting data

player_pointer = pygame.transform.scale_by(pygame.image.load("Player Pointer.png"),3)
player_outliner = pygame.transform.scale_by(pygame.image.load("Player Outliner.png"),3)
inventory_entry = pygame.image.load("Inventory Entry Button.png")
inventory_entryh = pygame.image.load("Inventory Entry Button Highlighted.png")
item_background = pygame.image.load("Item Background.png")
title_screen = pygame.transform.scale_by(pygame.image.load("Game intro screen.png"),10)
campfire_button = pygame.image.load("Light campfire button.png")
campfire_buttonh = pygame.image.load("Light campfire button hover.png")
respawn_screen = pygame.transform.scale_by(pygame.image.load("Death Screen.png"),2)
respawn_button = pygame.image.load("Respawn Button Unclicked.png")
respawn_buttonh = pygame.image.load("Respawn Button Clicked.png")
cursor = pygame.transform.scale_by(pygame.image.load("Cursor.png"),3)

#map related things






#initiating classes

A = classes.AudioSys()

pluralizer = Pluralizer()
pygame.init()
events = pygame.event.get()
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
tutorial_green = pygame.Color(108, 245, 0)
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

show_title = True
fading_in = [False,0,(0,0)]

xcor = 640
ycor = 360

#Title screen


#introduction
introduction_text = ["","Once upon a time, there was a land of only sky.", "It was home to a civilisation of beings, not unlike our own.", "And, just like us, they were plagued by a large problem.", "War.", "And, one day, a war broke out too big to contain... splitting the world in two.", "In one desperate attempt to save their dying civilisation, they took to the stars.", "Hoping that one day they might find another planet to live on."]
A.pause_time_ambience()

if show_title == True:
    A.get_music("Title")
    secs = 3
    repeats = int(secs/0.01)
    alphachange = 255/repeats
    showing_title = True
    imgdisp = title_screen
    alph = 0
    days_played = 0
    for i in range(repeats):
        pygame.event.pump()
        screen.fill(black)
        imgdisp.set_alpha(alph)
        screen.blit(imgdisp,(0,0))
        alph += alphachange
        pygame.display.update()
        left_click = pygame.mouse.get_pressed(3)[0]
        if left_click == True:
            break
        sleep(0.005)
    

else:
    print("The title screen loading animation has been blocked by show_title")

not_clicked = True
mode = "subtract"
shown = True
secs = 0
while not_clicked:
    screen.blit(title_screen,(0,0))
    if secs >= 0.5:
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
A.get_effect("Select1")
A.end_music()
time_elapsed = 0
screen.fill(black)
pygame.display.update()
sleep(1)

for i in introduction_text:
    
    mousepress = pygame.mouse.get_pressed(3)[0]
    intro_text = futurefontL.render(i,False,white,black)
    screen.fill(black)
    screen.blit(intro_text,(300,300))
    pygame.display.update()
    sleep(0.2)
    while time_elapsed <= 1.5:
        mousepress = pygame.mouse.get_pressed(3)[0]
        if mousepress == True:
            A.get_effect("Select1")
            break
        sleep(0.001)
        time_elapsed += 0.001
    pygame.event.pump()
    time_elapsed = 0

tutorial_text = ["Booting up training system 65Dx5>> ", "BOOTING UP 50% [REMINDER: you can hold left click to skip the intro and tutorial]", "Training system fully booted", "Welcome cadet", "Today will be the final day of your training", "We will be going through a summary of everything you've learned.", "Use WASD to move", "And E to search for things", "You may need to check your inventory for useful materials", "And, in case of landing on a hostile planet, make sure to make a campfire before dark.","Good luck cadet."]

for i in tutorial_text:
    
    mousepress = pygame.mouse.get_pressed(3)[0]
    intro_text = futurefontL.render(i,False,tutorial_green,black)
    screen.fill(black)
    screen.blit(intro_text,(300,300))
    pygame.display.update()
    sleep(0.2)
    while time_elapsed <= 1.5:
        mousepress = pygame.mouse.get_pressed(3)[0]
        if mousepress == True:
            A.get_effect("Select1")
            break
        sleep(0.001)
        time_elapsed += 0.001
    pygame.event.pump()
    time_elapsed = 0



while running:
    M = classes.GameMap(classes.biomes)
    P = classes.Player(M.gmap[(0,0)])
    T = classes.Timer()
    G = classes.GSys(A)
    E = classes.EntitySys()
    F = classes.FightSys()
    G.campfire_start_shown = False
    G.campfire_ui_shown = False
    #main gameplay
    s = False
    time_elapsed = 0
    enc_time_elapsed = 0
    current_item_displayed = ""
    result_notif = ""
    idict = {}
    displaying = None
    inbattle = False
    campfire_lit = False
    player_pointer_offset = 0
    dev_access = False
    alive = True
    enemies_faced = {}
    enc = []
    hploss = 0
    if dev_access:
        print("Developer mode is currently on. To enjoy the game properly, please change dev_access to False")
        for i in classes.item_graphics:
            P.inventory[i] = 99

    G.updateinventory(P.inventory)
    A.unpause_time_ambience()
    A.get_time_ambience(T.time)

    while alive:
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

        if enc_time_elapsed > 2 or enemies_faced != None:
            if enemies_faced != None:
                enemies_n = ""
                for i in enemies_faced:
                    enemies_n += f"{enemies_faced[i]}x {pluralizer.pluralize(i,enemies_faced[i],False)}, "
                result_notif = "You encountered: " + enemies_n + " and lost " + str(hploss) + "health."
                enemies_faced = None
                enc_time_elapsed = 0
            else:
                result_notif = ""
            

        item_notif = futurefont.render(current_item_displayed, False, white, black)
        time_notif = futurefont.render(T.timeperiod, False, white, black)
        heart_notif = futurefont.render(f"HP: {P.values["hp"]}", False, white, black)
        result_notif2 = futurefont.render(result_notif,False, white, black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                alive = False
        if G.campfire_ui_shown == True:
            A.pause_time_ambience()
            mousex, mousey = pygame.mouse.get_pos()
            mousepress = pygame.mouse.get_pressed(3)[0]
            temp = G.campfire_screen(mousex, mousey, mousepress)
            if temp != True:
                G.campfire_ui_shown = False
                fading_in = temp
            print(temp)
            A.unpause_time_ambience()
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
                if G.inv_shown == True:
                    G.inv_reopened = True
                    G.crafting_reopened = True
                    G.inv_shown = False
                elif G.inv_shown == False:
                    G.inv_shown = True
            P.currentbiome = M.GenerateSurroundings(P.xcor,P.ycor)
            t = M.GenerateMap(P.xcor,P.ycor)
            for i in t:
                screen.blit(i[0],(i[1],i[2]))
            screen.blit(player_outliner,(xcor,ycor))
            screen.blit(player_pointer,(xcor,ycor-60+player_pointer_offset))
            screen.blit(time_notif,(1100,0))
            screen.blit(item_notif,(1100,650))
            screen.blit(heart_notif,(0,0))
            screen.blit(result_notif2,(0,325))
            if displaying != None:
                screen.blit(classes.item_graphics[displaying],(1000,600))
            mousepos = pygame.mouse.get_pos()
            mousepress = pygame.mouse.get_pressed()
            leftbutton = mousepress[0]
            middlebutton = mousepress[1]
            rightbutton = mousepress[2]
            mousex = mousepos[0]
            mousey = mousepos[1]
            if G.inv_shown == True:
                A.muffle_time_ambience()
                G.inv_shown = G.inventoryscreen(mousex,mousey,leftbutton)
                P.inventory = G.inv_contents
            elif G.campfire_start_shown == True:
                A.muffle_time_ambience()
                G.campfire_start_shown = G.start_campfire_UI(mousex,mousey,leftbutton)
            elif G.campfire_ui_shown == True:
                A.pause_time_ambience()
                G.campfire_ui_shown = G.campfire_screen(mousex,mousey,leftbutton)
            else:
                if A.ambience_paused == True:
                    A.unpause_time_ambience()
                A.unmuffle_time_ambience()

                highlighted = classes.button(30,504,140,546,mousex,mousey)
                if highlighted == True:
                    screen.blit(inventory_entryh,(30,500))
                    if leftbutton == True:
                        G.inv_shown = True
                else:
                    screen.blit(inventory_entry,(30,500))
                cd = True
                for temp in G.campfireitemvalues.keys():
                    if temp not in P.inventory.keys():
                        cd = False
                if cd:
                    highlighted = classes.button(30,564,140,606,mousex,mousey)
                    if highlighted == True:
                        screen.blit(campfire_buttonh,(30,560))
                        if leftbutton == True:
                            G.campfire_start_shown = True
                    else:
                        screen.blit(campfire_button,(30,560))
            
        player_pointer_offset += player_pointer_offset_change
            
        if player_pointer_offset <= -20:
            player_pointer_offset_change = abs(player_pointer_offset_change)
        if player_pointer_offset >= 50:
            player_pointer_offset_change = abs(player_pointer_offset_change)*-1
        if fading_in[0] != False:
            tempimg = fading_in[0]
            tempimg.set_alpha(fading_in[1])
            screen.blit(tempimg,fading_in[2])
            fading_in[1] -= 1
            if fading_in[1] <= 0:
                fading_in[1] = 0
                A.end_music()
                A.unpause_time_ambience()
                fading_in[0] = False
        pygame.display.update()
        sleep(0.01)
        if G.slept == True:
            G.slept = False
            T.update(random.randint(5,9))
            A.get_time_ambience(T.time)
            T.days_played += 1
        if s == True:
            T.tick()
            A.get_time_ambience(T.time)
            sleep(0.29)
            time_elapsed += 0.3
            enc_time_elapsed += 0.3
            s = False
            player_pointer_offset += 9*player_pointer_offset_change
            enc = E.generate_encounter(T.time,M.biometolevel[P.currentbiome])
            
            if enc != []:
                enemies_faced = {}
                for i in enc:
                    if i in enemies_faced.keys():
                        enemies_faced[i] += 1
                    else:
                        enemies_faced[i] = 1
                    P.values["hp"],hploss,e = F.encounter(i,P.values)
                    if P.values["hp"] <= 0:
                        break
                    

            
        time_elapsed += 0.01
        enc_time_elapsed += 0.01
        
        screen.fill(black)
        if P.values["hp"] <= 0:
            alive = False
        P.EquipWeapon()
    res = False
    screen.blit(respawn_screen,(0,0))
    not_clicked = True
    if running == False:
        not_clicked = False
        A.stop_ambience()
    while not_clicked:

        cursorx,cursory = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed(3)[0]
        highlighted = classes.button(500,500, 800, 600, cursorx, cursory)
        days_played = futurefontL.render("Days survived: "+str(T.days_played),False,white,black)
        screen.blit(days_played,(400,400))
        if highlighted == False:
            screen.blit(respawn_button,(500,500))
        else:
            screen.blit(respawn_buttonh,(500,500))
            if clicked == True:
                not_clicked = False
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                not_clicked = False