import pygame


class Vehicle:
    def __init__(self,pos,speed):
        self.speed=speed
        self.pos=pos
        self.rect=pygame.Rect(self.pos[0],self.pos[1],11,11)


    def in_window(self):                    #vérifie si la voiture est dans la fenêtre
        from simulation import res
        x,y=self.pos[0],self.pos[1]
        return -20<x<res[0]+20 and -20<y<res[1]+20


    def move(self,dx,dy):                   #bah ça bouge la caisse quoi
        from simulation import window
        pygame.draw.rect(window,(0,0,0),self.rect)
        self.pos[0]+=dx
        self.pos[1]+=dy
        self.rect=pygame.Rect(self.pos[0],self.pos[1],11,11)
        pygame.draw.rect(window,(0,0,255),self.rect)


class Road:
    def __init__(self,start,end):
        from simulation import window
        self.start=start    #(x,y)
        self.end=end        #(x,y)

        if start[0]==end[0]:
            self.vect=(start[0],(end[1]-start[1])/abs(end[1]-start[1]))
        elif start[1]==end[1]:
            self.vect=((end[0]-start[0])/abs(end[0]-start[0]),start[1])

        self.vehicles=[]
        pygame.draw.line(window,[255,255,255],start,end)

    def in_road(self,vehicle):
        if self.start[0]<=self.end[0]
        return self.start[0]<=self.pos[0]<=self.end[0] and self.start[1]<=self.pos[1]<=self.end[1]
