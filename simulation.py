import pygame
import time
from random import randint
from car_generator import Car


pygame.init()
res=(1280,720)
window = pygame.display.set_mode(res)   #création de la fenêtre


txt_font = pygame.font.SysFont("arial",20)
txt_surface = txt_font.render("Frames: 0",False,[255,255,255])
window.blit(txt_surface,[5,5])


cars = []                               #liste des voitures


launched=True
frames,latency,tf=0,0,0
while launched:                         #boucle de lancement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False


    if randint(0,200)==0:                 #génération aléatoire de voitures
        cars.append(Car([20,300],1))
        pygame.draw.rect(window,(0,0,255),cars[-1].rect)


    i=0
    for i in range(len(cars)):
        if cars[i].in_window():
            time.sleep(.1)
            cars[i].move(5,0)
        else:
            cars.pop(i)
            break


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
