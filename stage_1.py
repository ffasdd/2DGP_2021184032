from pico2d import *
import game_framework

running = True

def enter():
    global image
    image = load_image('resource/background.png')
    pass

def exit():
    global image
    del image
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(530, 400)
    update_canvas()

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
