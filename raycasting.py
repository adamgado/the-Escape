import pygame as pg
from settings import *
import math


class Raycasting:
    def __init__(self, game):
        self.game = game
        
    def rays(self):
        player_x, player_y = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        
        ray_angle = self.game.player.angle - (FOV / 2) + 0.0001
        for ray in range(RAYSNUM):
            sin_ray = math.sin(ray_angle)
            cos_ray = math.cos(ray_angle)
            
            y_hor, dy = (y_map + 1, 1) if sin_ray > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - player_y) / sin_ray
            x_hor = player_x + depth_hor * cos_ray
            
            delta_depth = dy / sin_ray
            dx = delta_depth * cos_ray
            
            for a in range(DISTANCE):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
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
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor
                
            # temporary view for testing
            pg.draw.line(self.game.screen, 'yellow', (100 * player_x, 100 * player_y),
                         (100 * player_x + 100 * depth * cos_ray, 100 * player_y + 100 * depth * sin_ray), 2)
            
            ray_angle += RAYS_ANGLE
    
    def update(self):
        self.rays()