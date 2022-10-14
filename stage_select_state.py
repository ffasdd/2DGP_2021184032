from pico2d import *
import game_framework
import intro_state
import game_manual_state
import stage_1
running = True

def enter():
    global image
    image = load_image('resource/stage_select/select_map_3.png')
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
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.change_state(game_manual_state)
                case pico2d.SDLK_1:
                    game_framework.change_state(stage_1)
                case pico2d.SDLK_2:
                    game_framework.change_state(intro_state)
                case pico2d.SDLK_3:
                    game_framework.change_state(intro_state)