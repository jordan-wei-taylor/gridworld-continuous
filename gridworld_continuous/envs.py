from gridworld_continuous.env     import BaseEnv
                         
class FourRooms(BaseEnv):

    def __init__(self, variant = None, agent_loc = None, events = [], initial_states = None, cost_func = None, terminal_func = None):
        from gridworld_continuous.strings import four_rooms_string

        super().__init__(string         = four_rooms_string(variant),
                         agent_loc      = agent_loc,
                         events         = events,
                         initial_states = initial_states,
                         cost_func      = cost_func,
                         terminal_func  = terminal_func)
