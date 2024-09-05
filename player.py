from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE
        self.shot = False
        
    def fire(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.shot = True
                self.game.weapon.reloading = True
        
    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
            
        self.collision(dx, dy)
        
        #if keys[pg.K_RIGHT]:
            #self.angle += PLAYER_ROTATION * self.game.delta_time
        #if keys[pg.K_LEFT]:
            #self.angle -= PLAYER_ROTATION * self.game.delta_time
        self.angle %= math.tau
        
    def draw(self):
        """pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)"""
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)
    
    def update(self):
        self.move()
        self.mouse()
        
    def wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.delta_time
        if self.wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
            
    def mouse(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_x > BORDER_RIGHT or mouse_x < BORDER_LEFT:
            pg.mouse.set_pos([(WIDTH // 2),(HEIGHT // 2)])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX, min(MOUSE_MAX, self.rel))
        self.angle += self.rel * MOUSE_SENS * self.game.delta_time

    @property
    def pos(self):
        return self.x, self.y
        
    @property
    def map_pos(self):
        
        return int(self.x), int(self.y)
