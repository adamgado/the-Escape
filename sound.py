import pygame as pg
"""add audio to the game"""


class Sound:
    """class that initializes the sounds to be called in game"""
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.gun = pg.mixer.Sound('textures/sound/gun.wav')
        self.npc_pain = pg.mixer.Sound('textures/sound/pain.mp3')
        self.npc_death = pg.mixer.Sound('textures/sound/death.mp3')
        self.npc_attack = pg.mixer.Sound('textures/sound/npc_shot.mp3')
        self.player_pain = pg.mixer.Sound('textures/sound/player_pain.mp3')
