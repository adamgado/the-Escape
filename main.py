import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from texturesnobjects import *
from weapon import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.render = Render(self)
        self.raycasting = Raycasting(self)
        self.weapon = Weapon(self)
    
    def update(self):
        self.player.update()
        self.raycasting.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        #self.screen.fill('black')
        self.render.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()
        
    def run(self):
        while True:
            self.update()
            self.draw()
            self.events()
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.player.fire(event)
                

if __name__ == '__main__':
    game = Game()
    game.run()
