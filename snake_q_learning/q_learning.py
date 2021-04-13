import numpy as np
import random
from pynput.keyboard import Key, Controller  # to simulate keypress
import pickle


direction_idx = {
    'left': 0,
    'right': 1,
    'up': 2,
    'down': 3
}


def init_q_table(grid_size, file_name=None, q_value_init_range=(-1, 1), num_actions=4):

    if file_name is None:
        # create a dictionary that will serve as a q table for fast lookup
        # the keys are the states and the values will correspond to each action
        # q-table keys: (food-head distance), direction
        q_table = {}

        print('Initializing q-table... ', end="", flush=True)
        max_x_diff = grid_size[0]
        max_y_diff = grid_size[1]
        for x in range(-max_x_diff + 1, max_x_diff):
            for y in range(-max_y_diff + 1, max_y_diff):
                for direction in range(num_actions):
                    q_table[(x, y, direction)] = np.random.uniform(
                        q_value_init_range[0], q_value_init_range[1], size=num_actions)
        print('Initialized q-table!')
    else:
        with open(file_name, 'rb') as f:
            q_table = pickle.load(f)
        print(f'Loaded existing q-table ({file_name})!')
    return q_table


def calc_new_state(snake, food_block):
    head_block_pos = np.array(snake.body_dict[0])
    food_block_pos = np.array(food_block.position)
    diff = tuple(head_block_pos - food_block_pos)
    if diff[0] == 0 and diff[1] == 0:
        on_food = True
    else:
        on_food = False

    return (diff[0], diff[1], direction_idx[snake.direction]), on_food


def select_action(q_table, state, epsilon, num_actions=4):
    # if randomly generated value is larger than epsilon, than use q-table
    if epsilon > np.random.uniform(0, 1):
        action = np.argmax(q_table[state])
    else:
        action = random.randint(0, num_actions-1)
    return action


def press_key(keyboard, key_idx):
    keys = {0: Key.left,
            1: Key.right,
            2: Key.up,
            3: Key.down}

    keyboard.press(keys[key_idx])
    keyboard.release(keys[key_idx])



def calc_reward(on_food, move_penalty, crash_penalty, food_reward, crashed):
    if crashed:
        reward = -crash_penalty

    if on_food:
        reward = food_reward
    else:
        reward = -move_penalty

    return reward


def update_q_table(q_table, state, new_state, action, reward, learning_rate, discount):
    max_future_q = np.max(q_table[new_state])
    current_q = q_table[state][action]
    new_q = (1 - learning_rate) * current_q + learning_rate * \
        (reward + discount * max_future_q)  # formula to update q-values

    q_table[state][action] = new_q
    # print(f'updated state = {state}')
