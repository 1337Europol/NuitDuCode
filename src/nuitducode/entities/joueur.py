import pyxel
from ..utils import LARGEUR, HAUTEUR, VITESSE_JOUEUR, COL_JOUEUR, COL_MOTEUR
from .projectile import Projectile
from .powerup import TYPE_TIR_DOUBLE, TYPE_BOUCLIER, TYPE_VIE


class Joueur:
    def __init__(self):
        self.x = float(LARGEUR // 2)
        self.y = float(HAUTEUR - 22)
        self.vies = 3
        self.score = 0
        self.invincible = 0
        self.cadence_tir = 12
        self.dernier_tir = 0
        self.projectiles = []
        self.tir_double_restant = 0
        self.bouclier_restant = 0

    def rectangle(self):
        return (int(self.x) - 5, int(self.y) - 8, 10, 16)

    def mise_a_jour(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            self.x = max(6.0, self.x - VITESSE_JOUEUR)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.x = min(float(LARGEUR - 6), self.x + VITESSE_JOUEUR)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
            self.y = max(16.0, self.y - VITESSE_JOUEUR)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.y = min(float(HAUTEUR - 10), self.y + VITESSE_JOUEUR)

        if pyxel.btn(pyxel.KEY_SPACE):
            if pyxel.frame_count - self.dernier_tir >= self.cadence_tir:
                self._tirer()
                self.dernier_tir = pyxel.frame_count

        for p in self.projectiles:
            p.mise_a_jour()
        self.projectiles = [p for p in self.projectiles if not p.est_hors_ecran()]

        if self.invincible > 0:
            self.invincible -= 1
        if self.tir_double_restant > 0:
            self.tir_double_restant -= 1
        if self.bouclier_restant > 0:
            self.bouclier_restant -= 1

    def _tirer(self):
        if self.tir_double_restant > 0:
            self.projectiles.append(Projectile(self.x - 4, self.y - 8, est_ennemi=False))
            self.projectiles.append(Projectile(self.x + 4, self.y - 8, est_ennemi=False))
        else:
            self.projectiles.append(Projectile(self.x, self.y - 8, est_ennemi=False))
        pyxel.play(0, 0)

    def appliquer_powerup(self, type_powerup):
        if type_powerup == TYPE_TIR_DOUBLE:
            self.tir_double_restant = 360
        elif type_powerup == TYPE_BOUCLIER:
            self.bouclier_restant = 300
        elif type_powerup == TYPE_VIE:
            self.vies = min(5, self.vies + 1)
        pyxel.play(0, 4)

    def touche(self):
        if self.bouclier_restant > 0:
            return
        if self.invincible == 0:
            self.vies -= 1
            self.invincible = 90
            pyxel.play(1, 2)

    def est_mort(self):
        return self.vies <= 0

    def dessiner(self):
        ix, iy = int(self.x), int(self.y)

        if self.bouclier_restant > 0:
            rayon = 12
            col_bouclier = 12 if pyxel.frame_count % 10 < 5 else 7
            pyxel.circb(ix, iy, rayon, col_bouclier)

        if self.invincible > 0 and pyxel.frame_count % 6 < 3:
            for p in self.projectiles:
                p.dessiner()
            return

        pyxel.tri(ix, iy - 9, ix - 6, iy + 5, ix + 6, iy + 5, COL_JOUEUR)
        pyxel.rect(ix - 2, iy - 6, 4, 8, 7)
        pyxel.rect(ix - 7, iy + 1, 3, 5, 1)
        pyxel.rect(ix + 4, iy + 1, 3, 5, 1)

        if self.tir_double_restant > 0:
            pyxel.pset(ix - 4, iy - 9, 11)
            pyxel.pset(ix + 4, iy - 9, 11)

        flamme = 10 if pyxel.frame_count % 6 < 3 else 9
        pyxel.pset(ix - 5, iy + 6, flamme)
        pyxel.pset(ix + 5, iy + 6, flamme)
        pyxel.pset(ix - 5, iy + 7, 8 if pyxel.frame_count % 6 < 3 else COL_MOTEUR)
        pyxel.pset(ix + 5, iy + 7, 8 if pyxel.frame_count % 6 < 3 else COL_MOTEUR)

        for p in self.projectiles:
            p.dessiner()
