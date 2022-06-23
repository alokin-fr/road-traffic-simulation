import pygame
import time
from random import randint
from car_generator import *

pygame.init()
res=(1280,720)
window = pygame.display.set_mode(res)   #création de la fenêtre

txt_font = pygame.font.SysFont("arial",20)
txt_surface = txt_font.render("Frames: 0",False,[255,255,255])
window.blit(txt_surface,[5,5])

roads=[Road((20,300),(500,300))]
launched=True
frames,latency,tf=0,0,0


while launched:                         #boucle de lancement
    time.sleep(.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False

    for road in roads:
        for vehicle in road.vehicles:
            vehicle.move()

        if randint(0,80)==0:
            road.vehicles.append(Vehicle(road,1))                           #on ajoute un véhicule à la route
            print(road.start)
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
