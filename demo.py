from   continuous_gridworld         import Grid, GridWorld
from   continuous_gridworld.patches import RectanglePatch

from   matplotlib                   import pyplot as plt, animation

import numpy as np

plt.switch_backend('agg')

def animate(gridworld, locs, interval = 50):

    fig, ax, objects, patches = gridworld.render()

    offset = objects[-1].xy - objects[-1].loc

    count  = 0
    def func(i):
        nonlocal count
        patches[-1].set_xy(locs[i] + offset)
        fig.canvas.draw()
        count += (locs[i] == locs[i - 1]).all()
        if count:
            ax.set_title(f'hit wall {count} times')

    ax.set_xticks([])
    ax.set_yticks([])

    plt.close()

    anim = animation.FuncAnimation(fig, func, len(locs), interval = interval)

    return anim

width = 0.4

walls = [[(0, 0), 10, width],
         [(0, 0), width, 10],
         [(10 - width, 0), width, 10],
         [(0, 10 - width), 10, width],
         [(0, 5 - width / 2), 2.5, width],
         [(3.5, 5 - width / 2), 3, width],
         [(7.5, 5 - width / 2), 2.5, width],
         [(5 - width / 2, 0), width, 2.5],
         [(5 - width / 2, 3.5), width, 3],
         [(5 - width / 2, 7.5), width, 2.5]]

agent_patch = RectanglePatch((5, 2), width, width, fc = 'g', ec = 'k')
gold_patch  = RectanglePatch((7, 7), width, width, fc = 'y', ec = 'k')

grid        = Grid(10, 10, walls)
gridworld   = GridWorld(grid, agent_patch, [[10, gold_patch]])

np.random.seed(12)

locs = [gridworld.reset()]

while not any(gridworld.agent(locs[-1]).contains(gridworld.terminal_states[0][1])):
    delta = np.clip(gridworld.terminal_states[0][1].loc - locs[-1], -0.05, 0.05)
    locs.append(locs[-1] + delta)
    
anim = animate(gridworld, locs)

anim.save('four-rooms-get-gold.gif')

np.random.seed(12)

locs  = [gridworld.reset()]
count = 0
while count < 20:
    reward, state, terminal = gridworld.step((-0.05, 0))
    count += (state == locs[-1]).all()
    locs.append(state)
    
anim = animate(gridworld, locs, 100)

anim.save('four-rooms-to-wall.gif')