from matplotlib import pyplot as plt
import pygame
import os
import snake
import q_learning
import random
from pynput.keyboard import Key, Controller  # to simulate keypress

import copy
import json
import pickle

# following chunk allows plotting
import matplotlib
matplotlib.use("Qt5Agg")

import time
import sys

''' 
q-table state space: 
    - distance between food
'''

# q-learning parameters
EPISODES = 100000  # number of simulations to run
# number of maximum steps per simulation (so instance doesn't continue forever)
MAX_STEPS = 200
MOVE_PENALTY = 2
CRASH_PENALTY = 100
FOOD_REWARD = 30
epsilon = 0.5  # for random movement
EPISLON_DECAY = 1  # to decrease chance of random movement as num episodes increase
LEARNING_RATE = 0.1
DISCOUNT = 0.95
SHOW_EVERY = 100  # show progress after every n episodes


# global pygame variables
WINDOW_SIZE = 200
DISPLAY_WIDTH = WINDOW_SIZE  # should be multiples of block size
DISPLAY_HEIGHT = WINDOW_SIZE
BLOCK_SIZE = 20

infinite_loop = False
show_grid = False
save_q_tables = False

q_table_location = None


def main_loop():

    num_steps = 0
    # round instantiation position to nearest block size
    x = round((DISPLAY_WIDTH * 0.5)/BLOCK_SIZE)*BLOCK_SIZE
    y = round((DISPLAY_HEIGHT * 0.5)/BLOCK_SIZE)*BLOCK_SIZE

    play = True

    snake_velocity = BLOCK_SIZE
    snake_is_stopped = False

    # instantiate snake head and food block objects
    s = snake.Snake(x, y, max_x=DISPLAY_WIDTH, max_y=DISPLAY_HEIGHT,
                    block_size=BLOCK_SIZE, velocity=snake_velocity)
    food_block = snake.FoodBlock(
        snake=s, x_max=DISPLAY_WIDTH, y_max=DISPLAY_HEIGHT)

    score = 0
    ep_reward = 0
    while play and num_steps <= MAX_STEPS:
        # snake.draw_grid(gameDisplay, BLOCK_SIZE, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        # snake.draw_score(score, gameDisplay)  # display the score

        state, _ = q_learning.calc_new_state(s, food_block)
        action = q_learning.select_action(q_table, state, epsilon)
        q_learning.press_key(keyboard, action)

        for event in pygame.event.get():  # retrieve all events (inputs)
            if event.type == pygame.QUIT:  # if click on the X of window to quit
                play = False  # break from main loop

            if event.type == pygame.KEYDOWN:  # change direction of snake based on keypress
                if event.key == pygame.K_LEFT and s.direction != 'right':
                    s.action(0)
                elif event.key == pygame.K_RIGHT and s.direction != 'left':
                    s.action(1)
                elif event.key == pygame.K_UP and s.direction != 'down':
                    s.action(2)
                elif event.key == pygame.K_DOWN and s.direction != 'up':
                    s.action(3)

        s.move()  # move snake
        new_state, on_food = q_learning.calc_new_state(s, food_block)
        s, food_block, score, crashed = snake.process_game_logic(
            s, food_block, score)  # check if scored point/game over

        reward = q_learning.calc_reward(
            on_food, MOVE_PENALTY, CRASH_PENALTY, FOOD_REWARD, crashed)  # calculate reward

        q_learning.update_q_table(
            q_table, state, new_state, action, reward, LEARNING_RATE, DISCOUNT)

        # draw background, snake, and food
        snake.draw_window(gameDisplay, s, food_block, score, show_grid)

        if crashed and infinite_loop:  # quit current session and reruns another instance
            main_loop()
            play = False
        elif crashed and not infinite_loop:  # exit out of session
            play = False

        clock.tick(fps)  # input is the frames per second
        num_steps += 1
        ep_reward += reward

    if print_score:
        print(f'Score: {score}, Crash: {crashed}, Epsilon: {epsilon}')

    return ep_reward


q_table = q_learning.init_q_table(grid_size=(
    DISPLAY_WIDTH, DISPLAY_HEIGHT), file_name=q_table_location)
print(f'Q table length {len(q_table)}')

initial_q_table = copy.deepcopy(q_table)
keyboard = Controller()

ep_reward_hist = []

for episode in range(1, EPISODES + 1):
    if episode % SHOW_EVERY == 0:
        fps = 20
        print_score = True

        if 'SDL_VIDEODRIVER' in os.environ:  # show simulation
            del os.environ['SDL_VIDEODRIVER']

        if save_q_tables:
            path = f'q_tables/{episode}.pkl'
            with open(path, 'wb') as f:
                pickle.dump(q_table, f)
            # print(f'Saved {path}')

        print(f'Episode: {episode}', end=' ', flush=True)

    else:
        fps = 1000000
        print_score = False
        # os.environ["SDL_VIDEODRIVER"] = "dummy"  # run simulations headlessly
        # print(f'Episode: {episode}', end=' ', flush=True)

    pygame.init()

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    pygame.display.set_caption('Lil Noodle')
    clock = pygame.time.Clock()

    t = time.time()
    ep_reward = main_loop()
    
    # pygame.quit()

    ep_reward_hist.append(ep_reward)
    

    epsilon *= EPISLON_DECAY  # update epsilon to reduce chance of random action

    
    # save episode reward history
    ep_reward_hist_path = 'ep_reward_hist.pkl'
    # if os.path.exists(ep_reward_hist_path):
    #     os.remove(ep_reward_hist_path)
    #     time.sleep(0.05)
    with open(file=ep_reward_hist_path, mode='wb') as f:
        pickle.dump(ep_reward_hist, f)

    


plt.plot(ep_reward_hist)
plt.show()


# inspect q table after
initial_q_table = {str(key): list(value)
                   for key, value in initial_q_table.items()}
q_table = {str(key): list(value) for key, value in initial_q_table.items()}
with open('initial_q_table.txt', 'w') as outfile:
    json.dump(initial_q_table, outfile, indent=4)
with open('end_q_table.txt', 'w') as outfile:
    json.dump(q_table, outfile, indent=4)


quit()
