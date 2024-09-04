import pygame as pg
from settings import *
import math
from texturesnobjects import *


class Raycasting:
    def __init__(self, game):
        self.game = game
        self.result = []
        self.objects = []
        self.textures = self.game.render.wall_texture
    
    def get_objects(self):
        self.objects = []
        for ray, values in enumerate(self.result):
            depth, projected_height, texture, off_set = values
            
            if projected_height < HEIGHT:
                column = self.textures.subsurface(
                    off_set * (TEXTURE - SCALE), 0, SCALE, TEXTURE
                )
                column = pg.transform.scale(column, (SCALE, projected_height))
                wall_position = (ray * SCALE, (HEIGHT // 2) - projected_height // 2)
            else:
                texture_height = TEXTURE * HEIGHT / projected_height
                column = self.textures.subsurface(
                    off_set * (TEXTURE - SCALE), (TEXTURE // 2) - texture_height // 2,
                    SCALE, texture_height
                )
                column = pg.transform.scale(column, (SCALE, HEIGHT))
                wall_position = (ray * SCALE, 0)
            self.objects.append((depth, column, wall_position))
        
    def rays(self):
        self.result = []
        player_x, player_y = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        texture_vert, texture_hor = 1, 1
        
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
                    texture_hor = self.game.map.world_map[tile_hor]
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
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                if cos_ray > 0:
                    off_set = y_vert
                else:
                    off_set = 1 - y_vert 
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                if sin_ray > 0:
                    off_set = x_hor
                else:
                    off_set = 1 - x_hor 
                
            # temporary view for testing
            #pg.draw.line(self.game.screen, 'yellow', (100 * player_x, 100 * player_y),
                         #(100 * player_x + 100 * depth * cos_ray, 100 * player_y + 100 * depth * sin_ray), 2)
                         
            depth *= math.cos(self.game.player.angle - ray_angle)
            projected_height = SCREEN / (depth + 0.00001)
            #lighting = [200 / (1 + depth ** 5 * 0.00001)] * 3
            #pg.draw.rect(self.game.screen, lighting, (ray * SCALE, (HEIGHT // 2) - projected_height // 2, SCALE, projected_height))
            self.result.append((depth, projected_height, texture, off_set))

            ray_angle += RAYS_ANGLE
    
    def update(self):
        self.rays()
        self.get_objects()
