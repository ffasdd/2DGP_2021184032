import pico2d
import intro_state

pico2d.open_canvas(1070,800)

intro_state.enter()

while intro_state.running:
    intro_state.handle_events()
    intro_state.update()
    intro_state.draw()

intro_state.exit()

pico2d.clear_canvas()