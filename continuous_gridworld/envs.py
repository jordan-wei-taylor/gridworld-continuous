from continuous_gridworld.env     import BaseEnv


class FourRooms(BaseEnv):

    def __init__(self, variant = None, terminal_states = [], initial_states = None):
        from continuous_gridworld.strings import four_rooms_string

        super().__init__(string          = four_rooms_string(variant),
                         agent_loc       = (1.5, 1.5),
                         terminal_states = terminal_states,
                         initial_states  = initial_states)
