import matplotlib.pyplot as plt
import json


with open("data.json","r") as file:
    data = json.load(file)


def vmoy_t():
    "représenter la vitesse moyenne en fonction du temps"

    N=len(data[str(len(data)-1)]["speeds"]) #nombre de frames considérées
    fn=data[str(len(data)-1)]["start"]   #frame à laquelle la dernière voiture apparaît
    v_moy=[]

    for i in range(N):
        try:
            s=0
            for key in data:
                f=fn-data[key]["start"]+i
                s+=data[key]["speeds"][f]
            v_moy.append(s/len(data))

        except IndexError:
            print(f"Erreur dans le fichier (frame {f})")

    plt.plot([i for i in range(fn,fn+N)],v_moy)
    plt.show()


def v_t():
    "exprimer la vitesse d'un ou plusieurs véhicules en fonction du temps"

    plt.plot([i for i in range(data["1"]["start"],data["1"]["start"]+len(data["1"]["speeds"]))],data["1"]["speeds"])
    plt.plot([i for i in range(data["0"]["start"],data["0"]["start"]+len(data["0"]["speeds"]))],data["0"]["speeds"])
    plt.show()


def vmoy_sigma():
    "exprimer la vitesse moyenne des véhicules en fonction de l'écart-type de la distribution des vitesses"

    N=len(data[str(len(data)-1)]["speeds"]) #nombre de frames considérées
    fn=data[str(len(data)-1)]["start"]   #frame à laquelle la dernière voiture apparaît
    vmoy_sig=[]

    for j in range(n):  #n, nb de fichiers data à traiter
        try:
            with open(f"data{str(j)}.json","r") as file:
                data = json.load(file)

            N=len(data[str(len(data)-1)]["speeds"]) #nombre de frames considérées
            fn=data[str(len(data)-1)]["start"]      #frame à laquelle la dernière voiture apparaît
            s=0

            for i in range(N):
                try:
                    for key in data:
                        f=fn-data[key]["start"]+i
                        s+=data[key]["speeds"][f]
                except IndexError:
                    print(f"Erreur dans le fichier (frame={f}, j={j}, len={N})")
            vmoy_sig.append(s/(len(data)*N))
        except FileNotFoundError:
            pass

    return vmoy_sig
