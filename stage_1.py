from pico2d import *
import game_framework

running = True

class BG:
    def __init__(self):
        self.image = load_image('resource/background.png')

    def draw(self):
        self.image.draw(530, 510)
class UI:
    def __init__(self):
        self.image = load_image('resource/ui.png')

    def draw(self):
        self.image.draw(530, 160)
class Player:
    def __init__(self):
        self.x, self.y = 100, 150
        self.direction=1
        self.frame = 0
        self.image = load_image('resource/player/player_move.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        delay(0.05)
        if move == True:
            if dir == -1:
                self.direction = -1
                self.x += self.direction*3
            elif dir == 1:
                self.direction = 1
                self.x += self.direction*3
        if self.x > 800:
            self.x=800
        elif self.x<0:
            self.x = 0

    def draw(self):
        if move == True:
            if dir == 1:
                self.image.clip_draw(self.frame * 128, 0, 128, 120, self.x, self.y,192,180)
            elif dir == -1:
                self.image.clip_draw(self.frame * 128, 120, 128, 120, self.x, self.y,192,180)
        elif move == False:
            if dir == 1:
                self.image.clip_draw(0, 0, 128, 120, self.x, self.y,192,180)
            elif dir == -1:
                self.image.clip_draw(0, 120, 128, 120, self.x, self.y,192,180)
def handle_events():
    global running, dir, move
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            move =True
            match event.key:
                case pico2d.SDLK_LEFT:
                    dir = -1
                case pico2d.SDLK_RIGHT:
                    dir = 1
                case pico2d.SDLK_ESCAPE:
                    game_framework.quit()
        elif event.type == SDL_KEYUP:
            move =False

player = None
background =None
ui =None
move = False
running = True
dir = 0

def draw_world():
    background.draw()
    ui.draw()
    player.draw()

def enter():
    global player, running, background, ui
    running = True
    ui= UI()
    player = Player()
    background =BG()
    pass

def exit():
    global player, background
    del background
    del player
    pass

def update():
    player.update()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

