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
        
    def _render_skeleton(self, figsize):
        (fig, ax) = (self.fig, self.ax) = plt.subplots(figsize = figsize)

        ax.set_xlim((0, self.x))
        ax.set_ylim((0, self.y))

        ax.set_aspect('equal')

        for wall in self._gather_walls():
            ax.add_patch(wall.patch)

    def _gather_patches(self, objects):
        ret = []
        for obj in objects:
            ret.append(obj.patch)
        return ret

    def render(self, *objects, figsize = None):
        self._render_skeleton(figsize)
        patches = self._gather_patches(objects)
        for patch in patches:
            self.ax.add_patch(patch)
        return self. fig, self.ax, objects, patches

class GridWorld(Base):

    def __init__(self, grid, agent, terminal_states, initial_states = None):
        assert isinstance(grid, Grid)
        assert isinstance(terminal_states, (list, tuple))
        assert isinstance(initial_states, (list, tuple)) or initial_states is None
        super().__init__(locals())
        self.walls = grid._gather_walls()

        if initial_states:
            for state in initial_states:
                if np.any(self._check_overlap(agent(state))):
                    raise Exception()
        
        self.state = agent.loc
        
    def _check_terminal(self):
        for reward, state in self.terminal_states:
            if any(state.contains(self.agent)):
                self.terminal = True
                return reward
        return 0

    def _check_overlap(self, patch):
        ret = []
        for wall in self.walls:
            if any(wall.contains(patch)):
                ret.append(wall)
        return ret
        
    def reset(self):
        self.terminal = False
        if self.initial_states:
            self.state = loc = np.random.choice(self.initial_states)
            return loc
        else:
            loc = np.random.uniform((0, 0), (self.grid.x, self.grid.y))
            while self._check_overlap(self.agent(loc)) or np.any([state.contains(self.agent(loc)) for reward, state in self.terminal_states]):
                loc = np.random.uniform((0, 0), (self.grid.x, self.grid.y))
            self.state = loc
            return loc

    def _correct(self, action):
        new   = self.state + action
        check = self._check_overlap(self.agent(new))
        n     = len(check)

        if n:
            for modifier in [[1,0],[0,1],[0,0]]:
                new   = self.state + action * modifier
                check = self._check_overlap(self.agent(new))
                n     = len(check)

                if n == 0:
                    break

        return new
    
    def step(self, action):
        action = np.array(action)
        assert action.ndim == 1 and len(action) == 2
        new  = self._correct(action)
        move = np.square(new - self.state).sum() + (new == self.state).all()
        reward = self._check_terminal()
        self.state = new
        return reward - move, self.state, self.terminal
        
        
    def render(self):
        return self.grid.render(*[terminal[1] for terminal in self.terminal_states], self.agent)

class BaseEnv(GridWorld):

    def __init__(self, string, agent_loc, terminal_states = [], initial_states = None, size = 0.5):

        walls, H, V = string2walls(string)

        assert isinstance(agent_loc, (list, tuple)) and len(agent_loc) == 2

        for reward, state, kwargs in terminal_states:
            assert isinstance(reward, (int, float))
            assert isinstance(state , (list, tuple)) and len(state) == 2
            assert isinstance(kwargs, dict)

        super().__init__(grid            = Grid(H, V, walls),
                         agent           = RectanglePatch(agent_loc, size, size, fc = 'g', ec = 'k'),
                         terminal_states = [(reward, RectanglePatch(loc, size, size, **kwargs)) for reward, loc, kwargs in terminal_states], 
                         initial_states  = initial_states)

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
