import pygame
import time
from random import randint


pygame.init()
res=(800,600)
window = pygame.display.set_mode(res)   #création de la fenêtre


cars = []                               #liste des voitures


def in_window(recta):                    #vérifie si la voiture est dans la fenêtre
    w,h=recta.width,recta.height
    return -w<recta.x<res[0]+w and -h<recta.y<res[1]+h


def move_rect(recta,dx,dy):
    pygame.draw.rect(window,(0,0,0),recta)
    recta.x +=dx
    recta.y +=dy
    pygame.draw.rect(window,(0,0,255),recta)



launched=True
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
    pygame.display.flip()
