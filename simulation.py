import pygame
import time
from random import randint


pygame.init()
res=(800,600)
window = pygame.display.set_mode(res)   #création de la fenêtre



txt_font = pygame.font.SysFont("arial",20)
txt_surface = txt_font.render("Frames: 0",False,[255,255,255])
window.blit(txt_surface,[5,5])


cars = []                               #liste des voitures


def in_window(recta):                    #vérifie si la voiture est dans la fenêtre
    w,h=recta.width,recta.height
    return -w<recta.x<res[0]+w and -h<recta.y<res[1]+h


def move_rect(recta,dx,dy):
    pygame.draw.rect(window,(0,0,0),recta)
    recta.x +=dx
    recta.y +=dy
    pygame.draw.rect(window,(0,0,255),recta)
print(pygame.font.get_fonts())


launched=True
loops,latency,tf=0,0,0
while launched:                         #boucle de lancement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False


    if randint(0,200)==0:                 #génération aléatoire de voitures
        cars.append(pygame.Rect(20,300,20,20))
        pygame.draw.rect(window,(0,0,255),cars[-1])


    i=0
    for i in range(len(cars)):
        if in_window(cars[i]):
            time.sleep(.001)
            move_rect(cars[i],1,0)
        else:
            cars.pop(i)
            break


    txt_surface = txt_font.render(f"Latency: {int(round(latency,3)*1e3)} ms",False,[0,0,0])         #debug
    window.blit(txt_surface,[5,25])
    latency=time.monotonic()-tf
    txt_surface = txt_font.render(f"Latency: {int(round(latency,3)*1e3)} ms",False,[255,255,255])
    window.blit(txt_surface,[5,25])
    txt_surface = txt_font.render(f"Frames: {loops}",False,[0,0,0])
    window.blit(txt_surface,[5,5])
    loops+=1
    txt_surface = txt_font.render(f"Frames: {loops}",False,[255,255,255])
    window.blit(txt_surface,[5,5])
    pygame.display.flip()
    tf=time.monotonic()
