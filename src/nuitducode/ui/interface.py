import pyxel
from ..utils import (
    LARGEUR, HAUTEUR,
    COL_HUD, COL_TEXTE, COL_JOUEUR, COL_VAGUE,
    COL_BARRE_VIE, COL_BARRE_FOND
)


RANGS = [
    (80000, "S", 10),
    (50000, "A", 11),
    (30000, "B", 12),
    (10000, "C", 9),
    (0,     "D", 8),
]


def rang_pour_score(score):
    for seuil, lettre, couleur in RANGS:
        if score >= seuil:
            return lettre, couleur
    return "D", 8


class Interface:
    def dessiner_hud(self, joueur, vague, nb_vagues):
        pyxel.rect(0, 0, LARGEUR, 11, COL_HUD)
        pyxel.text(3, 2, f"SCORE:{joueur.score:06d}", COL_TEXTE)
        pyxel.text(60, 2, f"VAGUE {vague}/{nb_vagues}", COL_VAGUE)
        for i in range(joueur.vies):
            bx = LARGEUR - 8 - i * 9
            pyxel.tri(bx, 2, bx - 4, 9, bx + 4, 9, COL_JOUEUR)
        if joueur.tir_double_restant > 0:
            pyxel.text(3, 12, "x2", 11)
        if joueur.bouclier_restant > 0:
            pyxel.text(14, 12, "[]", 12)

    def dessiner_combo(self, combo, multiplicateur):
        if combo < 2:
            return
        texte = f"COMBO x{multiplicateur}"
        couleur = 10 if pyxel.frame_count % 20 < 10 else 9
        pyxel.text(LARGEUR // 2 - len(texte) * 2, 15, texte, couleur)

    def dessiner_flash(self, intensite):
        if intensite <= 0:
            return
        for y in range(0, HAUTEUR, 4):
            pyxel.line(0, y, LARGEUR, y, 8)

    def dessiner_menu(self, champ_etoiles, highscore=0):
        pyxel.cls(0)
        champ_etoiles.dessiner()

        for i in range(3):
            pyxel.rect(0, 22 + i * 28, LARGEUR, 10, 1)

        titre = "G A L A C T I X"
        pyxel.text(LARGEUR // 2 - len(titre) * 2, 30, titre, 10)
        pyxel.text(LARGEUR // 2 - len(titre) * 2 - 1, 29, titre, 9)

        sous = "NUIT DU CODE 2026"
        pyxel.text(LARGEUR // 2 - len(sous) * 2, 42, sous, 6)

        if highscore > 0:
            hs = f"MEILLEUR : {highscore:06d}"
            pyxel.text(LARGEUR // 2 - len(hs) * 2, 54, hs, 5)

        if pyxel.frame_count % 40 < 28:
            invite = "[ ESPACE ] JOUER"
            pyxel.text(LARGEUR // 2 - len(invite) * 2, 68, invite, 7)

        ctrl = [("FLECHES/ZQSD", "DEPLACER"), ("ESPACE", "TIRER"), ("P", "PAUSE")]
        for i, (t, a) in enumerate(ctrl):
            pyxel.text(28, 85 + i * 8, f"{t:<12} {a}", 5)

    def dessiner_pause(self):
        pyxel.rect(40, 45, 80, 30, 1)
        pyxel.rectb(40, 45, 80, 30, 7)
        pyxel.text(62, 53, "- PAUSE -", 7)
        pyxel.text(47, 65, "P pour reprendre", 6)

    def dessiner_game_over(self, score, champ_etoiles, highscore=0):
        pyxel.cls(0)
        champ_etoiles.dessiner()
        pyxel.rect(22, 28, 116, 68, 1)
        pyxel.rectb(22, 28, 116, 68, 8)

        pyxel.text(LARGEUR // 2 - 20, 36, "GAME  OVER", 8)

        rang, col_rang = rang_pour_score(score)
        pyxel.text(LARGEUR // 2 - 4, 50, f"RANG", 6)
        pyxel.text(LARGEUR // 2 - 2, 58, rang, col_rang)

        s_txt = f"SCORE : {score:06d}"
        pyxel.text(LARGEUR // 2 - len(s_txt) * 2, 70, s_txt, 10)

        if score >= highscore and score > 0:
            hs_txt = "NOUVEAU RECORD !"
            col = 10 if pyxel.frame_count % 20 < 10 else 9
            pyxel.text(LARGEUR // 2 - len(hs_txt) * 2, 80, hs_txt, col)
        else:
            hs_txt = f"RECORD:{highscore:06d}"
            pyxel.text(LARGEUR // 2 - len(hs_txt) * 2, 80, hs_txt, 5)

        if pyxel.frame_count % 40 < 28:
            invite = "ESPACE pour rejouer"
            pyxel.text(LARGEUR // 2 - len(invite) * 2, 90, invite, 7)

    def dessiner_victoire(self, score, champ_etoiles, highscore=0):
        pyxel.cls(0)
        champ_etoiles.dessiner()
        pyxel.rect(18, 25, 124, 74, 1)
        pyxel.rectb(18, 25, 124, 74, 11)

        pyxel.text(LARGEUR // 2 - 20, 33, "VICTOIRE !", 11)

        rang, col_rang = rang_pour_score(score)
        pyxel.text(LARGEUR // 2 - 4, 47, "RANG", 6)
        pyxel.text(LARGEUR // 2 - 2, 55, rang, col_rang)

        s_txt = f"SCORE : {score:06d}"
        pyxel.text(LARGEUR // 2 - len(s_txt) * 2, 67, s_txt, 10)

        if score >= highscore and score > 0:
            hs_txt = "NOUVEAU RECORD !"
            col = 10 if pyxel.frame_count % 20 < 10 else 9
            pyxel.text(LARGEUR // 2 - len(hs_txt) * 2, 77, hs_txt, col)

        if pyxel.frame_count % 40 < 28:
            invite = "ESPACE pour rejouer"
            pyxel.text(LARGEUR // 2 - len(invite) * 2, 88, invite, 6)

    def dessiner_transition_vague(self, vague, compteur):
        if compteur > 0:
            msg = f"-- VAGUE {vague} --"
            col = 10 if pyxel.frame_count % 16 < 8 else 9
            pyxel.text(LARGEUR // 2 - len(msg) * 2, HAUTEUR // 2 - 4, msg, col)
