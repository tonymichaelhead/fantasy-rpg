from sprites import Npc
from npc_data import *

# Special character classes

class HomeGirl(Npc):

    def talk(self):
        if self.game.brother_found:
            self.dialogue_1 = NPCS[self.char_name]['found_dialogue_1']
            self.dialogue_2 = NPCS[self.char_name]['found_dialogue_2']
            super().talk()
        else:
            super().talk()    

class Brother(Npc):

    def talk(self):
        if self.game.brother_found:
            self.dialogue_1 = NPCS[self.char_name]['found_dialogue_1']
            self.dialogue_2 = NPCS[self.char_name]['found_dialogue_2']
            super().talk()
        else:
            self.game.brother_found = True
            super().talk()
            self.talked_to = False    

special_npcs = {'girl_home': HomeGirl,
                'brother': Brother}   