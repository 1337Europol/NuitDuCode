import pyxel
import math
import random
from ..utils import (
    LARGEUR, HAUTEUR,
    TYPE_BASIQUE, TYPE_RAPIDE, TYPE_LOURD, TYPE_BOSS,
    POINTS_BASIQUE, POINTS_RAPIDE, POINTS_LOURD, POINTS_BOSS,
    COL_ENNEMI_BASIQUE, COL_ENNEMI_RAPIDE, COL_ENNEMI_LOURD,
    COL_BOSS, COL_BARRE_VIE, COL_BARRE_FOND
)
from .projectile import Projectile


CONFIGS = {
    TYPE_BASIQUE: {
        "pv_max": 1, "vitesse_y": 0.6, "vitesse_x": 0.0,
        "cadence": 80, "largeur": 10, "hauteur": 9,
        "points": POINTS_BASIQUE, "couleur": COL_ENNEMI_BASIQUE
    },
    TYPE_RAPIDE: {
        "pv_max": 1, "vitesse_y": 1.4, "vitesse_x": 0.8,
        "cadence": 0, "largeur": 8, "hauteur": 7,
        "points": POINTS_RAPIDE, "couleur": COL_ENNEMI_RAPIDE
    },
    TYPE_LOURD: {
        "pv_max": 4, "vitesse_y": 0.25, "vitesse_x": 0.0,
        "cadence": 50, "largeur": 14, "hauteur": 12,
        "points": POINTS_LOURD, "couleur": COL_ENNEMI_LOURD
    },
    TYPE_BOSS: {
        "pv_max": 25, "vitesse_y": 0.0, "vitesse_x": 0.9,
        "cadence": 25, "largeur": 32, "hauteur": 22,
        "points": POINTS_BOSS, "couleur": COL_BOSS
    },
}


class Ennemi:
    def __init__(self, x, y, type_ennemi=TYPE_BASIQUE):
        self.x = float(x)
        self.y = float(y)
        self.type = type_ennemi
        cfg = CONFIGS[type_ennemi]
        self.pv = cfg["pv_max"]
        self.pv_max = cfg["pv_max"]
        self.vitesse_y = cfg["vitesse_y"]
        self.vitesse_x = cfg["vitesse_x"]
        self.cadence = cfg["cadence"]
        self.largeur = cfg["largeur"]
        self.hauteur = cfg["hauteur"]
        self.points = cfg["points"]
        self.couleur = cfg["couleur"]
        self.projectiles = []
        self.dernier_tir = random.randint(0, self.cadence) if self.cadence > 0 else 0
        self.direction_x = random.choice([-1, 1])
        self.phase_y = random.uniform(0, 6.28)
        self.entree = True
        self.entree_cible_y = y

    def rectangle(self):
        ml = self.largeur // 2
        mh = self.hauteur // 2
        return (int(self.x) - ml, int(self.y) - mh, self.largeur, self.hauteur)

    def mise_a_jour(self):
        if self.entree:
            self.y += 1.5
            if self.y >= self.entree_cible_y:
                self.y = self.entree_cible_y
                self.entree = False
            return

        if self.type == TYPE_BOSS:
            self.x += self.vitesse_x * self.direction_x
            if self.x < 20 or self.x > LARGEUR - 20:
                self.direction_x *= -1
            self.y = 30.0 + math.sin(pyxel.frame_count * 0.05) * 8

        elif self.type == TYPE_RAPIDE:
            self.x += self.vitesse_x * self.direction_x
            self.y += self.vitesse_y
            if self.x < 5 or self.x > LARGEUR - 5:
                self.direction_x *= -1

        else:
            self.y += self.vitesse_y

        if self.cadence > 0:
            if pyxel.frame_count - self.dernier_tir >= self.cadence:
                self._tirer()
                self.dernier_tir = pyxel.frame_count

        for p in self.projectiles:
            p.mise_a_jour()
        self.projectiles = [p for p in self.projectiles if not p.est_hors_ecran()]

    def _tirer(self):
        if self.type == TYPE_BOSS:
            for decalage in [-12, 0, 12]:
                self.projectiles.append(
                    Projectile(self.x + decalage, self.y + 12, est_ennemi=True)
                )
            pyxel.play(2, 3)
        else:
            self.projectiles.append(
                Projectile(self.x, self.y + self.hauteur // 2, est_ennemi=True)
            )

    def touche(self, degats=1):
        self.pv -= degats
        return self.pv <= 0

    def est_hors_ecran(self):
        return self.y > HAUTEUR + 30

    def dessiner(self):
        ix, iy = int(self.x), int(self.y)

        if self.type == TYPE_BASIQUE:
            pyxel.tri(ix, iy + 5, ix - 5, iy - 4, ix + 5, iy - 4, self.couleur)
            pyxel.rect(ix - 2, iy - 2, 4, 4, 5)
            pyxel.pset(ix - 2, iy, 10)
            pyxel.pset(ix + 2, iy, 10)

        elif self.type == TYPE_RAPIDE:
            pyxel.tri(ix, iy + 4, ix - 4, iy - 3, ix + 4, iy - 3, self.couleur)
            pyxel.pset(ix, iy, 10)

        elif self.type == TYPE_LOURD:
            pyxel.rect(ix - 7, iy - 6, 14, 12, self.couleur)
            pyxel.tri(ix, iy + 7, ix - 4, iy + 3, ix + 4, iy + 3, self.couleur)
            pyxel.rect(ix - 4, iy - 4, 8, 8, 1)
            pyxel.pset(ix - 2, iy - 1, 10)
            pyxel.pset(ix + 2, iy - 1, 10)
            self._dessiner_barre_vie(ix, iy - 9, 12)

        elif self.type == TYPE_BOSS:
            pyxel.rect(ix - 16, iy - 11, 32, 22, self.couleur)
            pyxel.rect(ix - 10, iy - 16, 20, 7, 2)
            pyxel.rect(ix - 4, iy - 8, 8, 16, 7)
            pyxel.circ(ix - 7, iy, 3, 8)
            pyxel.circ(ix + 7, iy, 3, 8)
            pyxel.rect(ix - 3, iy - 4, 6, 8, 12)
            if pyxel.frame_count % 8 < 4:
                pyxel.pset(ix - 7, iy, 7)
                pyxel.pset(ix + 7, iy, 7)
            self._dessiner_barre_vie(ix, iy - 19, 28)

        for p in self.projectiles:
            p.dessiner()

    def _dessiner_barre_vie(self, ix, iy, largeur_max):
        rempli = int((self.pv / self.pv_max) * largeur_max)
        pyxel.rect(ix - largeur_max // 2, iy, largeur_max, 2, COL_BARRE_FOND)
        pyxel.rect(ix - largeur_max // 2, iy, rempli, 2, COL_BARRE_VIE)
