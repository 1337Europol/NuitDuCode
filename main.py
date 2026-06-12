import pyxel
from src.nuitducode.utils import LARGEUR, HAUTEUR, FPS, TITRE
from src.nuitducode.core import Jeu


class Application:
    def __init__(self):
        pyxel.init(LARGEUR, HAUTEUR, title=TITRE, fps=FPS)
        self.jeu = Jeu()
        pyxel.run(self.mise_a_jour, self.dessiner)

    def mise_a_jour(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        self.jeu.mise_a_jour()

    def dessiner(self):
        self.jeu.dessiner()


Application()
