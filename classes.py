import pygame
from collections import deque


class Vehicle:
    def __init__(self, road, num, init_speed=0, max_speed=None):
        self.speed=float(init_speed)                                #vitesse -> float
        self.position=list(road.start)                              #position -> tuple (float*float)
        self.road=road                                              #route -> class Road
        self.index=len(road.vehicles)                               #indice -> int
        self.dim=21                                                 #taille -> int
        self.num=num                                                #numéro d'apparition

        if max_speed==None:
            #on choisit aléatoirement la vitesse max du véhicule selon une loi normale :
            # - espérance : la limite de vitesse de la route
            # - écart type : 10% de la limite de vitesse de la route
            from random import gauss
            self.max_speed=abs(gauss(road.speed_limit,road.speed_limit*0.1))  #float
            #self.max_speed=road.speed_limit
        else:
            #utile si la voiture change de route et ainsi conserver sa vitesse
            self.max_speed=max_speed

        #par défaut les coordonnées du rectangle sont celles du sommet sup-gauche
        #on veut qu'elles correspondent à l'avant du véhicule
        if self.road.vect[0]==1:    #si la route est vers la droite
            self.rect=pygame.Rect(self.position[0]-self.dim, self.position[1]-(self.dim+1)/2, self.dim, self.dim)
        elif self.road.vect[0]==-1: #si la route est vers la gauche
            self.rect=pygame.Rect(self.position[0], self.position[1]-(self.dim+1)/2, self.dim, self.dim)
        elif self.road.vect[1]==1:  #si la route est vers le bas
            self.rect=pygame.Rect(self.position[0]-(self.dim+1)/2, self.position[1]-self.dim, self.dim, self.dim)
        elif self.road.vect[1]==-1:  #si la route est vers le haut
            self.rect=pygame.Rect(self.position[0]-(self.dim+1)/2, self.position[1], self.dim, self.dim)


    def in_window(self):
        "renvoie True si le véhicule est dans la fenêtre de simulation, False sinon"
        from simulation import res
        x,y=self.position[0],self.position[1]
        return -self.dim<x<res[0]+self.dim and -self.dim<y<res[1]+self.dim


    def in_road(self):
        "renvoie True si le véhicule est dans la route, False sinon"
        if self.road.vect[0]==1:        #si la route est vers la droite
            return self.road.start[0]<=self.position[0]<=self.road.end[0]
        elif self.road.vect[0]==-1:     #si la route est vers la gauche
            return self.road.start[0]>=self.position[0]>=self.road.end[0]
        elif self.road.vect[1]==1:      #si la route est vers le bas
            return self.road.start[1]<=self.position[1]<=self.road.end[1]
        elif self.road.vect[1]==-1:      #si la route est vers le haut
            return self.road.start[1]>=self.position[1]>=self.road.end[1]


    def idm(self):
        "calcule l'accélération du véhicule à l'instant t selon l'équation différentielle de l'IDM"
        #On utilise les relations 1 m <-> 10 px et 1 s <-> 50 frames choisies arbitrairement
        #(la taille des véhicules est alors de 2 m x 2 m)
        a=0.2                                           #a=1.0 m/s², par défaut
        b=0.3                                           #b=1.5 m/s², par défaut
        delta=4                                         #delta=4, par défaut
        s0=self.dim*0.75                                #distance minimale
        T=1/.02                                         #temps de réaction, T=1s par défaut
        v_i=self.speed                                  #v_i
        v_0i=self.max_speed                             #v_0,i

        acceleration = a*(1-(v_i/v_0i)**delta)          #accélération en route libre

        if self.index>0:
            #s'il est précédé d'un véhicule
            Dv_i = v_i - self.road.vehicles[self.index-1].speed     #Δv_i = v_i - v_(i-1)
            stop_dist = v_i*T + v_i*Dv_i/(2*(a*b)**(0.5))           #correspond au terme X dans s_star = s0 + max(0,X)

            if stop_dist>0:
                s_star=s0
            else:
                s_star=s0+stop_dist
            #s_star = s0 + max[0, v_i*T + (v_i*Δv_i)/(2*sqrt(ab))]
            from simulation import distance
            s_i = distance(self.position, self.road.vehicles[self.index-1].position) - self.dim
            #s_i = |x_i - x_(i-1)| - l
            return acceleration - a*(s_star/s_i)**2

        elif self.road.next_road!=None and len(self.road.next_road.vehicles)>0:
            #s'il est précédé d'un véhicule qui se situe sur la route suivante
            Dv_i = v_i - self.road.next_road.vehicles[self.index-1].speed
            stop_dist = v_i*T + v_i*Dv_i/(2*(a*b)**(0.5))

            if stop_dist>0:
                s_star=s0
            else:
                s_star=s0+stop_dist

            from simulation import distance
            s_i = distance(self.position, self.road.end) + distance(self.road.next_road.start, self.road.next_road.vehicles[-1].position) - self.dim

            return acceleration - a*(s_star/s_i)**2

        return acceleration


    def move(self):
        "modifie la position du véhicule"
        from simulation import window
        pygame.draw.rect(window,(0,0,0),self.rect)  #on efface le véhicule de sa position initiale

        if self.road.vect[0]==0:                    #on réaffiche la ligne qui a été effacée par le véhicule
            pygame.draw.line(window, [255,255,255], self.position, [self.position[0],self.position[1]-self.dim*self.road.vect[1]])
        elif self.road.vect[1]==0:
            pygame.draw.line(window, [255,255,255], self.position, [self.position[0]-self.dim*self.road.vect[0],self.position[1]])

        a=self.idm()
        if self.speed+a <0:
            #si la vitesse deviendrait négative, on l'approxime égale à 0
            if self.road.vect[0]==1:
                self.position[0] += self.speed/2
            elif self.road.vect[0]==-1:
                self.position[0] -= self.speed/2
            elif self.road.vect[1]==1:
                self.position[1] += self.speed/2
            elif self.road.vect[1]==-1:
                self.position[1] -= self.speed/2
            self.speed = 0

        else:
            #v(t+Δt) = v(t) + a(t)Δt
            #x(t+Δt) = x(t) + v(t)Δt + (a(t)Δt²)/2
            #[avec Δt=1]
            self.speed = self.speed + a
            if self.road.vect[0]==1:    #si la route est horizontale vers la droite
                self.position[0] += self.speed+a/2
            elif self.road.vect[0]==-1: #si la route est horizontale vers la gauche
                self.position[0] -= self.speed+a/2
            elif self.road.vect[1]==1:  #si la route est verticale vers le bas
                self.position[1] += self.speed+a/2
            elif self.road.vect[1]==-1:  #si la route est verticale vers le haut
                self.position[1] -= self.speed+a/2

        if self.in_road():
            if self.road.vect[0]==1:    #si la route est horizontale vers la droite
                self.rect=pygame.Rect(self.position[0]-self.dim, self.position[1]-(self.dim+1)/2, self.dim, self.dim)
            elif self.road.vect[0]==-1: #si la route est horizontale vers la gauche
                self.rect=pygame.Rect(self.position[0], self.position[1]-(self.dim+1)/2, self.dim, self.dim)
            elif self.road.vect[1]==1:  #si la route est verticale vers le bas
                self.rect=pygame.Rect(self.position[0]-6, self.position[1]-self.dim, self.dim, self.dim)
            elif self.road.vect[1]==-1:  #si la route est verticale vers le haut
                self.rect=pygame.Rect(self.position[0]-6, self.position[1], self.dim, self.dim)
            pygame.draw.rect(window,(0,0,255),self.rect)
        else:
            self.road.vehicles.popleft()
            for vehicle in self.road.vehicles:  #en retirant le véhicule à l'avant de la file, l'indice des autres véhicules diminue de 1
                vehicle.index-=1
            if self.road.next_road!=None:
                self.index+=1
                self.__init__(self.road.next_road,self.num,self.speed,self.max_speed)
                self.road.vehicles.append(self)
                pygame.draw.rect(window,(0,0,255),self.rect)


class Road:
    def __init__(self, start, end, speed_limit, avg_gen=10, max_gen=float("inf")):
        from simulation import window
        self.start=start                #position du début de la route
        self.end=end                    #position de la fin de la route
        self.speed_limit=speed_limit    #limitation de vitesse de la route
        self.avg_gen=avg_gen            #génération moyenne de véhicules en 1000 frames
        self.max_gen=max_gen            #nombre max de véhicules que l'on souhaite générer
        self.next_road=None             #route qui succède à celle-là

        if start[0]==end[0]:        #vecteur unitaire de la route
            self.vect=(0, int((end[1]-start[1])/abs(end[1]-start[1])))
        elif start[1]==end[1]:
            self.vect=(int((end[0]-start[0])/abs(end[0]-start[0])), 0)

        self.vehicles=deque([])            #liste des véhicules sur la route
        pygame.draw.line(window,[255,255,255],start,end)


    def set_next_road(self,road):
        "défini la nouvelle route sur laquelle vont les véhicules arrivés à la fin de la route"
        self.next_road=road
