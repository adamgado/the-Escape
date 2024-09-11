import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.gun = pg.mixer.Sound('textures/sound/gun.wav')