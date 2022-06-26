import pygame
import time
from random import randint
from classes import *

pygame.init()
res=(1280,720)
window = pygame.display.set_mode(res)   #création de la fenêtre

txt_font = pygame.font.SysFont("arial",20)
txt_surface = txt_font.render("Frames: 0",False,[255,255,255])
window.blit(txt_surface,[5,5])

roads=[Road((20,300),(800,300),5)]


def distance(a:tuple,b:tuple):
    "renvoie la distance entre deux points"
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


frames=0
latency=0
tf=0
loop=True
while loop:                             #boucle de lancement
    time.sleep(.02)                     #dépend de la puissance de calcul de la machine utilisée
    for event in pygame.event.get():    #pour quitter la simulation lorsqu'on clique sur la croix
        if event.type == pygame.QUIT:
            loop = False

    for road in roads:
        for vehicle in list(road.vehicles):
            vehicle.move()

        if randint(0,int(1000/road.avg_gen))==0 and (len(road.vehicles)==0 or distance(road.start, road.vehicles[-1].position)>road.vehicles[-1].dim):
            #on génère aléatoirement en faisant attention à ce que le dernier véhicule se soit assez élogné
            road.vehicles.append(Vehicle(road,0))                           #on ajoute un véhicule à la route
            pygame.draw.rect(window,(0,0,255),road.vehicles[-1].rect)       #on fait apparaître le dernier véhicle ajouté


    txt_surface = txt_font.render(f"Latency: {int(round(latency,3)*1e3)} ms",False,[0,0,0])         #debug
    window.blit(txt_surface,[5,25])
    latency=time.monotonic()-tf
    txt_surface = txt_font.render(f"Latency: {int(round(latency,3)*1e3)} ms",False,[255,255,255])
    window.blit(txt_surface,[5,25])
    txt_surface = txt_font.render(f"Frames: {frames}",False,[0,0,0])
    window.blit(txt_surface,[5,5])
    frames+=1
    txt_surface = txt_font.render(f"Frames: {frames}",False,[255,255,255])
    window.blit(txt_surface,[5,5])
    pygame.display.flip()
    tf=time.monotonic()
