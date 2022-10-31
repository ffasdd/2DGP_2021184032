import random

import pico2d
from pico2d import *
import game_framework
import stage_select_state


running = True

class BG:
    def __init__(self):
        global x
        self.image = load_image('resource/background3.png')

    def draw(self):
        global x
        self.image.draw(1600-(x*2), 510)

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

    def update(self):
        global x
        self.frame = (self.frame + 1) % 8
        if move == True:
            if dir == -1:
                self.direction = -1
                self.x += self.direction*5
                x=self.x
            elif dir == 1:
                self.direction = 1
                self.x += self.direction*5
                x=self.x
        if self.x > 1000:
            self.x=1000
        elif self.x<0:
            self.x = 0

    def draw(self):
        if move == True:
            if dir == 1:
                self.image.clip_draw(self.frame * 210, 0, 205, 120, self.x, self.y,307.5,180)
            elif dir == -1:
                self.image.clip_draw(self.frame * 210, 120, 205, 120, self.x, self.y,307.5,180)
        elif move == False:
            if dir == 1:
                self.image.clip_draw(3, 0, 210, 120, self.x, self.y,307.5,180)
            elif dir == -1:
                self.image.clip_draw(3, 120, 210, 120, self.x, self.y,307.5,180)


class Mouse:
    def __init__(self):
        self.x, self.y = random.randint(0,20),400
        self.state = 0 # 0=walk/1=attack/2=die
        self.frame = 0
        self.image = load_image('resource/player/mouse.png')

    def update(self):
        delay(0.05)
        self.frame = (self.frame + 1) % 6
        self.x += 5
        if self.x > 800:
            self.x = 800
    def draw(self):
        if self.state == 0:
            for x in range (0,mouse_num,1):
                self.image.clip_draw(self.frame * 57, 0, 57,51, self.x, self.y,100,120)


def handle_events():
    global running, dir, move,mouse_num
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
                    game_framework.push_state(mouse_adjust)
                case pico2d.SDLK_ESCAPE:
                    game_framework.change_state(stage_select_state)
        elif event.type == SDL_KEYUP:
            move =False

player = None
background =None
mouses = []
mouse_num = 0
num=0
ui =None
move = False
running = True
dir = 0
x =0

def draw_world():
    background.draw()
    ui.draw()
    player.draw()
    for mouse in mouses:
        mouse.draw()

def enter():
    global player, running, background, ui
    running = True
    ui= UI()
    player = Player()
    background =BG()
    mouses.append(Mouse())
    pass

def exit():
    global player, background
    for mouse in mouses:
        del mouse
    del background
    del player
    pass

def update():
    player.update()
    for mouse in mouses:
        mouse.update()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def add_mouse():
    mouses.append(Mouse())
