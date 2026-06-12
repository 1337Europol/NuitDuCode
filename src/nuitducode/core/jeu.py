import pyxel
import random
from ..utils import (
    LARGEUR, HAUTEUR,
    ETAT_MENU, ETAT_JEU, ETAT_PAUSE, ETAT_GAME_OVER, ETAT_VICTOIRE,
    TYPE_BASIQUE, TYPE_RAPIDE, TYPE_LOURD, TYPE_BOSS,
    NB_VAGUES,
    initialiser_sons
)
from ..entities import Joueur, Ennemi, Explosion, ChampEtoiles
from ..ui import Interface


FORMATIONS = {
    1: [(TYPE_BASIQUE, 20, -15), (TYPE_BASIQUE, 50, -15), (TYPE_BASIQUE, 80, -15),
        (TYPE_BASIQUE, 110, -15), (TYPE_BASIQUE, 140, -15),
        (TYPE_BASIQUE, 35, -30), (TYPE_BASIQUE, 65, -30), (TYPE_BASIQUE, 95, -30), (TYPE_BASIQUE, 125, -30)],
    2: [(TYPE_BASIQUE, 40, -15), (TYPE_BASIQUE, 80, -15), (TYPE_BASIQUE, 120, -15),
        (TYPE_RAPIDE, 20, -30), (TYPE_RAPIDE, 60, -30), (TYPE_RAPIDE, 100, -30), (TYPE_RAPIDE, 140, -30),
        (TYPE_BASIQUE, 60, -45), (TYPE_BASIQUE, 100, -45)],
    3: [(TYPE_LOURD, 40, -20), (TYPE_LOURD, 80, -20), (TYPE_LOURD, 120, -20),
        (TYPE_RAPIDE, 20, -40), (TYPE_RAPIDE, 140, -40),
        (TYPE_BASIQUE, 60, -40), (TYPE_BASIQUE, 100, -40)],
    4: [(TYPE_RAPIDE, 15, -15), (TYPE_RAPIDE, 35, -25), (TYPE_RAPIDE, 55, -15),
        (TYPE_RAPIDE, 75, -25), (TYPE_RAPIDE, 95, -15), (TYPE_RAPIDE, 115, -25),
        (TYPE_RAPIDE, 135, -15), (TYPE_RAPIDE, 145, -25),
        (TYPE_LOURD, 50, -50), (TYPE_LOURD, 80, -50), (TYPE_LOURD, 110, -50)],
    5: [(TYPE_BOSS, 80, -25),
        (TYPE_LOURD, 30, -60), (TYPE_LOURD, 130, -60),
        (TYPE_RAPIDE, 20, -80), (TYPE_RAPIDE, 60, -80),
        (TYPE_RAPIDE, 100, -80), (TYPE_RAPIDE, 140, -80)],
}


class Jeu:
    def __init__(self):
        self.etat = ETAT_MENU
        self.champ_etoiles = ChampEtoiles()
        self.interface = Interface()
        initialiser_sons()
        self._reinitialiser()

    def _reinitialiser(self):
        self.joueur = Joueur()
        self.ennemis = []
        self.explosions = []
        self.vague = 0
        self.compteur_transition = 0
        self._lancer_vague_suivante()

    def _lancer_vague_suivante(self):
        self.vague += 1
        self.ennemis.clear()
        formation = FORMATIONS.get(self.vague, FORMATIONS[1])
        for type_e, ex, ey in formation:
            self.ennemis.append(Ennemi(ex, ey, type_e))
        self.compteur_transition = 90

    def mise_a_jour(self):
        self.champ_etoiles.mise_a_jour()

        if self.etat == ETAT_MENU:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self._reinitialiser()
                self.etat = ETAT_JEU

        elif self.etat == ETAT_JEU:
            if pyxel.btnp(pyxel.KEY_P):
                self.etat = ETAT_PAUSE
                return
            self._mise_a_jour_jeu()

        elif self.etat == ETAT_PAUSE:
            if pyxel.btnp(pyxel.KEY_P):
                self.etat = ETAT_JEU

        elif self.etat in (ETAT_GAME_OVER, ETAT_VICTOIRE):
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.etat = ETAT_MENU

    def _mise_a_jour_jeu(self):
        if self.compteur_transition > 0:
            self.compteur_transition -= 1
            return

        self.joueur.mise_a_jour()

        for ennemi in self.ennemis:
            ennemi.mise_a_jour()

        for explosion in self.explosions:
            explosion.mise_a_jour()
        self.explosions = [e for e in self.explosions if not e.est_terminee()]

        self._verifier_collisions()

        self.ennemis = [e for e in self.ennemis if not e.est_hors_ecran()]

        if not self.ennemis:
            if self.vague >= NB_VAGUES:
                self.etat = ETAT_VICTOIRE
            else:
                self._lancer_vague_suivante()

        if self.joueur.est_mort():
            self.etat = ETAT_GAME_OVER

    def _verifier_collisions(self):
        rx, ry, rl, rh = self.joueur.rectangle()

        for ennemi in self.ennemis[:]:
            for proj in self.joueur.projectiles[:]:
                ex, ey, el, eh = ennemi.rectangle()
                if proj.collision(ex, ey, el, eh):
                    if proj in self.joueur.projectiles:
                        self.joueur.projectiles.remove(proj)
                    if ennemi.touche():
                        self.joueur.score += ennemi.points
                        self.explosions.append(Explosion(ennemi.x, ennemi.y, ennemi.largeur))
                        pyxel.play(3, 1)
                        if ennemi in self.ennemis:
                            self.ennemis.remove(ennemi)
                        break

            for proj in ennemi.projectiles[:]:
                if proj.collision(rx, ry, rl, rh):
                    ennemi.projectiles.remove(proj)
                    self.joueur.touche()
                    self.explosions.append(Explosion(self.joueur.x, self.joueur.y, 6))

        for ennemi in self.ennemis[:]:
            ex, ey, el, eh = ennemi.rectangle()
            if (rx < ex + el and rx + rl > ex and ry < ey + eh and ry + rh > ey):
                self.joueur.touche()
                if ennemi.touche(ennemi.pv):
                    self.explosions.append(Explosion(ennemi.x, ennemi.y, ennemi.largeur))
                    if ennemi in self.ennemis:
                        self.ennemis.remove(ennemi)

    def dessiner(self):
        pyxel.cls(0)

        if self.etat == ETAT_MENU:
            self.interface.dessiner_menu(self.champ_etoiles)
            return

        self.champ_etoiles.dessiner()

        if self.etat == ETAT_GAME_OVER:
            self.interface.dessiner_game_over(self.joueur.score, self.champ_etoiles)
            return

        if self.etat == ETAT_VICTOIRE:
            self.interface.dessiner_victoire(self.joueur.score, self.champ_etoiles)
            return

        for ennemi in self.ennemis:
            ennemi.dessiner()

        for explosion in self.explosions:
            explosion.dessiner()

        self.joueur.dessiner()

        if self.etat == ETAT_PAUSE:
            self.interface.dessiner_pause()

        self.interface.dessiner_hud(self.joueur, self.vague, NB_VAGUES)
        self.interface.dessiner_transition_vague(self.vague, self.compteur_transition)
