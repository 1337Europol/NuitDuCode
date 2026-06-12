import pyxel
import random
from ..utils import (
    COL_EXPLOSION_1, COL_EXPLOSION_2, COL_EXPLOSION_3
)


class Particule:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(-2.5, 2.5)
        self.duree_vie = random.randint(8, 22)
        self.couleur = random.choice([
            COL_EXPLOSION_1, COL_EXPLOSION_1,
            COL_EXPLOSION_2, COL_EXPLOSION_3, 7
        ])

    def mise_a_jour(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.duree_vie -= 1

    def est_morte(self):
        return self.duree_vie <= 0

    def dessiner(self):
        pyxel.pset(int(self.x), int(self.y), self.couleur)


class Explosion:
    def __init__(self, x, y, taille=10):
        self.x = x
        self.y = y
        self.particules = [Particule(x, y) for _ in range(taille * 3)]

    def mise_a_jour(self):
        for p in self.particules:
            p.mise_a_jour()
        self.particules = [p for p in self.particules if not p.est_morte()]

    def est_terminee(self):
        return len(self.particules) == 0

    def dessiner(self):
        for p in self.particules:
            p.dessiner()
