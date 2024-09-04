import pygame as pg
from settings import *
from pathlib import Path

class Render:
    def __init__(self, game):
        self.game = game
        self.game.screen = game.screen
        self.wall_texture = self.wall_textures()
        
    @staticmethod
    def load_texture(path, res=(TEXTURE, TEXTURE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def wall_textures(self):
        texture_path = str(Path.cwd()) + 'textures\wall.avif'
        return self.load_texture(texture_path)