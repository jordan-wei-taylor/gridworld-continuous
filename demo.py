from   continuous_gridworld.envs import FourRooms

from   matplotlib                import pyplot as plt, animation

import numpy as np

plt.switch_backend('agg')

def animate(gridworld, locs, infos = None, interval = 50, wall_count = False):
    """helper function to create demo animations"""
    
    gridworld._special_states = gridworld.special_states.copy()

    fig, ax, objects, patches = gridworld.render()

    # compute offset between bottom left corner and midpoint of rectangular agent patch
    offset = objects[-1].xy - objects[-1].loc

    count  = 0
    def func(i):
        nonlocal count
        patches[-1].set_xy(locs[i] + offset)
        fig.canvas.draw()
        count += (locs[i] == locs[i - 1]).any()
        if wall_count and count:
            ax.set_title(f'hit wall {count} times')
        if infos:
            ax.set_xlabel(infos[i])

    ax.set_xticks([])
    ax.set_yticks([])

    plt.close()

    anim = animation.FuncAnimation(fig, func, len(locs), interval = interval)

    return anim

reward = 10
loc    = (9.5, 9.5)
flag   = 'gold'
kwargs = dict(fc = 'y', ec = 'k')

states = [[reward, loc, flag, kwargs]]

env    = FourRooms(special_states = states)

env.render()

plt.savefig('four-rooms.png', dpi = 400)

np.random.seed(12)

locs     = [env.reset()]
terminal = env.terminal

while not terminal:
    action = np.clip(env.special_states[0][1].loc - locs[-1], -0.05, 0.05)
    reward, state, terminal, info = env.step(action)
    locs.append(state)
    
anim = animate(env, locs)

anim.save('four-rooms-get-gold.gif')

np.random.seed(12)

locs  = [env.reset()]
infos = [{}]
count = 0
while count < 20:
    reward, state, terminal, info = env.step((-0.05, 0.02))

    # check to see if new state is same as old state (i.e. move into wall)
    count += (state == locs[-1]).any()
    
    locs.append(state)
    infos.append(info)
    
anim = animate(env, locs, infos, interval = 100, wall_count = True)

anim.save('four-rooms-to-wall.gif')

def terminal_func(flags):
    return flags.count('gold') == 2

reward  = 10
locs    = [(2, 2), (9.5, 9.5)]
kwargs  = dict(fc = 'y', ec = 'k')
flag    = 'gold'

states  = [[reward, loc, flag, kwargs] for loc in locs]

initial = (8.9, 8.9)
env     = FourRooms(special_states = states, initial_states = [initial], terminal_func = terminal_func)

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

from continuous_gridworld.env import BaseEnv

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
