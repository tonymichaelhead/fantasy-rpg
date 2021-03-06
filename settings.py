import pygame as pg
vec = pg.math.Vector2

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0,0)
GREEN = (0, 255,0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# Game options/settings
WIDTH = 1100 # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 620 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Castlewalker"
BGCOLOR = BROWN

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tile_354.png'

# Player settings
PLAYER_INIT_HEALTH = 100
PLAYER_INIT_MP = 20
PLAYER_INIT_ATTACK = 5
PLAYER_SPEED = 200
ATTACK_FREQUENCY = 200
ATTACK_RECOVERY = 0
ATTACK_BUFFER = 350 # After attacking, gives some 
ATTACK_LUNGE = [5 for i in range(0, 7, 1)] + [-5 for i in range(0, 7, 1)]
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_SPRITESHEET = 'test-hero.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET_l = vec(-23, 10)
BARREL_OFFSET_r = vec(23, 10)
BARREL_OFFSET_f = vec(0, -23)
BARREL_OFFSET_b = vec(-8, 26)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 500,
                     'rate': 200,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 350,
                      'bullet_lifetime': 1000,
                      'rate': 900,
                      'kickback': 2000,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12}

# Mob spritesheets
MOB_SPRITESHEET = 'rpgcritters2.png'

# Mob template/Zombie
# Mob settings
MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEEDS = [150, 100, 75, 175, 150] 
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 500

# Skeleton mob settings
SKELETON_MOB_SPEEDS = [25, 50, 75, 100] 
SKELETON_MOB_HEALTH = 40
SKELETON_EXP = 10
GOLD_DROP_PROBABILITY = 0.2

# NPC settings
NPC_SPRITESHEET = '32-npc.png'
NPC_GATE = [0.5 for i in range(0, 200, 1)] + [-0.5 for i in range(0, 200, 1)]

# Effects
MUZZLE_FLASHES = ['smoke_05.png', 'smoke_06.png', 'smoke_07.png', 'smoke_08.png']
SPLAT = 'splat red.png'
SKELETON_PARTS_SPRITESHEET = 'skeleton.png'
FLASH_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (1000, 1000)
LIGHT_MASK = "light_350_med.png"

# Layers
WALL_LAYER = 3
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'Healthpack.png',
               'shotgun': 'obj_shotgun.png'}
GOLD_SPRITESHEET = 'gold.png'
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
START_BGM = 'RPG Ambient 3.mp3'
BG_MUSIC = 'TownTheme.mp3'
MUSIC_HOME_TOWN = 'TownTheme.mp3'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav',]
MOB_HIT_SOUND = 'wood_hit_04.ogg'
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
SKELETON_HIT_SOUNDS = ['wood_falling_03.ogg']
WEAPON_SOUNDS = {'pistol': ['sfx_weapon_singleshot2.wav'],
                 'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'gold_drop': 'metal_falling_02.ogg',
                  'gold_drop_2': 'tools_10.ogg',
                  'gold_pickup': 'keys_05.ogg',
                  'level_up': 'piano.wav',
                  'quest_start': 'snare.wav'}
ATTACK_SOUNDS = {'punch': ['jump1.ogg']}



