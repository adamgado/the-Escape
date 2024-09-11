from npc import *


class Npc_render:
    def __init__(self, game):
        self.game = game
        self.npc_list = []
        self.npc_path = 'textures/npc'
        new_npc = self.new_npc
        
        new_npc(Npc(game))

    def update(self):
        for npc in self.npc_list:
            npc.update()
        
    def new_npc(self, npc):
        self.npc_list.append(npc)
        