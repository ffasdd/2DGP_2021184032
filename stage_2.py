import random
import time
import pico2d
from pico2d import *
import game_framework
import stage_select_state
import game_world
import game_over
import game_clear
import pause_state


running = True

PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class BG:
    def __init__(self):
        self.image = load_image('resource/background2.png')

    def draw(self):
        global x
        self.image.draw(1060-x*2, 510)

class UI:
    def __init__(self):
        self.image = load_image('resource/ui.png')


    def draw(self):
        self.image.draw(530, 160)



class Player:
    def __init__(self):
        self.x, self.y = 0,400
        self.direction = 1
        self.frame = 0
        self.image = load_image('resource/player/player_move.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 100

    def update(self):
        global x
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if move == True:
            if dir == -1:
                self.direction = -1
                self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time
                x = self.x
            elif dir == 1:
                self.direction = 1
                self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time
                x = self.x
        if self.x > 800:
            self.x = 800
        elif self.x < 0:
            self.x = 0

        if self.x == 800:
            game_framework.change_state(game_clear)
        if self.stamina <= 0:
            game_framework.change_state(game_over)

    def draw(self):
        if move == True:
            if dir == 1:
                self.image.clip_draw(int(self.frame)* 210, 0, 205, 120, self.x, self.y,307.5,180)
            elif dir == -1:
                self.image.clip_draw(int(self.frame)* 210, 120, 205, 120, self.x, self.y,307.5,180)
        elif move == False:
            if dir == 1:
                self.image.clip_draw(3, 0, 210, 120, self.x, self.y,307.5,180)
            elif dir == -1:
                self.image.clip_draw(3, 120, 210, 120, self.x, self.y,307.5,180)
        self.font.draw(90,260, f'{food}', (255, 255, 255))
        self.font.draw(800,260, f'{mana}', (255, 255, 255))
        self.font.draw(self.x-30,self.y+90, f'{self.stamina}', (255, 255, 255))
    def get_bb(self):
        return self.x-60, self.y-50,self.x+60,self.y+80
    def handle_collision(self, other, group):
        pass
    def set_collision(self, input):
        self.iscollision = input
class Mouse:
    def __init__(self):
        global x
        self.x, self.y = -x, 400
        self.state = 0  # 0 = walk / 1 = attack / 2 = die
        self.iscollision = 0  # 0 = 충돌x / 1 = 충돌
        self.frame = random.randint(0,6)
        self.image = load_image('resource/player/mouse.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 20
        self.time = 0.0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.iscollision == 0:
            self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
            if self.x > 1700 - x:
                self.x = 1700 - x

        elif self.iscollision == 1:
            self.time += 0.1
    def draw(self):
        if self.stamina < 0:
            game_world.remove_object(self)
        elif self.stamina > 0:
            if self.state == 0:
                self.image.clip_draw(int(self.frame) * 57, 0, 57, 51, self.x, self.y,100,120)
            self.font.draw(self.x-20,self.y+51, f'{self.stamina}', (255, 255, 255))

    def get_bb(self):
        return self.x-30, self.y-50, self.x+30, self.y+50

    def handle_collision(self, other, group):
        if group == 'enemy:mouse':
            self.iscollision = 1
            if self.time >= 3.0:
                self.time = 0.0
                other.stamina -= 10
                self.font.draw(self.x + 10, self.y + 94, f'{-30}', (255, 255, 255))

    def set_collision(self, input):
        self.iscollision = input


class Dragon:
    def __init__(self):
        global x
        self.x, self.y = -x,400
        self.iscollision = 0  # 0 = 충돌x / 1 = 충돌
        self.state = 0 #  0=walk/1=attack/2=die
        self.frame = 0
        self.image = load_image('resource/player/dragon.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 40
        self.time = 0.0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if self.iscollision == 0:
            self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
            if self.x > 1700 - x:
                self.x = 1700 - x
        elif self.iscollision == 1:
            self.time += 0.1
    def draw(self):
        if self.stamina < 0:
            game_world.remove_object(self)
        elif self.stamina >0:
            if self.state == 0:
                self.image.clip_draw(int(self.frame) * 170, 0, 170,170, self.x, self.y,200,200)
            self.font.draw(self.x,self.y+85, f'{self.stamina}', (255, 255, 255))

    def get_bb(self):
        return self.x-40, self.y-70,self.x+40,self.y+70

    def handle_collision(self, other, group):
        if group == 'enemy:dragon':
            self.iscollision = 1
            if self.time >= 4.0:
                self.time = 0.0
                other.stamina -= 20
                self.font.draw(self.x + 10, self.y + 94, f'{-30}', (255, 255, 255))
    def set_collision(self, input):
        self.iscollision = input

class Rhino:
    def __init__(self):
        global x
        self.x, self.y = -x, 400
        self.iscollision = 0  # 0 = 충돌x / 1 = 충돌
        self.state = 0 # 0 = walk / 1 = attack / 2 = die
        self.frame = 0
        self.image = load_image('resource/player/rhinoceros.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 80
        self.time = 0.0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.iscollision == 0:
            self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time/1.8
            if self.x > 1700 - x:
                self.x = 1700 - x
        elif self.iscollision == 1:
            self.time += 0.1

    def draw(self):
        if self.stamina < 0:
            game_world.remove_object(self)
        elif self.stamina > 0:
            if self.state == 0:
                self.image.clip_draw(int(self.frame) * 128, 0, 128,149, self.x, self.y,166.4,193.7)
            self.font.draw(self.x-10, self.y + 74, f'{self.stamina}', (255, 255, 255))

    def get_bb(self):
        return self.x-40, self.y-60,self.x+40,self.y+60
    def handle_collision(self, other, group):
        if group == 'enemy:rhino':
            self.iscollision = 1
            if self.time >= 6.0:
                self.time = 0.0
                other.stamina -= 30
                self.font.draw(self.x + 10, self.y + 94, f'{-30}', (255, 255, 255))

    def set_collision(self, input):
        self.iscollision = input

class Mace_1():
    def __init__(self):
        global x
        self.x, self.y = x, 450
        self.iscollision = 1
        self.frame = 0
        self.image = load_image('resource/mace/1/m01_1.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time / 0.3
        if self.x > 1700 - x:
            game_world.remove_object(self)

    def draw(self):
        if self.x < 1700 - x:
            self.image.clip_draw(int(self.frame) * 65, 0, 65, 57, self.x, self.y, 131.6, 114)

    def get_bb(self):
        return self.x-40, self.y-60,self.x+40,self.y+60

    def handle_collision(self, other, group):
        if group == 'enemy:mace1':
            self.iscollision = 1

    def set_collision(self, input):
        self.iscollision = input
class Mace_2():
    def __init__(self):
        global x
        self.x, self.y = x, 450
        self.frame = 0
        self.image = load_image('resource/mace/2/m02.png')
        self.time = 0.0

    def update(self):
        self.time += 0.1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if self.x > 1060:
            self.x = 1060

    def draw(self):
        if self.time < 6:
            self.image.clip_draw(int(self.frame) * 161, 0, 161, 71, self.x+230, self.y-100, 330,228)

    def get_bb(self):
        return self.x-40, self.y-60, self.x+40, self.y+60

    def handle_collision(self, other, group):
        if group == 'mouses:mace_2':
            if other.stamina < 20:
                other.stamina += 20
        elif group == 'rhinos:mace_2':
            if other.stamina < 80:
                other.stamina += 40
        elif group == 'dragons:mace_2':
            if other.stamina < 40:
                other.stamina += 30


    def set_collision(self, input):
        self.iscollision = input
class Mace_3():
    def __init__(self):
        global x
        self.x, self.y = x, 450
        self.frame = 0
        self.image = load_image('resource/mace/3/m09.png')
        self.time = 0.0

    def update(self):
        self.time += 0.1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if self.x > 1060:
            self.x = 1060

    def draw(self):
        if self.time < 6:
            self.image.clip_draw(int(self.frame) * 91, 0, 91, 86, self.x-10, self.y + 50, 182, 172)

    def handle_collision(self, other, group):
        if group == 'player:mace3':
            print('충돌입니다')

class enemy():
    def __init__(self):
        self.x, self.y = random.randint(1500, 1700), 400
        self.state = 0  # 충돌 = 0 , 충돌 아닌 상황 = 1
        self.iscollision = 0
        self.frame = 0
        self.image = load_image('resource/monster/mummymove.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 50
        self.time = 0.0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.iscollision == 0:
            self.x += -1 * RUN_SPEED_PPS * game_framework.frame_time / 1.8
        elif self.iscollision == 1:
            self.time += 0.1
    def draw(self):
        self.image.clip_draw(int(self.frame) * 53, 0, 53, 71, self.x, self.y, 106, 142)
        if self.stamina <= 0:
            game_world.remove_object(self)
        elif self.stamina > 0:
            self.font.draw(self.x - 10, self.y + 74, f'{self.stamina}', (255, 255, 255))

    def get_bb(self):
        return self.x - 40, self.y - 60, self.x + 40, self.y + 60

    def handle_collision(self, other, group):
        if group == 'enemy:mouse' or group == 'enemy:dragon' or group == 'enemy:rhino':
            self.iscollision = 1
            if self.time >= 6.0:
                self.time = 0.0
                other.stamina -= 5
                self.font.draw(self.x + 10, self.y + 94, f'{-30}', (255, 255, 255))
        elif group == 'enemy:mace_1':
            self.stamina -=1
        elif group == 'enemy:player':
            self.iscollision = 1
            if self.time >= 6.0:
                self.time = 0.0
                other.stamina -= 5
                self.font.draw(self.x + 10, self.y + 94, f'{-30}', (255, 255, 255))

    def set_collision(self, input):
        self.iscollision = input

def handle_events():
    global running, dir, move, food, mana
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_a:
                    move = True
                    dir = -1
                case pico2d.SDLK_d:
                    move = True
                    dir = 1
                case pico2d.SDLK_KP_1:
                    if food >=1:
                        add_mouse()
                        food =food-10
                case pico2d.SDLK_KP_2:
                    if food >=20:
                        add_dragon()
                        food =food-20
                case pico2d.SDLK_KP_3:
                    if food >=30:
                        add_rhinos()
                        food =food-30
                case pico2d.SDLK_j:
                    if mana >= 9:
                        attack_1()
                        mana = mana-9
                case pico2d.SDLK_k:
                    if mana >= 30:
                        attack_2()
                        mana = mana-30
                case pico2d.SDLK_l:
                    if mana >= 50:
                        attack_3()
                        mana = mana-50
                        food = 40
                case pico2d.SDLK_ESCAPE:
                    game_framework.push_state(pause_state)
        elif event.type == SDL_KEYUP:
            move = False

player = None
background =None

mouses = []
dragons = []
rhinos = []

maces_1 = []
maces_2 = []
maces_3 = []

enemies = []

food = 40
mana = 100

ui =None
move = False
running = True
dir = 0
x = 0
bgm=None

p_time =0.0

def draw_world():
    global background, ui
    background.draw()
    ui.draw()

    for game_object in game_world.all_objects():
        game_object.draw()

def enter():
    global player, running, background, ui, p_time, enemies, bgm
    p_time = 0.0
    ui = UI()
    player = Player()
    background = BG()
    # game_world.add_object(background, 0)
    game_world.add_object(player, 0)
    enemies = [enemy() for i in range(5)]
    game_world.add_objects(enemies, 0)
    running = True
    game_world.add_collision_pairs(enemies, player, 'enemy:player')
    bgm = load_music('resource/bgm.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
def pause():
    pass

def exit():
    global bgm
    bgm.stop
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    global p_time
    p_time = p_time + 0.1

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)
        else:
            a.set_collision(False)
            b.set_collision(False)
    if p_time == 30.0:
        enemies = [enemy() for i in range(5)]
        game_world.add_objects(enemies, 0)


def draw():
    global p_time, food, mana
    clear_canvas()
    draw_world()
    if p_time > 3.0:
        if mana < 100:
            mana = mana + 1
        if food < 40:
            food = food + 1
        p_time = 0.0
    update_canvas()


def resume():
    pass

def add_mouse():
    mouses.append(Mouse())
    for game_object in mouses:
        game_world.add_object(game_object, 0)
        game_world.add_collision_pairs(enemies, game_object, 'enemy:mouse')

def add_dragon():
    dragons.append(Dragon())
    for game_object in dragons:
        game_world.add_object(game_object, 0)
        game_world.add_collision_pairs(enemies, game_object, 'enemy:dragon')

def add_rhinos():
    rhinos.append(Rhino())
    for game_object in rhinos:
        game_world.add_object(game_object, 0)
        game_world.add_collision_pairs(enemies, game_object, 'enemy:rhino')

def attack_1():
    maces_1.append(Mace_1())
    for game_object in maces_1:
        game_world.add_object(game_object, 0)
        game_world.add_collision_pairs(enemies, game_object, 'enemy:mace_1')

def attack_2():
    maces_2.append(Mace_2())
    for game_object in maces_2:
        game_world.add_object(game_object, 0)
        game_world.add_collision_pairs(mouses, game_object, 'mouses:mace_2')
        game_world.add_collision_pairs(rhinos, game_object, 'rhinos:mace_2')
        game_world.add_collision_pairs(dragons, game_object, 'dragons:mace_2')

def attack_3():
    maces_3.append(Mace_3())
    for game_object in maces_3:
        game_world.add_object(game_object, 0)

def collide(a,b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True
