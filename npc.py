import pygame as pg
from collections import deque
import os
from random import randint, random, choice
from settings import *


class Npc:
    def __init__(self, game, path='textures/npcs/0.png', pos=(10.5, 5.5),
                 scale=0.8, shift=0.25, animation=180):
        self.game = game
        self.player = game.player
        self.path = path.rsplit('/', 1)[0]
        self.x, self.y = pos
        self.dx, self.dy, self.theta = 0, 0, 0
        self.screen_x, self.dist, self.norm_dist = 0, 1, 1
        self.image = pg.image.load(path).convert_alpha()
        self.ratio = self.image.get_width() / self.image.get_height()
        self.scale = scale
        self.shift = shift
        self.running = False
        self.animation = animation
        self.animation_prev = pg.time.get_ticks()
        self.trigger = False
        self.attack = self.get_images('textures/npcs/attack')
        self.death = self.get_images('textures/npcs/death')
        self.idle = self.get_images('textures/npcs/idle')
        self.pain_img = self.get_images('textures/npcs/pain')
        
        self.attack_distance = randint(3, 6)
        self.size = 10
        self.health = 100
        self.damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        
    def projection(self):
        proj = SCREEN / self.norm_dist * self.scale
        proj_width, proj_height = proj * self.ratio, proj
        self.proj_width = proj_width
        image = pg.transform.scale(self.image, (proj_width, proj_height))
        pos = self.screen_x - (proj_width // 2), (HEIGHT // 2) - proj_height // 2 + (proj_height * self.shift)
        
        self.game.raycasting.objects.append((self.norm_dist, image, pos))
        
    def get_npc(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)
        delta_angle = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta_angle += math.tau
            
        delta_rays = delta_angle / RAYS_ANGLE
        self.screen_x = (HALF_RAYSNUM + delta_rays) * SCALE
        
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta_angle)
        if (self.image.get_width() // 2) < self.screen_x < (WIDTH + (self.image.get_width() // 2)) and self.norm_dist > 0.5:
            self.projection()
            
    def update(self):
        self.get_npc()
        self.animation_time()
        self.logic()
        
    def hit(self):
        if self.game.player.shot:
            if ((WIDTH // 2) - (self.proj_width // 2)) < self.screen_x < ((WIDTH // 2) + (self.proj_width // 2)):
                self.game.player.shot = False
                self.pain = True
                
    def damage_animation(self):
        self.animate(self.pain_img)
        if self.trigger:
            self.pain = False
            self.running = False
        
    def logic(self):
        if self.alive:
            self.hit()
            if self.pain:
                self.damage_animation()
            else:
                self.animate(self.idle)
        
    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img =pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
    
    def animate(self, images):
        if self.trigger:
            images.rotate(-1)
            self.image = images[0]            
    
    def animation_time(self):
        self.trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_prev > self.animation:
            self.animation_prev = time_now
            self.trigger = True
            
