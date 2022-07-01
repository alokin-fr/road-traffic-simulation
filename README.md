# road-traffic-simulation
Le programme est un simulateur de trafic routier se basant sur un modèle microscopique (c.à.d. contrôlant individuellement chaque véhicule). Il utilise le module Pygame (https://www.pygame.org/docs/) et se base sur le modèle "Intelligent Driver Model" (IDM) (https://en.wikipedia.org/wiki/Intelligent_driver_model).

Étant un modèle microscopique, l'IDM fournit au programme un système de n équations différentielles d'ordre 1 à résoudre, vérifiées par la vitesse de chaque véhicule (où n est le nombre de véhicules mis en jeu). Actuellement, le choix d'approximer la vitesse et la position de chaque véhicule à tout instant par un développement en séries de Taylor (resp. à l'ordre 1 et 2) a été retenu.

Il est à noter que le programme est pour le moment écrit de façon très simplifiée (par exemple il est prévu que les véhicules ne se déplacent qu'horizontalement ou verticalement) et qu'il sera ammélioré au fil du temps. En particulier, la méthode de résolution des équations différentielles sera probablement revue pour amméliorer la précision des résultats (les méthodes d'Euler/Runge-Kutta seront testées). 

 🚦    :car::blue_car::truck::racing_car:
