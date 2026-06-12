import pyxel
import random
from ..utils import HAUTEUR, LARGEUR

TYPE_TIR_DOUBLE = 0
TYPE_BOUCLIER = 1
TYPE_VIE = 2

_COULEURS = {TYPE_TIR_DOUBLE: 11, TYPE_BOUCLIER: 12, TYPE_VIE: 14}
_SYMBOLES = {TYPE_TIR_DOUBLE: ">>", TYPE_BOUCLIER: "[]", TYPE_VIE: "+1"}
_PROBAS = {TYPE_TIR_DOUBLE: 0.45, TYPE_BOUCLIER: 0.35, TYPE_VIE: 0.20}


def type_aleatoire():
    rng = random.random()
    cumul = 0.0
    for t, proba in _PROBAS.items():
        cumul += proba
        if rng < cumul:
            return t
    return TYPE_TIR_DOUBLE


class Powerup:
    def __init__(self, x, y, type_powerup=None):
        self.x = float(x)
        self.y = float(y)
        self.type = type_powerup if type_powerup is not None else type_aleatoire()
        self.vitesse = 0.7
        self.couleur = _COULEURS[self.type]
        self.symbole = _SYMBOLES[self.type]

    def mise_a_jour(self):
        self.y += self.vitesse

    def est_hors_ecran(self):
        return self.y > HAUTEUR + 10

    def collision_joueur(self, rx, ry, rl, rh):
        ix, iy = int(self.x), int(self.y)
        return ix + 5 > rx and ix - 5 < rx + rl and iy + 4 > ry and iy - 4 < ry + rh

    def dessiner(self):
        ix, iy = int(self.x), int(self.y)
        bord = self.couleur if pyxel.frame_count % 20 < 10 else 7
        pyxel.rectb(ix - 5, iy - 4, 10, 8, bord)
        pyxel.rect(ix - 4, iy - 3, 8, 6, 0)
        pyxel.text(ix - 3, iy - 2, self.symbole, self.couleur)
