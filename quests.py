import pygame as pg
from settings import *
import collections

# Sub quests
FIND_BROTHER_SUBS = collections.OrderedDict()
FIND_BROTHER_SUBS["Locate brother in the forest"] = { "active": False, "completed": False }
FIND_BROTHER_SUBS["Return brother to girl"] = { "active": False, "completed": False }

# Quest data
QUEST_DATA = {"find_brother": {"description": "Help girl find her brother",
                               "sub_quests": FIND_BROTHER_SUBS} }

class Quest:
    def __init__(self, game, player, description, main_quest, sub_quests):
        self.game = game
        self.player = player
        self.description = description
        self.main_quest = main_quest
        self.active = False
        self.completed = False
        self.sub_quests = sub_quests
    
    # Show starting of quest alert and details
    def start(self):
        self.active = True
        pg.mixer.music.pause()
        self.game.effects_sounds['quest_start'].play()
        self.game.screen.blit(self.game.dim_screen, (0, 0))
        # Draw side bar
        self.game.draw_text("New Quest!", self.game.hud_font, 45, WHITE, 
                        WIDTH / 2, HEIGHT / 3 - 50, align="center")
        self.game.draw_text(self.description, self.game.hud_font, 30, WHITE, 
                        WIDTH / 2, HEIGHT / 3 + 50, align="center")
        for i,sub_quest in enumerate(self.sub_quests):
            if self.sub_quests[sub_quest]["active"]:
                self.game.draw_text("-> {}".format(sub_quest), self.game.hud_font, 18, WHITE, 
                                WIDTH / 2, HEIGHT / 3 + 80 + i * 30, align="center")
        pg.display.flip()
        pg.time.delay(2000)
        pg.event.clear()
        pg.mixer.music.unpause()
        pg.mixer.music.set_volume(0.1)
        self.game.wait_for_confirm()
        pg.mixer.music.set_volume(1)
    
    def finish(self):
        self.active = False
        self.completed = True
        pg.mixer.music.pause()
        self.game.effects_sounds['level_up'].play()
        self.game.screen.blit(self.game.dim_screen, (0, 0))
        # Draw side bar
        self.game.draw_text("Completed Quest!", self.game.hud_font, 45, WHITE, 
                        WIDTH / 2, HEIGHT / 3 - 50, align="center")
        self.game.draw_text("X {}".format(self.description), self.game.hud_font, 30, WHITE, 
                        WIDTH / 2, HEIGHT / 3 + 50, align="center")
        for i,sub_quest in enumerate(self.sub_quests):
            if self.sub_quests[sub_quest]["completed"]:
                self.game.draw_text("X {}".format(sub_quest), self.game.hud_font, 18, WHITE, 
                                WIDTH / 2, HEIGHT / 3 + 80 + i * 30, align="center")
        pg.display.flip()
        pg.time.delay(2000)
        pg.event.clear()
        pg.mixer.music.unpause()
        pg.mixer.music.set_volume(0.1)
        self.game.wait_for_confirm()
        pg.mixer.music.set_volume(1)

    def finish_sub_quest(self, quest_name):
        self.sub_quests[quest_name]["active"] = False
        self.sub_quests[quest_name]["completed"] = True
        pg.mixer.music.pause()
        self.game.effects_sounds['level_up'].play()
        self.game.screen.blit(self.game.dim_screen, (0, 0))
        # Draw side bar
        self.game.draw_text("Completed Sub-Quest!", self.game.hud_font, 45, WHITE, 
                        WIDTH / 2, HEIGHT / 3 - 50, align="center")
        self.game.draw_text(self.description, self.game.hud_font, 30, WHITE, 
                        WIDTH / 2, HEIGHT / 3 + 50, align="center")
        for i,sub_quest in enumerate(self.sub_quests):
            if self.sub_quests[sub_quest]["completed"]:
                self.game.draw_text("X {}".format(sub_quest), self.game.hud_font, 18, WHITE, 
                                WIDTH / 2, HEIGHT / 3 + 80 + i * 30, align="center")
            if self.sub_quests[sub_quest]["active"]:
                self.game.draw_text("-> {}".format(sub_quest), self.game.hud_font, 18, WHITE, 
                                WIDTH / 2, HEIGHT / 3 + 80 + i * 30, align="center")
        pg.display.flip()
        pg.time.delay(2000)
        pg.event.clear()
        pg.mixer.music.unpause()
        pg.mixer.music.set_volume(0.1)
        self.game.wait_for_confirm()
        pg.mixer.music.set_volume(1)


