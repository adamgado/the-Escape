from npc import *
"""function that places all npcs on the map and generates new ones"""


class Npc_render:
    """class to render NPCs on the map"""
    def __init__(self, game):
        self.game = game
        self.npc_list = []
        self.npc_path = 'textures/npc'
        new_npc = self.new_npc
        self.npc_positions = {}
        
        new_npc(Npc(game))
        new_npc(Npc(game, pos=(12.5, 5.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        for npc in self.npc_list:
            npc.update()
        
    def new_npc(self, npc):
        self.npc_list.append(npc)
        
