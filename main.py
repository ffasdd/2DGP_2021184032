import pico2d
import game_framework
import intro_state
import stage_1

pico2d.open_canvas(1060,800)
game_framework.run(intro_state)
pico2d.clear_canvas()