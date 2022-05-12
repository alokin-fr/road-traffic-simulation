import pygame


class Car:
    def __init__(self,pos:list,speed):
        self.speed=speed
        self.pos=pos
        self.rect=pygame.Rect(self.pos[0],self.pos[1],10,10)


    def in_window(self):                    #vérifie si la voiture est dans la fenêtre
        from simulation import res
        x,y=self.pos[0],self.pos[1]
        return -20<x<res[0]+20 and -20<y<res[1]+20


    def move(self,dx,dy):                   #bah ça bouge la caisse quoi
        from simulation import window
        pygame.draw.rect(window,(0,0,0),self.rect)
        self.pos[0]+=dx
        self.pos[1]+=dy
        self.rect=pygame.Rect(self.pos[0],self.pos[1],10,10)
        pygame.draw.rect(window,(0,0,255),self.rect)
