import pygame as pg
from random import random, uniform, choice, randint
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width /2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class SpriteSheet:
    # Utility class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        # For scaling images, leave commented out if not using
        # image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class  Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.shooting = False
        self.recovering = False
        self.facing = 'back'
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frame_b
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        # Player Stats
        self.level = 1
        self.exp = 0
        self.last_shot = 0
        self.last_recovering = 0
        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.damaged = False
    
    def load_images(self):
        # Standing
        self.standing_frame_b = self.game.spritesheet.get_image(35, 63, 24, 32)
        self.standing_frame_b = pg.transform.scale(self.standing_frame_b, (36, 48))
        self.standing_frame_f = self.game.spritesheet.get_image(35, 32, 26, 31)
        self.standing_frame_f = pg.transform.scale(self.standing_frame_f, (36, 48))
        self.standing_frame_l = self.game.spritesheet.get_image(33, 0, 28, 32)
        self.standing_frame_l = pg.transform.scale(self.standing_frame_l, (36, 48))
        self.standing_frame_r = pg.transform.flip(self.standing_frame_l, True, False)
        # # Walking
        self.raw_walk_frames_b = [self.game.spritesheet.get_image(3, 65, 26, 31),
                                  self.game.spritesheet.get_image(35, 63, 24, 32),
                                  self.game.spritesheet.get_image(67, 65, 26, 32)]
        self.walk_frames_b = []
        for frame in self.raw_walk_frames_b:
            self.walk_frames_b.append(pg.transform.scale(frame, (36, 48)))
        self.raw_walk_frames_f = [self.game.spritesheet.get_image(3, 34, 26, 31),
                                  self.game.spritesheet.get_image(35, 32, 26, 31),
                                  self.game.spritesheet.get_image(67, 33, 26, 32)]
        self.walk_frames_f = []
        for frame in self.raw_walk_frames_f:
            self.walk_frames_f.append(pg.transform.scale(frame, (36, 48)))
        self.raw_walk_frames_l = [self.game.spritesheet.get_image(0, 1, 29, 32),
                                  self.game.spritesheet.get_image(33, 0, 28, 32),
                                  self.game.spritesheet.get_image(65, 1, 28, 32)]
        self.walk_frames_l = []
        for frame in self.raw_walk_frames_l:
            self.walk_frames_l.append(pg.transform.scale(frame, (36, 48)))
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            self.walk_frames_r.append(pg.transform.flip(frame, True, False))
        # Shooting pistol
        self.raw_shooting_pistol_frames_l = [self.game.spritesheet.get_image(100, 2, 28, 30)]
        self.shooting_pistol_frames_l = []   
        for frame in self.raw_shooting_pistol_frames_l:
            self.shooting_pistol_frames_l.append(pg.transform.scale(frame, (36, 48)))
        self.shooting_pistol_frames_r = []
        for frame in self.shooting_pistol_frames_l:
            self.shooting_pistol_frames_r.append(pg.transform.flip(frame, True, False))
        self.raw_shooting_pistol_frames_b = [self.game.spritesheet.get_image(100, 66, 24, 30)]
        self.shooting_pistol_frames_b = []
        for frame in self.raw_shooting_pistol_frames_b:
            self.shooting_pistol_frames_b.append(pg.transform.scale(frame, (36, 48)))
        # # Jumping
        # self.jump_frame_r = self.game.spritesheet.get_image(100, 184, 72, 68)
        # self.jump_frame_l = pg.transform.flip(self.jump_frame_r, True, False)
        # # Throwing
        # self.throw_frame_r = self.game.spritesheet.get_image(104, 96, 64, 72)
        # self.throw_frame_l = pg.transform.flip(self.throw_frame_r, True, False)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if not self.recovering:
                self.walking = True
                self.facing = 'left'
                self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)
        elif keys[pg.K_RIGHT] or keys[pg.K_s]:
            if not self.recovering:
                self.walking = True
                self.facing = 'right'
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        elif keys[pg.K_UP] or keys[pg.K_w]:
            if not self.recovering:
                self.walking = True
                self.facing = 'forward'
                self.vel = vec(0, -PLAYER_SPEED).rotate(-self.rot)
        elif keys[pg.K_DOWN] or keys[pg.K_r]:
            if not self.recovering:
                self.walking = True
                self.facing = 'back'
                self.vel = vec(0, PLAYER_SPEED).rotate(-self.rot)
        else:
            self.walking = False
        if keys[pg.K_1]:
            self.weapon = 'pistol'
        if keys[pg.K_2]:
            self.weapon = 'shotgun'
        if keys[pg.K_SPACE]:
            self.shooting = True
            self.shoot()


    def calculateExp(self):
        if self.exp >= 100:
            if self.exp > 100:
                remainder = self.exp - 100
            else:
                remainder = 0
            self.level += 1
            self.exp = 0 + remainder
            
    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            self.recovering = True
            self.recovering_start = now
            # Determine direction and kickback
            if self.facing == 'left':
                dir = vec(-1, 0)
                self.vel = vec(WEAPONS[self.weapon]['kickback'], 0)
            elif self.facing == 'right':
                dir = vec(1, 0)
                self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0)        
            elif self.facing == 'forward':
                dir = vec(0, -1)
                self.vel = vec(0, WEAPONS[self.weapon]['kickback'])
            elif self.facing == 'back':
                dir = vec(0, 1)
                self.vel = vec(0, -WEAPONS[self.weapon]['kickback'])
            # Barrel Offset
            if self.facing == 'right':
                pos = self.pos + BARREL_OFFSET_r
            if self.facing == 'left':
                pos = self.pos + BARREL_OFFSET_l
            if self.facing == 'forward':
                pos = self.pos + BARREL_OFFSET_f
            if self.facing == 'back':
                pos = self.pos + BARREL_OFFSET_b
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                choice(self.game.weapon_sounds[self.weapon]).play()
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def talk(self):
        hits = pg.sprite.spritecollide(self, self.game.npcs, False)
        if hits:
            if not hits[0].talked_to:
                for line in hits[0].dialogue_1:
                    self.game.draw_dialogue(line)
                    pg.display.flip()
                    self.game.wait_for_key()
                hits[0].talked_to = True
            else:
                for line in hits[0].dialogue_2:
                    self.game.draw_dialogue(line)
                    pg.display.flip()
                    self.game.wait_for_key()

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def update(self):
        self.calculateExp()
        self.get_keys()
        if self.shooting:
            now = pg.time.get_ticks() # Maybe move to a higher level of update() to share
            if now - self.last_shot > WEAPONS[self.weapon]['rate']:
                self.shooting = False
        if self.recovering:
            now = pg.time.get_ticks()
            if now - self.recovering_start > WEAPONS[self.weapon]['rate']:
                self.recovering = False
        self.animate()
        # self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #TODO: probably not gonna rotate
        # self.image = pg.transform.rotate(self.image, self.rot)
        self.image = self.image.copy() # A copy seems to need to be made for damage
        if self.damaged:
            try:
                pass
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
             
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
   
    def animate(self):
        now = pg.time.get_ticks()
        # if self.vel.x != 0:
        #     self.walking = True
        # else:
        #     self.walking = False
        # Draw gun if shooting
        if self.shooting and now - self.last_shot < WEAPONS[self.weapon]['rate']:
            self.last_update = now
            # self.walking = False
            self.current_frame = (self.current_frame + 1) % len(self.shooting_pistol_frames_l)
            bottom = self.rect.bottom
            if self.facing == 'back':
                self.image = self.shooting_pistol_frames_b[self.current_frame]
            elif self.facing == 'forward':
                self.image = self.standing_frame_f
            elif self.facing == 'left':
                self.image = self.shooting_pistol_frames_l[self.current_frame]
            elif self.facing == 'right':
                self.image = self.shooting_pistol_frames_r[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        # Show walking animation    
        elif self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_b)
                bottom = self.rect.bottom
                if self.facing == 'back':
                    # self.facing = 'back'
                    self.image = self.walk_frames_b[self.current_frame]
                elif self.facing == 'forward':
                    # self.facing = 'forward'
                    self.image = self.walk_frames_f[self.current_frame]
                elif self.facing == 'left':
                    # self.facing = 'left'
                    self.image = self.walk_frames_l[self.current_frame]
                elif self.facing == 'right':
                    # self.facing = 'right'
                    self.image = self.walk_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        else:
            if self.facing == 'back':
                self.image = self.standing_frame_b
            elif self.facing == 'forward':
                self.image = self.standing_frame_f
            elif self.facing == 'left':
                self.image = self.standing_frame_l
            elif self.facing == 'right':
                self.image = self.standing_frame_r

        # else: # TODO: MAYBE??
        #     bottom = self.rect.bottom
        #     self.last_update = now
        #     self.current_frame = (self.current_frame + 1) % len(self.walk_frames_b)
        #     self.rect = self.image.get_rect()
        #     self.rect.bottom = bottom

        # TODO: Possibly use for pixel collisions
        # self.mask = pg.mask.from_surface(self.image)

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = (0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
    
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
    
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class SkeletonMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.skeleton_mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.facing = 'right'
        self.image = self.standing_frame_r.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = (0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = SKELETON_MOB_HEALTH
        self.speed = choice(SKELETON_MOB_SPEEDS)
        self.target = game.player
        self.mode = 'dormant'
    
    def load_images(self):
        # Standing
        self.standing_frame_r = self.game.mob_spritesheet.get_image(56, 155, 29, 35)
        self.standing_frame_r = pg.transform.scale(self.standing_frame_r, (48, 57))
        self.standing_frame_l = pg.transform.flip(self.standing_frame_r, True, False) 

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def dormant(self):
        pass # code to wander around

    def update(self):
        if self.facing == 'right':
            self.image = self.standing_frame_r.copy()
        else:
            self.image = self.standing_frame_l.copy()
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            # self.rot = target_dist.angle_to(vec(1, 0))
            # self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos # TODO: probably should comment out
            # self.acc = vec(1, 0).rotate(-self.rot)
            self.acc = target_dist.normalize()
            if target_dist[0] > 0:
                self.facing = 'right'
            else:
                self.facing = 'left'
            self.avoid_mobs()
            # print(self.acc)
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        else:
            # put into chill mode
            pass
        if self.health <= 0:
            choice(self.game.skeleton_hit_sounds).play()
            self.kill()
            self.game.player.exp += SKELETON_EXP
            self.game.map_img.blit(self.game.skeleton_parts, self.pos - vec(32, 32))
     
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / SKELETON_MOB_HEALTH)
        self.health_bar = pg.Rect(0, 5, width, 7)
        if self.health < SKELETON_MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Npc(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.npcs, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.dialogue_1 = ['Hey, I really wish you well on your quest.']
        self.dialogue_2 = ['Stop talking to me.']
        self.talked_to = False
        self.facing = 'right'
        self.image = self.standing_frame_r.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = (0, 0)
        self.rect.center = self.pos
        # self.rot = 0
        # self.health = SKELETON_MOB_HEALTH
        self.speed = choice(SKELETON_MOB_SPEEDS)
        # self.target = game.player
        self.mode = 'dormant'
    
    def load_images(self):
        # Standing
        self.standing_frame_r = self.game.mob_spritesheet.get_image(56, 155, 29, 35)
        self.standing_frame_r = pg.transform.scale(self.standing_frame_r, (48, 57))
        self.standing_frame_l = pg.transform.flip(self.standing_frame_r, True, False) 

    def update(self):
        if self.facing == 'right':
            self.image = self.standing_frame_r.copy()
        else:
            self.image = self.standing_frame_l.copy()

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        # spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self .vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Exit(pg.sprite.Sprite):
    def __init__(self, game, map_file, music_file, spawn_player_x, spawn_player_y, x, y, w, h):
        self.groups = game.exits
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.map_file = map_file
        self.music_file = music_file
        self.spawn_player_x = spawn_player_x
        self.spawn_player_y = spawn_player_y
        
class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # Bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
