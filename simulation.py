import pygame
import time
from random import randint
from classes import *
import json

pygame.init()
res=(1280,720)

window = pygame.display.set_mode(res)
#création de la fenêtre

txt_font = pygame.font.SysFont("arial",20)
txt_surface = txt_font.render("Frames: 0",False,[255,255,255])
window.blit(txt_surface,[5,5])

roads=[
Road((50,670), (1230,670),5, 100, 50),
Road((1230,670),(1230,50),5, 0),
Road((1230,50),(50,50),   5, 0),
Road((50,50),(50,670),    5, 0)]
#création des routes

roads[0].set_next_road(roads[1])
roads[1].set_next_road(roads[2])
roads[2].set_next_road(roads[3])
roads[3].set_next_road(roads[0])
#connextion des routes entre elles

def distance(a:tuple,b:tuple):
    "renvoie la distance entre deux points"
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

data={}
#données destinées à être sauvegardées pour analyse
frames=0
latency=0
clock=0
num=0
loop=True

while loop:                             #boucle de lancement

    time.sleep(.02)
    #dépend de la puissance de calcul de la machine utilisée (.02 par défaut)

    for event in pygame.event.get():
        #pour quitter la simulation lorsqu'on clique sur la croix
        if event.type == pygame.QUIT:
            filename=f"data{frames}.json"
            with open(filename,"w") as file:
                json.dump(data,file)
            #on enregistre les résultats lorsque l'on quitte
            loop = False

    for road in roads:
        #on fait rouler tous les véhicules de la route
        for vehicle in list(road.vehicles):
            vehicle.move()
            data[vehicle.num]["speeds"].append(vehicle.speed)

        if road.max_gen*road.avg_gen > 0:
            #tant qu'on veut générer des véhicules sur la route
            if randint(0,int(1000/road.avg_gen))==0 and (len(road.vehicles)==0 or distance(road.start, road.vehicles[-1].position)>road.vehicles[-1].dim):
                road.max_gen -= 1
                #on génère aléatoirement en faisant attention à ce que le dernier véhicule se soit assez élogné
                road.vehicles.append(Vehicle(road, num))                           #on ajoute un véhicule à la route
                data[num]={"start":frames,"speeds":[road.vehicles[-1].speed]}
                num += 1
                pygame.draw.rect(window,(0,0,255),road.vehicles[-1].rect)       #on fait apparaître le dernier véhicle ajouté

    txt_surface = txt_font.render(f"Latency: {int(round(latency,3)*1e3)} ms",False,[0,0,0])
    window.blit(txt_surface,[5,25])
    latency=time.monotonic()-clock
    txt_surface = txt_font.render(f"Latency: {int(round(latency,3)*1e3)} ms",False,[255,255,255])
    window.blit(txt_surface,[5,25])
    #affichage de la latence

    txt_surface = txt_font.render(f"Frames: {frames}",False,[0,0,0])
    window.blit(txt_surface,[5,5])
    frames+=1
    txt_surface = txt_font.render(f"Frames: {frames}",False,[255,255,255])
    window.blit(txt_surface,[5,5])
    #affichage du nombre de frames

    pygame.display.flip()   #actualiser la fenêtre de simulation

    clock=time.monotonic()
