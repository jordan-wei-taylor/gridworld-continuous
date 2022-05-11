from   continuous_gridworld.base    import Base
from   continuous_gridworld.patches import RectanglePatch

from   matplotlib import pyplot as plt, patches

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
