import math

"""game settings"""
RES = WIDTH, HEIGHT = 1600, 900
FPS = 60

"""Player attribute constants"""
PLAYER_POSITION = 1.5, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROTATION = 0.002
PLAYER_SIZE = 60
MAX_HEALTH = 100

"""mouse controls constants"""
MOUSE_SENS = 0.0002
MOUSE_MAX = 40
BORDER_LEFT = 100
BORDER_RIGHT = WIDTH - BORDER_LEFT

"""raycasting and 3d projection constants"""
FLOOR = (30, 30, 30)
FOV = math.pi / 2
RAYSNUM = WIDTH // 2
RAYS_ANGLE = FOV / RAYSNUM
DISTANCE = 20
HALF_RAYSNUM = RAYSNUM // 2
SCREEN = (WIDTH // 2) / math.tan(FOV / 2)
SCALE = WIDTH // RAYSNUM
TEXTURE = 256
