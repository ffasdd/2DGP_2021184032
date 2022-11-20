import random
import time
import pico2d
from pico2d import *
import game_framework
import stage_select_state

running = True

PIXEL_PER_METER = (10.0 / 0.4) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class BG:
    def __init__(self):
        self.image = load_image('resource/background3.png')

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
        self.direction=1
        self.frame = 0
        self.image = load_image('resource/player/player_move.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 100

    def update(self):
        global x
        self.frame =  (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if move == True:
            if dir == -1:
                self.direction = -1
                self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time
                x =self.x
            elif dir == 1:
                self.direction = 1
                self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time
                x=self.x
        if self.x > 800:
            self.x=800
        elif self.x<0:
            self.x = 0

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

class Mouse:
    def __init__(self):
        global x
        self.x, self.y = -x,400
        self.state = 0 # 0=walk/1=attack/2=die
        self.frame = 0
        self.image = load_image('resource/player/mouse.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 20

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 1060:
            self.x = 1060
    def draw(self):
        if self.state == 0:
            self.image.clip_draw(int(self.frame) * 57, 0, 57,51, self.x, self.y,100,120)
        self.font.draw(self.x-20,self.y+51, f'{self.stamina}', (255, 255, 255))

class Dragon:
    def __init__(self):
        global x
        self.x, self.y = -x,400
        self.state = 0 #  0=walk/1=attack/2=die
        self.frame = 0
        self.image = load_image('resource/player/dragon.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 40

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 1060:
            self.x = 1060
    def draw(self):
        if self.state == 0:
            self.image.clip_draw(int(self.frame) * 170, 0, 170,170, self.x, self.y,200,200)
        self.font.draw(self.x,self.y+85, f'{self.stamina}', (255, 255, 255))


class Rhino:
    def __init__(self):
        global x
        self.x, self.y = -x,400
        self.state = 0 #  0=walk/1=attack/2=die
        self.frame = 0
        self.image = load_image('resource/player/rhinoceros.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.stamina = 80

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time/1.8
        if self.x > 1060:
            self.x = 1060
    def draw(self):
        if self.state == 0:
            self.image.clip_draw(int(self.frame) * 128, 0, 128,149, self.x, self.y,166.4,193.7)
        self.font.draw(self.x-10 , self.y + 74, f'{self.stamina}', (255, 255, 255))


class Mace_1():
    def __init__(self):
        global x
        self.x, self.y = x, 450
        self.frame = 0
        self.image = load_image('resource/mace/1/m01_1.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time/0.3
        if self.x > 1060:
            self.x = 1060

    def draw(self):
        self.image.clip_draw(int(self.frame) * 65, 0, 65, 57, self.x, self.y, 131.6, 114)

class Mace_2():
    def __init__(self):
        global x
        self.x, self.y = x, 450
        self.frame = 0
        self.image = load_image('resource/mace/2/m02.png')
        self.time = 0.0

    def update(self):
        self.time +=0.1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if self.x > 1060:
            self.x = 1060

    def draw(self):
        if self.time<6:
            self.image.clip_draw(int(self.frame) * 161, 0, 161, 71, self.x+230, self.y-100, 330,228)


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
            self.image.clip_draw(int(self.frame) * 91, 0, 91, 86, self.x-10, self.y + 50, 182,172)


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
                    exit()
                    game_framework.change_state(stage_select_state)
        elif event.type == SDL_KEYUP:
            move =False

player = None
background =None

mouses = []
dragons = []
rhinos = []

maces_1 =[]
maces_2=[]
maces_3=[]

food = 40
mana=100

ui =None
move = False
running = True
dir = 0
x =0

p_time =0.0
def draw_world():
    global font, background
    background.draw()
    ui.draw()
    player.draw()
    for mouse in mouses:
        mouse.draw()
    for dragon in dragons:
        dragon.draw()
    for rhino in rhinos:
        rhino.draw()

    for mace_1 in maces_1:
        mace_1.draw()
    for mace_2 in maces_2:
        mace_2.draw()
    for mace_3 in maces_3:
        mace_3.draw()


def enter():
    global player, running, background, ui,p_time
    p_time=0.0
    ui= UI()
    player = Player()
    background = BG()
    running = True

def exit():
    for mouse in mouses:
        del mouse
    for dragon in dragons:
        del dragon
    for rhino in rhinos:
        del rhino
    for mace_1 in maces_1:
        del mace_1
    for mace_2 in maces_2:
        del mace_2
    for mace_3 in maces_3:
        del mace_3


def update():
    global p_time,mana,food
    for mouse in mouses:
        mouse.update()
    for dragon in dragons:
        dragon.update()
    for rhino in rhinos:
        rhino.update()
    for mace_1 in maces_1:
        mace_1.update()
    for mace_2 in maces_2:
        mace_2.update()
    for mace_3 in maces_3:
        mace_3.update()
    player.update()
    p_time =p_time + 0.1

def draw():
    global p_time,food,mana
    clear_canvas()
    draw_world()
    if p_time > 3.0:
        if mana < 100:
            mana = mana + 1
        if food < 40:
            food = food + 1
        p_time = 0.0
    update_canvas()

def pause():
    pass

def resume():
    pass

def add_mouse():
    mouses.append(Mouse())
def add_dragon():
    dragons.append(Dragon())
def add_rhinos():
    rhinos.append(Rhino())

def attack_1():
    maces_1.append(Mace_1())

def attack_2():
    maces_2.append(Mace_2())

def attack_3():
    maces_3.append(Mace_3())
