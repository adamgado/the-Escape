import pygame as pg
from settings import *
from collections import deque
import os
"""add a weapon to the game"""


class Weapon:
    """class that runs the weapon and its functions and animations"""
    def __init__(self, game, path='textures/weapon/0.png', scale=0.4, animation=90):
        self.game = game
        self.player = game.player
        self.path = path
        self.image = pg.image.load(path).convert_alpha()
        self.images = self.get_images(self.path)
        self.animation = animation
        self.animation_prev = pg.time.get_ticks()
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
            for img in self.images])
        self.weapon_pos = ((WIDTH // 2) - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frames = 0
        self.damage = 50
        
    def animation_time(self):
        self.trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_prev > self.animation:
            self.animation_prev = time_now
            self.trigger = True
        
    def shoot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frames += 1
                if self.frames == self.num_images:
                    self.reloading = False
                    self.frames = 0
        
    def get_images(self, path):
        images = deque()
        path_dir = 'textures/weapon/'
        for file_name in os.listdir(path_dir):
            if os.path.isfile(os.path.join(path_dir, file_name)):
                img =pg.image.load(path_dir + '/' + file_name).convert_alpha()
                images.append(img)
        return images
        
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
        
    def update(self):
        self.animation_time()
        self.shoot()
