import pyxel
import random
from ..utils import LARGEUR, HAUTEUR, NB_ETOILES


class Etoile:
    def __init__(self, vitesse_min, vitesse_max, couleurs):
        self.x = float(random.randint(0, LARGEUR))
        self.y = float(random.randint(0, HAUTEUR))
        self.vitesse = random.uniform(vitesse_min, vitesse_max)
        self.couleur = random.choice(couleurs)

    def mise_a_jour(self):
        self.y += self.vitesse
        if self.y >= HAUTEUR:
            self.y = 0.0
            self.x = float(random.randint(0, LARGEUR))

    def dessiner(self):
        pyxel.pset(int(self.x), int(self.y), self.couleur)


class ChampEtoiles:
    def __init__(self):
        nb_lentes = NB_ETOILES // 3
        nb_rapides = NB_ETOILES - nb_lentes
        self.couche_fond = [Etoile(0.15, 0.4, [5]) for _ in range(nb_lentes)]
        self.couche_avant = [Etoile(0.6, 1.8, [5, 6, 6, 7]) for _ in range(nb_rapides)]

    def mise_a_jour(self):
        for e in self.couche_fond:
            e.mise_a_jour()
        for e in self.couche_avant:
            e.mise_a_jour()

    def dessiner(self):
        for e in self.couche_fond:
            e.dessiner()
        for e in self.couche_avant:
            e.dessiner()
