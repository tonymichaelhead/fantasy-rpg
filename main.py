# Pygame/Python Template

import pygame as pg
import sys
from os import path
import random
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        # Initialize game window, etc
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        # set pg.RESIZABLE flag to get resize event VIDEORESIZE size, w, h
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_dialogue(self, text):
        dialogue_box = pg.Surface((WIDTH / 2, 100)).convert_alpha()
        dialogue_box.fill((0,0,0, 180))
        dialogue_rect = dialogue_box.get_rect()
        dialogue_rect.center = (WIDTH / 2, HEIGHT / 2)
        self.screen.blit(dialogue_box, dialogue_rect)
        self.draw_text(text, self.hud_font, 20, WHITE, WIDTH / 2, HEIGHT / 2, align="center")

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        self.music_folder = path.join(game_folder, 'music')
        # Load sprite sheets
        self.spritesheet = SpriteSheet(path.join(img_folder, PLAYER_SPRITESHEET))
        self.mob_spritesheet = SpriteSheet(path.join(img_folder, MOB_SPRITESHEET))
        self.skeleton_parts_spritesheet = SpriteSheet(path.join(img_folder, SKELETON_PARTS_SPRITESHEET))
        self.npc_spritesheet = SpriteSheet(path.join(img_folder, NPC_SPRITESHEET))
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0, 180))
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['lg'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (7, 7))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.skeleton_parts = self.skeleton_parts_spritesheet.get_image(137, 256, 55, 57)
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # Lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.1)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder,snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder,snd)))
        self.skeleton_hit_sounds = []
        for snd in SKELETON_HIT_SOUNDS:
            self.skeleton_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder,snd)))

    def new(self):
        # Start a new game and initialize all variables and do all the setup
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.exits = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.skeleton_mobs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'forest1.tmx'))
        self.map_img = self.map.make_map()
        self.map_img = pg.transform.scale(self.map_img, (self.map.width, self.map.height))
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'skeleton':
                SkeletonMob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'npc':
                Npc(self, tile_object.npc_name, tile_object.mode, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, 
                         tile_object.width, tile_object.height)
            if tile_object.name == 'exit':
                Exit(self, tile_object.map_file, tile_object.music_file, tile_object.spawn_player_x, 
                     tile_object.spawn_player_y, tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        # self.effects_sounds['level_start'].play()
        self.paused = False
        self.night = False
        # self.effects_sounds['level_start'].play()

    def run(self):
        # Game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
    
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        self.camera.update(self.player)
        # Game over?
        # if len(self.mobs) == 0:
        #     self.playing = False
        # Player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
        # Player hits 
        # Player hits exits
        hits = pg.sprite.spritecollide(self.player, self.exits, False)
        for hit in hits:
            self.change_map(hit.map_file, hit.music_file, hit.spawn_player_x, hit.spawn_player_y)
        # Mob hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            target_dist = self.player.pos - hit.pos
            self.player.acc = target_dist.normalize()
            self.player.pos += (self.player.acc.x * MOB_KNOCKBACK, self.player.acc.y * MOB_KNOCKBACK)
        # Bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # Draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # Game loop - draw
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob) or isinstance(sprite, SkeletonMob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        if self.night:
            self.render_fog()
        # *after* drawing everything, flip the display
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text("Stats", self.hud_font, 30, WHITE, 
                       WIDTH - 10, 10, align="ne")
        self.draw_text("Lvl: {}".format(self.player.level), self.hud_font, 30, WHITE, 
                       WIDTH - 10, 40, align="ne")
        self.draw_text("Exp: {}".format(self.player.exp), self.hud_font, 30, WHITE, 
                       WIDTH - 10, 70, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key ==pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_RCTRL:
                    self.player.talk()
                # if event.key == pg.K_l:
                #     self.change_map('forest1.tmx')
                # if event.key == pg.K_u:
                #     self.change_map('begins.tmx')
    
    def change_map(self, map_file, music_file, spawn_player_x, spawn_player_y):
        # Load new map, pass current game state to change maps mid game
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.walls.empty()
        self.exits.empty()
        self.mobs.empty()
        self.skeleton_mobs.empty()
        self.bullets.empty()
        self.items.empty()
        self.map = TiledMap(path.join(self.map_folder, map_file))
        self.map_img = self.map.make_map()
        self.map_img = pg.transform.scale(self.map_img, (self.map.width, self.map.height))
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player.pos.x = float(spawn_player_x) 
                self.player.pos.y = float(spawn_player_y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'skeleton':
                SkeletonMob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'npc':
                Npc(self, tile_object.npc_name, tile_object.mode, tile_object.facing, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, 
                         tile_object.width, tile_object.height)
            if tile_object.name == 'exit':
                Exit(self, tile_object.map_file, tile_object.music_file, tile_object.spawn_player_x, 
                     tile_object.spawn_player_y, tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        # self.effects_sounds['level_start'].play()
        self.paused = False
        self.night = False

        # Kill old BGM and load new map music
        pg.mixer.music.load(path.join(self.music_folder, music_file))
        pg.mixer.music.play(loops=-1)
            
    def show_start_screen(self):
        # Game splash/start screen
        pass

    def show_go_screen(self):
        # Game over/continue
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED, 
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, 
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()