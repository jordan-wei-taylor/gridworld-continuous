from continuous_gridworld.env     import GridWorld, Grid
from continuous_gridworld.patches import RectanglePatch

class FourRoomsSym(GridWorld):

    def __init__(self, terminal_states, initial_states = None):
        width  = 0.4
        gap    = width * 3 / 2
        length = (10 - 2 * width - 2 * gap) / 4

        border = [[(0, 0), 10, width],
                  [(0, 0), width, 10],
                  [(10 - width, 0), width, 10],
                  [(0, 10 - width), 10, width]]

        left   = [[(width, 5 - width / 2), length, width],
                  [(width + length + gap, 5 - width / 2), length, width]]
        
        right  = [[(5 + width / 2, 5 - width / 2), length, width],
                  [(5 + width / 2 + length + gap, 5 - width / 2), length, width]]


        bottom = [[(5 - width / 2, width), width, length],
                  [(5 - width / 2, width + length + gap), width, length]]

        top    = [[(5 - width / 2, 5), width, length],
                  [(5 - width / 2, 5 + length + gap), width, length]]

        walls  = border + left + right + bottom + top

        for reward, state, kwargs in terminal_states:
            assert isinstance(reward, (int, float))
            assert isinstance(state , (list, tuple)) and len(state) == 2
            assert isinstance(kwargs, dict)

        super().__init__(grid            = Grid(10, 10, walls),
                         agent           = RectanglePatch((2.75, 7.25), width, width, fc = 'g', ec = 'k'),
                         terminal_states = [(reward, RectanglePatch(loc, width, width, **kwargs)) for reward, loc, kwargs in terminal_states], 
                         initial_states  = initial_states)

class FourRooms(GridWorld):

    def __init__(self, terminal_states, initial_states = None):
        width  = 0.4
        gap    = width * 3 / 2
        length = (10 - 2 * width - 2 * gap) / 4

        border = [[(0, 0), 10, width],
                  [(0, 0), width, 10],
                  [(10 - width, 0), width, 10],
                  [(0, 10 - width), 10, width]]

        left   = [[(width, 4.5 - width / 2), length, width],
                  [(width + length + gap, 4.5 - width / 2), length, width]]
        
        right  = [[(5 + width / 2, 5.5 - width / 2), length, width],
                  [(5 + width / 2 + length + gap, 5.5 - width / 2), length, width]]


        bottom = [[(5 - width / 2, width), width, length],
                  [(5 - width / 2, width + length + gap), width, length]]

        top    = [[(5 - width / 2, 5), width, length],
                  [(5 - width / 2, 5 + length + gap), width, length]]

        walls  = border + left + right + bottom + top

        assert isinstance(terminal_states, (list, tuple))

        for reward, state, kwargs in terminal_states:
            assert isinstance(reward, (int, float))
            assert isinstance(state , (list, tuple)) and len(state) == 2
            assert isinstance(kwargs, dict)

        super().__init__(grid            = Grid(10, 10, walls),
                         agent           = RectanglePatch((2.75, 7.25), width, width, fc = 'g', ec = 'k'),
                         terminal_states = [(reward, RectanglePatch(loc, width, width, **kwargs)) for reward, loc, kwargs in terminal_states], 
                         initial_states  = initial_states)