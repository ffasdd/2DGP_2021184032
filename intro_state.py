from pico2d import *
import game_framework
import game_manual_state

running = True


def enter():
    global image
    image = load_image('resource\intro_image.png')
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
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                game_framework.change_state(game_manual_state)

def pause():
    pass
def resume():
    pass
