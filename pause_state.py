from pico2d import *
import game_framework
import game_manual_state
import intro_state

running = True


def enter():
    global image
    image = load_image('resource\pngs\pause.png')
    pass

def exit():
    global image
    del image
    pass

def update():
   pass

def draw():
    clear_canvas()
    image.draw(530,400)
    update_canvas()


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.change_state(intro_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            game_framework.pop_state()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(intro_state)


def pause():
    pass

def resume():
    pass
