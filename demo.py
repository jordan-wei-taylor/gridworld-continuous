from   continuous_gridworld.envs   import FourRooms
from   continuous_gridworld.env    import BaseEnv
from   continuous_gridworld.events import SquareGold

from   matplotlib                  import pyplot as plt, animation

import numpy as np
import os

os.makedirs('demo', exist_ok = True)
os.chdir('demo')

plt.switch_backend('agg')

def animate(configs, interval = 50, wall_count = False):
    """helper function to create demo animations"""
    
    fig, ax = plt.subplots()

    _, ax, objects, patches = env.render(ax = ax)

    count  = 0
    def func(i):
        nonlocal count
        env.set_config(*configs[i])
        ax.clear()
        env.render(ax = ax)
        fig.canvas.draw()

        if i:
            ax.set_xlabel(configs[i][2])
            count += configs[i][2]['correction'] is not None
        
        if wall_count and count:
            ax.set_title(f'hit wall {count} times')

    ax.set_xticks([])
    ax.set_yticks([])

    plt.close()

    anim = animation.FuncAnimation(fig, func, len(configs), interval = interval)

    return anim

gold   = SquareGold(loc = (9.5, 9.5))

events = [gold]

env    = FourRooms(events = events)

env.render()

plt.savefig('four-rooms.png', dpi = 400)

np.random.seed(12)

state    = env.reset()
terminal = env.terminal
configs  = [env.get_config()]

while not terminal:
    action = np.clip(gold.loc - state, -0.05, 0.05)
    reward, state, terminal, info = env.step(action)
    configs.append(env.get_config())
    
anim = animate(configs)

anim.save('four-rooms-get-gold.gif')

np.random.seed(12)

state   = env.reset()
configs = [env.get_config()]

count = 0
while count < 20:
    reward, state, terminal, info = env.step((-0.05, 0.02))
    configs.append(env.get_config())
    count += info['correction'] is not None
    
anim = animate(configs, interval = 100)

anim.save('four-rooms-to-wall.gif')

def terminal_func(flags):
    return flags.count('gold') == 2

locs    = [(9.5, 9.5), (2, 2)]
events  = [SquareGold(loc = loc) for loc in locs]
initial = (8.9, 8.9)

env     = FourRooms(events = events, initial_states = [initial], terminal_func = terminal_func)

env.reset()

# two subplots for before and after gold collection
fig, ax = plt.subplots(1, 2, figsize = (12, 5))

# before gold collection
env.render(ax[0])

# step into gold location and confirm not a terminal state
action = (0.4, 0.4)
reward, state, terminal, info = env.step(action)

# after gold collection
env.render(ax[1])

sup = fig.suptitle(f'reward = {reward}\nstate = {state}\nterminal = {terminal}\ninfo = {info}', y = 1.15)

# remove ticks
for axes in ax:
    axes.set_xticks([])
    axes.set_yticks([])

ax[0].set_title(f'state = {initial}\naction = {action}')
ax[1].set_title(f'state = {tuple(env.state)}\n')

plt.savefig('four-rooms-first-gold.png', bbox_inches = 'tight', bbox_extra_artists = [sup])

custom = """
#############
#     #     #
#     #     #
#     #     #
#     #     #
#           #
#############
"""

BaseEnv(custom).render()

plt.savefig('custom.png', dpi = 400)

