import pygame as pg
from collections import deque
import os
from random import randint, random, choice
from settings import *
"""functions that control npc logic and display and generation"""


class Npc:
    """function that creates an npc and all their attributes, logic and animation"""
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
        self.animation = animation
        self.animation_prev = pg.time.get_ticks()
        self.trigger = False
        self.attack = self.get_images('textures/npcs/attack')
        self.death = self.get_images('textures/npcs/death')
        self.idle = self.get_images('textures/npcs/idle')
        self.pain_img = self.get_images('textures/npcs/pain')
        self.walk = self.get_images('textures/npcs/walk')
        self.attack_img = self.get_images('textures/npcs/attack')
        
        self.attack_distance = randint(3, 6)
        self.size = 10
        self.health = 100
        self.damage = 10
        self.accuracy = 0.90
        self.alive = True
        self.pain = False
        self.ray_value = False
        self.frame_count = 0
        self.speed = 0.03
        self.player_search = False
        
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
        #self.draw_ray_cast()
        
    def wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def collision(self, dx, dy):
        if self.wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy
        
    def npc_move(self):
        next_pos = self.game.player.map_pos
        next_x, next_y = next_pos
        if next_pos not in self.game.npc_render.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.y)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.collision(dx, dy)
            
    def attack_animation(self):
        if self.trigger:
            self.game.sound.npc_attack.play()
            if random() < self.accuracy:
                self.game.player.take_damage(self.damage)
    def animate_death(self):
        if not self.alive:
            if self.game.u_trigger and self.frame_count < len(self.death) - 1:
                self.death.rotate(-1)
                self.image = self.death[0]
                self.frame_count += 1
        
    def hit(self):
        if self.ray_value and self.game.player.shot:
            if ((WIDTH // 2) - (self.proj_width // 2)) < self.screen_x < ((WIDTH // 2) + (self.proj_width // 2)):
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.get_health()
                
    def get_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()
                
    def damage_animation(self):
        self.animate(self.pain_img)
        if self.trigger:
            self.pain = False
            self.running = False
        
    def logic(self):
        if self.alive:
            self.ray_value = self.rays_to_npc()
            self.hit()
            if self.pain:
                self.damage_animation()
            elif self.ray_value:
                self.player_search = True
                if self.dist < self.attack_distance:
                    self.animate(self.attack_img)
                    self.attack_animation()
                else:
                    self.animate(self.walk)
                    self.npc_move()
            elif self.player_search:
                self.animate(self.walk)
                self.npc_move() 
            else:
                self.animate(self.idle)
        else:
            self.animate_death()
        
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
            
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def rays_to_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True
        wall_dist_vert, wall_dist_hor = 0, 0
        player_dist_vert, player_dist_hor = 0, 0
        
        player_x, player_y = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        texture_vert, texture_hor = 1, 1
        
        ray_angle = self.theta
        
        sin_ray = math.sin(ray_angle)
        cos_ray = math.cos(ray_angle)
           
        y_hor, dy = (y_map + 1, 1) if sin_ray > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - player_y) / sin_ray
        x_hor = player_x + depth_hor * cos_ray
            
        delta_depth = dy / sin_ray
        dx = delta_depth * cos_ray
            
        for a in range(DISTANCE):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_hor = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_hor = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth
            
        x_vert, dx = (x_map + 1, 1) if cos_ray > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - player_x) / cos_ray
        y_vert = player_y + depth_vert * sin_ray
            
        delta_depth = dx / cos_ray
        dy = delta_depth * sin_ray
            
        for a in range(DISTANCE):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_vert = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_vert = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
            
        player_dist = max(player_dist_vert, player_dist_hor)
        wall_dist = max(wall_dist_vert, wall_dist_hor)
    
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.rays_to_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)
