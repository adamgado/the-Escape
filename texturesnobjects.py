import pygame as pg
from settings import *


class Render:
    def __init__(self, game):
        self.game = game
        self.game.screen = game.screen
        self.wall_texture = self.wall_textures()
        self.ceil = self.load_texture('textures/ceiling.png', (WIDTH, HEIGHT // 2))
        self.ceil_offset = 0

    def draw(self):
        self.draw_ceiling()
        self.objects_render()
        
        
    def draw_ceiling(self):
        self.ceil_offset = (self.ceil_offset + 4.0 * self.game.player.rel) % WIDTH
        self.game.screen.blit(self.ceil, (-self.ceil_offset, 0))
        self.game.screen.blit(self.ceil, (-self.ceil_offset + WIDTH, 0))
        pg.draw.rect(self.game.screen, FLOOR, (0, (HEIGHT // 2), WIDTH, HEIGHT))
        
    def objects_render(self):
        objects_list = sorted(self.game.raycasting.objects, key=lambda t: t[0], reverse=True)
        for depth, image, pos in objects_list:
            self.game.screen.blit(image, pos)
        
    @staticmethod
    def load_texture(path, res=(TEXTURE, TEXTURE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def wall_textures(self):
        return self.load_texture('textures/wall.jpg')