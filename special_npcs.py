import pygame as pg
from npc_data import *
from sprites import Npc, Quest 

# Special character classes

class HomeGirl(Npc):
    def __init__(self, game, char_name, mode, facing, x, y):
        super().__init__(game, char_name, mode, facing, x, y)
        self.quest = None
        self.game.home_girl = self

    def talk(self):
        # Check if brother has been found and added to the game's variables
        try:
            self.game.brother
        except:
            brother_exists = False
        else:
            brother_exists = True
        if brother_exists:
            # Brother is being returned for the first time
            if self.game.brother.found and not self.game.brother.brought_home:
                self.game.brother.brought_home = True
                self.game.brother.joined_party = False
                # Brother must be added back to the all and walls sprite groups to appear
                self.game.all_sprites.add(self.game.brother)
                self.game.walls.add(self.game.brother)
                self.game.brother.facing = 'back'
                self.game.brother.update()
                self.dialogue_1 = NPCS[self.char_name]['found_dialogue_1']
                self.dialogue_2 = NPCS[self.char_name]['found_dialogue_2']
                self.talked_to = False
            super().talk()
            # If brother has been brought home and quest completed
            if self.quest:  
                if not self.quest.completed and self.game.brother.found:
                    self.quest.finish() 
        else:
            super().talk()
        # Start the quest if this is your first time talking to girl
        if not next((quest for quest in self.game.player.quests if quest.name == "Help girl find lost brother"), None):
            self.quest = Quest(self.game, self.game.player, "Help girl find lost brother", True)
            self.game.player.quests.append(self.quest)
            self.quest.sub_quests["Locate brother in the forest"]["active"] = True
            self.quest.start()

class Brother(Npc):
    def __init__(self, game, char_name, mode, facing, x, y):
        super().__init__(game, char_name, mode, facing, x, y)
        self.game.brother = self
        self.brought_home = False
        self.joined_party = False
        self.found = False

    def talk(self):
        if self.found:
            self.dialogue_1 = NPCS[self.char_name]['found_dialogue_1']
            self.dialogue_2 = NPCS[self.char_name]['found_dialogue_2']
            super().talk()
        else:
            super().talk()
            self.found = True
            self.joined_party = True
            self.talked_to = False
            # Check if quest has been initiated and initiate if not
            if not self.game.home_girl.quest:
                self.game.home_girl.quest = Quest(self.game, self.game.player, "Help girl find lost brother", True)
                self.game.player.quests.append(self.game.home_girl.quest)
                self.game.home_girl.quest.start()

    def update(self):
        if self.joined_party:
            # Disappear from the screen to join player party
            self.pos = (10000, 10000)
        elif self.brought_home:
            self.pos = (2070, 2254)
        super().update()

special_npcs = {'girl_home': HomeGirl,
                'brother': Brother}   