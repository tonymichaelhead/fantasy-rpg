# Hometown NPCs
MOUNTAIN_ENTRANCE_BOY = {'dialogue_1': ["You really shouldn't go in there..."],
                         'dialogue_2': ["I told you once, aint gonna say it again"],
                         'is_merchant': False,
                         'standing_frame_b': {'x': 4, 'y': 98, 'w': 24, 'h': 30, 'scale': (36, 48)},
                         'standing_frame_f': {'x': 68, 'y': 98, 'w': 24, 'h': 30, 'scale': (36, 48)},
                         'standing_frame_l': {'x': 38, 'y': 100, 'w': 24, 'h': 28, 'scale': (36, 48)}}

OLD_MAN_WORLD_ENTRANCE = {'dialogue_1': ["There are many fun tales to be had out there"],
                          'dialogue_2': ["Have fun young lad!"],
                          'is_merchant': False,
                          'standing_frame_b': {'x': 6, 'y': 2, 'w': 20, 'h': 30, 'scale': (36, 48)},
                          'standing_frame_f': {'x': 70, 'y': 2, 'w': 20, 'h': 30, 'scale': (36, 48)},
                          'standing_frame_l': {'x': 38, 'y': 2, 'w': 22, 'h': 30, 'scale': (36, 48)}}

GIRL_HOME             = {'dialogue_1': ["Tony! Thank goodness your here. It's my brother...",
                                        "He ran into into the woods this morning and he never came home",
                                        "With all the reports of strange monsters in the woods these days",
                                        "I'm worried something may have happenend to him...",
                                        "Please find him and bring him home safe."],
                        'dialogue_2': ["You must be very careful, there are lots of monsters out there!."],
                        'is_merchant': False,
                        'standing_frame_b': {'x': 4, 'y': 64, 'w': 24, 'h': 32, 'scale': (36, 48)},
                        'standing_frame_f': {'x': 68, 'y': 64, 'w': 24, 'h': 32, 'scale': (36, 48)}, 
                        'standing_frame_l': {'x': 38, 'y': 64, 'w': 20, 'h': 30, 'scale': (36, 48)}}

BROTHER             = {'dialogue_1': ["t-t-Tony?",
                                      "Oh boy, is it good to see you.",
                                      "I heard stories about the monsters in these woods",
                                      "I didn't believe them at first, so I went to see them myself.",
                                      "Please, let's just go home now.",
                                      "Come one, I know a shortcut!",
                                      "We can go out through that tunnel ahead...",          ],
                        'dialogue_2': ["C'mon, lets hurry home.",
                                       "My sister must be worried sick..."],                
                        'is_merchant': False,
                        'standing_frame_b': {'x': 4, 'y': 98, 'w': 24, 'h': 30, 'scale': (36, 48)},
                        'standing_frame_f': {'x': 68, 'y': 98, 'w': 24, 'h': 30, 'scale': (36, 48)},
                        'standing_frame_l': {'x': 38, 'y': 100, 'w': 24, 'h': 28, 'scale': (36, 48)}}

PRINCESS             = {'dialogue_1': ["Yo, I'm the princess."],
                        'dialogue_2': ["I'm srs m8."],
                        'is_merchant': False,
                        'standing_frame_b': {'x': 6, 'y': 32, 'w': 20, 'h': 32, 'scale': (36, 48)},
                        'standing_frame_f': {'x': 70, 'y': 32, 'w': 20, 'h': 32, 'scale': (36, 48)}, 
                        'standing_frame_l': {'x': 38, 'y': 32, 'w': 22, 'h': 32, 'scale': (36, 48)}}

MERCHANT_GEEZER      = {'dialogue_1': ["Back da truck up. I'm a merchant."],
                        'dialogue_2': ["Come back soon."],
                        'is_merchant': True,
                        'standing_frame_b': {'x': 6, 'y': 2, 'w': 20, 'h': 30, 'scale': (36, 48)},
                        'standing_frame_f': {'x': 70, 'y': 2, 'w': 20, 'h': 30, 'scale': (36, 48)},
                        'standing_frame_l': {'x': 38, 'y': 2, 'w': 22, 'h': 30, 'scale': (36, 48)}}

# NPC Dictionary
NPCS = {'mountain_entrance_boy': MOUNTAIN_ENTRANCE_BOY,
        'old_man_world_entrance': OLD_MAN_WORLD_ENTRANCE,
        'girl_home': GIRL_HOME,
        'merchant_geezer': MERCHANT_GEEZER,
        'princess': PRINCESS,
        'brother': BROTHER,}