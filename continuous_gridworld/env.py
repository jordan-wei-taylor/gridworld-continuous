from   continuous_gridworld.base    import Base
from   continuous_gridworld.patches import RectanglePatch

from   matplotlib                   import pyplot as plt

import numpy as np


class Grid(Base):

    def __init__(self, x, y, walls, fc = 'k', lw = 0.01):
        super().__init__(locals())

    def _gather_walls(self):
        walls = []
        for (xy, dx, dy) in self.walls:
            wall = RectanglePatch((xy[0] + dx / 2, xy[1] + dy / 2), dx, dy, lw = self.lw, fc = self.fc)
            walls.append(wall)
        return walls
        
    def _render_skeleton(self, figsize, ax = None):
        
        if ax is None:
            (fig, ax) = (self.fig, self.ax) = plt.subplots(figsize = figsize)
        else:
            self.fig, self.ax = None, ax
            

        ax.set_xlim((0, self.x))
        ax.set_ylim((0, self.y))

        ax.set_aspect('equal')

        for wall in self._gather_walls():
            ax.add_patch(wall.patch)

    def _gather_patches(self, objects):
        ret = []
        for obj in objects:
            if obj.loc is not None:
                ret.append(obj.patch)
        return ret

    def render(self, *objects, ax = None, figsize = None):
        self._render_skeleton(figsize, ax)
        patches = self._gather_patches(objects)
        for patch in patches:
            self.ax.add_patch(patch)
        return self. fig, self.ax, objects, patches

class GridWorld(Base):

    def __init__(self, grid, agent, special_states, initial_states = None, cost_func = None, terminal_func = None):
        assert isinstance(grid, Grid)
        assert isinstance(special_states, (list, tuple))
        assert isinstance(initial_states, (list, tuple)) or initial_states is None

        if cost_func is None:
            cost_func = cost_sqdist

        if terminal_func is None:
            terminal_func = bool

        super().__init__(locals())
        self.walls = grid._gather_walls()

        if initial_states:
            for state in initial_states:
                if np.any(self._check_overlap(agent(state))):
                    raise Exception()
        
        self._special_states = self.special_states.copy()

        self.state    = agent.loc
        self.flags    = []
        self.terminal = False

    def _check_special(self):
        for i, (reward, state, flag) in enumerate(self._special_states):
            if any(state.contains(self.agent)):
                self.flags.append(flag)
                self.terminal = self.terminal_func(self.flags)
                del self._special_states[i]
                return reward, flag
        return 0, None

    def _check_overlap(self, patch):
        ret = []
        for wall in self.walls:
            if any(wall.contains(patch)):
                ret.append(wall)
        return ret
        
    def reset(self):
        self._special_states = self.special_states.copy()
        self.flags           = []
        self.terminal        = False
        if self.initial_states:
            self.state = self.agent.loc = self.initial_states[np.random.choice(len(self.initial_states))]
            return self.state
        else:
            self.state = np.random.uniform((0, 0), (self.grid.x, self.grid.y))
            while self._check_overlap(self.agent(self.state)) or np.any([state.contains(self.agent(self.state)) for reward, state, flag in self._special_states]):
                self.state = np.random.uniform((0, 0), (self.grid.x, self.grid.y))
            return self.state

    def _correct(self, action):
        new        = self.state + action
        check      = self._check_overlap(self.agent(new))
        n          = len(check)

        correction = None

        if n:
            for modifier in [[1,0],[0,1],[0,0]]:
                new   = self.state + action * modifier
                check = self._check_overlap(self.agent(new))
                n     = len(check)

                if n == 0:
                    break

            correction = (new - self.state - action)

        return new, correction
    
    def step(self, action):
        action = np.array(action)
        assert action.ndim == 1 and len(action) == 2
        new, correction = self._correct(action)
        move            = self.cost_func(self.state, action, new)
        reward, flag    = self._check_special()
        self.state      = new
        info            = dict(correction = correction, flag = flag)
        return reward - move, self.state, self.terminal, info
        
    def render(self, ax = None):
        return self.grid.render(*[special[1] for special in self._special_states], self.agent, ax = ax)

class BaseEnv(GridWorld):

    def __init__(self, string, agent_loc = None, special_states = [], initial_states = None, cost_func = None, terminal_func = None, size = 0.5):

        walls, H, V = string2walls(string)

        assert agent_loc is None or (isinstance(agent_loc, (list, tuple)) and len(agent_loc) == 2)

        for reward, state, flag, kwargs in special_states:
            assert isinstance(reward, (int, float))
            assert isinstance(state , (list, tuple)) and len(state) == 2
            assert isinstance(flag  , str)
            assert isinstance(kwargs, dict)

        special_states = [(reward, RectanglePatch(loc, size, size, **kwargs), flag) for reward, loc, flag, kwargs in special_states]

        super().__init__(grid           = Grid(H, V, walls),
                         agent          = RectanglePatch(agent_loc, size, size, fc = 'g', ec = 'k'),
                         special_states = special_states, 
                         initial_states = initial_states,
                         cost_func      = cost_func,
                         terminal_func  = terminal_func)

def cost_sqdist(old, action, new):
    return np.square(new - old).sum() + (new == old).all()

def string2arrays(string):

    string    = np.array(list(map(list, string.strip().split('\n')))[::-1])

    binary    = (string == '#').astype(int)

    n, m      = binary.shape

    zeros     = np.zeros_like(binary)

    left      = zeros.copy()
    left[:,0] = 1

    bottom    = zeros.copy()
    bottom[0] = 1

    right     = zeros.copy()
    right[:,-1] = 1

    top       = zeros.copy()
    top[-1]   = 1

    arrays    = [left, bottom, right, top]

    binary   -= sum(arrays)

    while (binary > 0).any():
        best = 0
        line = []
        temp = []
        for i in range(n):
            for j in range(m):
                if binary[i,j] > 0:
                    temp.clear()
                    for i_ in range(i, n):
                        if binary[i_,j] > 0:
                            temp.append((i_,j))
                        else:
                            break
                    l = len(temp)
                    if l > best:
                        best = l
                        line = temp.copy()

                    temp.clear()
                    for j_ in range(j, m):
                        if binary[i,j_] > 0:
                            temp.append((i,j_))
                        else:
                            break
                    
                    l = len(temp)
                    if l > best:
                        best = l
                        line = temp.copy()
        
        part = zeros.copy()

        part[tuple(zip(*line))] = 1

        arrays.append(part)

        binary -= part

    return arrays

def string2walls(string, unit = 1):
    arrays = string2arrays(string)
    H, V   = np.array(arrays[0].shape)[::-1] * unit
    walls  = []

    left, bottom, right, top = arrays[:4]

    X, Y   = np.where(left)
    dx, dy = X.ptp() * (unit + 1), Y.ptp() * (unit + 1)

    walls.append(((0, 0), unit, dx * unit + 2 * unit))

    X, Y   = np.where(bottom)
    dx, dy = X.ptp() * (unit + 1), Y.ptp() * (unit + 1)

    walls.append(((0, 0), dy * unit + 2 * unit, unit))

    X, Y   = np.where(right)
    dx, dy = X.ptp() * (unit + 1), Y.ptp() * (unit + 1)

    walls.append(((H - unit, 0), unit, dx * unit + 2 * unit))

    X, Y   = np.where(top)
    dx, dy = X.ptp() * (unit + 1), Y.ptp() * (unit + 1)

    walls.append(((0, V - unit), dy * unit + 2 * unit, unit))

    for array in arrays[4:]:
        Y , X  = np.where(array)
        dy, dx = Y.ptp() * unit + unit, X.ptp() * unit + unit
        xy     = X.min() * unit, Y.min() * unit

        walls.append((xy, dx, dy))
        
    return walls, H, V
