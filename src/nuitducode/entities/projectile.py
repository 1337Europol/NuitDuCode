import pyxel
from ..utils import (
    LARGEUR, HAUTEUR,
    COL_PROJ_JOUEUR, COL_PROJ_ENNEMI,
    VITESSE_PROJECTILE_JOUEUR, VITESSE_PROJECTILE_ENNEMI
)


class Projectile:
    def __init__(self, x, y, est_ennemi=False, vx=0.0):
        self.x = float(x)
        self.y = float(y)
        self.est_ennemi = est_ennemi
        self.vx = vx
        self.vy = VITESSE_PROJECTILE_ENNEMI if est_ennemi else -VITESSE_PROJECTILE_JOUEUR

    def mise_a_jour(self):
        self.x += self.vx
        self.y += self.vy

    def est_hors_ecran(self):
        return self.y < -8 or self.y > HAUTEUR + 8 or self.x < -8 or self.x > LARGEUR + 8

    def collision(self, rx, ry, rl, rh):
        return (
            self.x > rx and self.x < rx + rl and
            self.y > ry and self.y < ry + rh
        )

    def dessiner(self):
        ix, iy = int(self.x), int(self.y)
        if self.est_ennemi:
            pyxel.rect(ix - 1, iy, 2, 5, COL_PROJ_ENNEMI)
            pyxel.pset(ix, iy + 5, 14)
        else:
            pyxel.rect(ix - 1, iy, 2, 6, COL_PROJ_JOUEUR)
            pyxel.pset(ix, iy - 1, 7)
