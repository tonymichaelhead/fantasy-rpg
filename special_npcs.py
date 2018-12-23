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

special_npcs = {'girl_home': HomeGirl}   