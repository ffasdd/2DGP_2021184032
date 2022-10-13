from pico2d import *
import game_framework
import game_manual_state
import stage_select_state

running = True
# image = None

def enter():
    global image
    image = load_image('resource/paladog_game_manual.png')
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
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(stage_select_state)