import pygame


class Vehicle:
    def __init__(self, road, speed):
        self.speed=speed
        self.pos=list(road.start)
        self.road=road

        #par défaut les coordonnées du rect sont celles du sommet sup-gauche
        #on veut que les coor correspondent à l'avant de la voiture
        if self.road.vect[0]==1:    #si la route est horizontale vers la droite
            self.rect=pygame.Rect(self.pos[0]-11, self.pos[1]-6, 11,11)
        elif self.road.vect[0]==-1: #si la route est horizontale vers la gauche
            self.rect=pygame.Rect(self.pos[0], self.pos[1]-6, 11,11)
        elif self.road.vect[1]==1:  #si la route est verticale vers le bas
            self.rect=pygame.Rect(self.pos[0]-6, self.pos[1]-11, 11,11)
        elif self.road.vect[1]==-1:  #si la route est verticale vers le haut
            self.rect=pygame.Rect(self.pos[0]-6, self.pos[1], 11,11)


    def in_window(self):
        from simulation import res
        x,y=self.pos[0],self.pos[1]
        return -20<x<res[0]+20 and -20<y<res[1]+20


    def move(self):
        from simulation import window
        pygame.draw.rect(window,(0,0,0),self.rect)  #on efface la voiture de sa position initiale

        if self.road.vect[0]==0:                    #on réaffiche la ligne qui a été effacée par la voiture
            pygame.draw.line(window, [255,255,255], self.pos, [self.pos[0],self.pos[1]-11*self.road.vect[1]])
        elif self.road.vect[1]==0:
            pygame.draw.line(window, [255,255,255], self.pos, [self.pos[0]-11*self.road.vect[0],self.pos[1]])


        self.pos[0]+=self.speed*self.road.vect[0]               #vect(delta_x) = delta_t * v_x * vect(u_x)  [avec delta_t=1]
        self.pos[1]+=self.speed*self.road.vect[1]               #vect(delta_y) = delta_t * v_y * vect(u_y)  [avec delta_t=1]


        if self.road.vect[0]==1:    #si la route est horizontale vers la droite
            self.rect=pygame.Rect(self.pos[0]-11, self.pos[1]-6, 11,11)
        elif self.road.vect[0]==-1: #si la route est horizontale vers la gauche
            self.rect=pygame.Rect(self.pos[0], self.pos[1]-6, 11,11)
        elif self.road.vect[1]==1:  #si la route est verticale vers le bas
            self.rect=pygame.Rect(self.pos[0]-6, self.pos[1]-11, 11,11)
        elif self.road.vect[1]==-1:  #si la route est verticale vers le haut
            self.rect=pygame.Rect(self.pos[0]-6, self.pos[1], 11,11)


        pygame.draw.rect(window,(0,0,255),self.rect)


class Road:
    def __init__(self, start, end, gen_time=10):
        from simulation import window
        self.start=start    #position du début de la route
        self.end=end        #position de la fin de la route
        self.gen_time=gen_time

        if start[0]==end[0]:        #vecteur unitaire de la route
            self.vect=(0, int((end[1]-start[1])/abs(end[1]-start[1])))
        elif start[1]==end[1]:
            self.vect=(int((end[0]-start[0])/abs(end[0]-start[0])), 0)

        self.vehicles=[]            #liste des véhicules sur la route
        pygame.draw.line(window,[255,255,255],start,end)
