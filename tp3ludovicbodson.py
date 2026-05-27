"""Tp3
code par ludovic bodson
"""
import random

vie, victoires, victoires_tot, defaites, nb_combat = 20, 0, 0, 0, 0

while vie > 0:
    force = random.randint(10, 12) if victoires > 0 and victoires % 3 == 0 else random.randint(2, 10)
    print(f"\nMonstre force {force} | Vie: {vie} | Victoires: {victoires_tot}")
    choix = input("1-Combattre 2-Contourner(-1PV) 3-Règles 4-Quitter: ")

    if choix == "1":
        nb_combat += 1
        de = random.randint(1, 6) + random.randint(1, 6)
        print(f"Lancer: {de} vs Force: {force}")
        if de > force:
            vie += force
            victoires += 1
            victoires_tot += 1
            print(f"Gagné! +{force} PV")
        else:
            vie -= force
            victoires = 0
            defaites += 1
            print(f"Perdu! -{force} PV")
    elif choix == "2":
        vie -= 1
    elif choix == "3":
        print("Battre le monstre: Dé > Force. Échec: Dé <= Force. Contourner coûte 1 PV.")
    elif choix == "4":
        break

print(f"\nPartie terminée. Monstres vaincus: {victoires_tot}. Au revoir!")