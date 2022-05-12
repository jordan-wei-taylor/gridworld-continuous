from continuous_gridworld.env     import BaseEnv
                         
class FourRooms(BaseEnv):

    def __init__(self, variant = None, agent_loc = None, special_states = [], initial_states = None, cost_func = None, terminal_func = None):
        from continuous_gridworld.strings import four_rooms_string

        super().__init__(string         = four_rooms_string(variant),
                         agent_loc      = agent_loc,
                         special_states = special_states,
                         initial_states = initial_states,
                         cost_func      = cost_func,
                         terminal_func  = terminal_func)
