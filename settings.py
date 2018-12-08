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
WIDTH = 1600 # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 960 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Lion's Quest"
BGCOLOR = BROWN

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tile_354.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_SPRITESHEET = 'test-hero.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(0, 0)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 500,
                     'rate': 175,
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
DETECT_RADIUS = 400

# Skeleton mob settings
SKELETON_MOB_SPEEDS = [25, 50, 75, 100] 
SKELETON_MOB_HEALTH = 40

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
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'Healthpack.png',
               'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'World Map.mp3'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav',]
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
SKELETON_HIT_SOUNDS = ['wood_falling_03.ogg']
WEAPON_SOUNDS = {'pistol': ['sfx_weapon_singleshot2.wav'],
                 'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}



