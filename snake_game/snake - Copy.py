import pygame
import random
import copy
import time

colors = {'black': (0, 0, 0),
          'white': (255, 255, 255),
          'red':   (255, 0, 0),
          'green': (0, 255, 0),
          'blue':  (0, 0, 255),
          'grey':  (128, 128, 128)}


def draw_grid(surface, block_size, max_x, max_y, color=colors['grey']):
    for pos in range(0, max_x, block_size):  # draw horizontal grid lines
        pygame.draw.line(surface, color, (0, pos), (max_x, pos))
    for pos in range(0, max_y, block_size):  # draw vertical grid lines
        pygame.draw.line(surface, color, (pos, 0), (pos, max_y))

    pygame.display.update()


def text_objects(text, font):
    textSurface = font.render(text, True, colors['white'])
    return textSurface, textSurface.get_rect()  # allows us to position text


def draw_score(score, surface, x=0, y=0):  # display score
    score_text = pygame.font.SysFont('arial', 20)
    text_surf, text_rect = text_objects(f"Score: {score}", score_text)
    text_rect.top = x
    text_rect.left = y
    surface.blit(text_surf, text_rect)
    pygame.display.update()


def draw_body(snake, surface):
    # head_img = pygame.image.load('head.png') # load the snakehead
    block_size = snake.block_size
    for block in snake.body_dict:
        if block == 0:  # color head a different color
            pygame.draw.rect(surface, colors['grey'], [
                             snake.body_dict[block][0], snake.body_dict[block][1], block_size, block_size])
        else:
            pygame.draw.rect(surface, colors['white'], [
                             snake.body_dict[block][0], snake.body_dict[block][1], block_size, block_size])
    pygame.display.update()
    # gameDisplay.blit(head_img, (x, y))


def draw_food(food_block, surface, color=colors['green']):
    block_size = food_block.block_size
    pygame.draw.rect(surface, color, [
                     food_block.x, food_block.y, block_size, block_size])


def draw_window(surface, snake, food_block, score, show_grid):
    surface.fill(colors['black'])  # draw background
    if show_grid:
        draw_grid(surface, snake.block_size,
                  snake.max_x, snake.max_y)  # draw grids
    draw_score(score, surface)  # display the score

    draw_food(food_block, surface, colors['green'])
    draw_body(snake, surface)

    pygame.display.update()  # update the entire surface


def check_collision(snake, food_block):
    head_block_pos = snake.body_dict[0]
    body_pos = list(snake.body_dict.values())[1:]
    print(f'{head_block_pos}, {body_pos}')
    if head_block_pos in body_pos:
        print('Crash!')
        crashed = True
        return crashed
    else:
        crashed = False
        return crashed


def process_game_logic(snake, food_block, score):
    # first check if there is collision with head and body
    crashed = check_collision(snake, food_block)

    # if head block and food block in same location, then score a point
    head_block_pos = snake.body_dict[0]
    if sum([abs(a-b) for a, b in zip(head_block_pos, food_block.position)]) == 0:
        print('Nom!')
        score += 1
        food_block.reset_block()
        snake.add_body_block()

    return snake, food_block, score, crashed


class FoodBlock():
    '''block that player aims to move snake head to
        -spawns in random location that is not part of snake
    '''

    # takes a snake argument to avoid spawning in snake's location
    def __init__(self, snake, x_max, y_max):
        self.block_size = snake.block_size
        self.x_max = x_max
        self.y_max = y_max

        self.x_pixels_to_avoid = [loc[0] for loc in snake.body_dict.items()]
        self.y_pixels_to_avoid = [loc[1] for loc in snake.body_dict.items()]
        self.reset_block()

    def reset_block(self):  # resets food block to a new location
        self.x = random.choice([i for i in range(
            0, self.x_max, self.block_size) if i not in self.x_pixels_to_avoid])
        self.y = random.choice([i for i in range(
            0, self.y_max, self.block_size) if i not in self.y_pixels_to_avoid])
        self.position = [self.x, self.y]
        print(f'New food block spawned block in {self.x}, {self.y}!')


class Snake:
    '''snake that user controls
        - snake has a constant velocity
        - pressing a key changes the velocity
        - when 'head' of snake passes over 'food', 'food disappears and
          snake's body increases in length
        - game instance ends when snake 'head' runs into its 'body'
    '''

    def __init__(self, x, y, max_x, max_y, velocity=20, block_size=20, direction='up'):
        self.block_size = block_size
        self.velocity = velocity  # speed at which snake moves
        self.direction = direction  # direction of velocity
        self.max_x = max_x  # set bounds for which snake can traverse
        self.max_y = max_y

        # instantiate a list of the body blocks with a head block, where (x, y) is top left of block
        self.body_dict = {0: [x, y]}
        self.number_blocks = 1

    def add_body_block(self):
        # add another block temporarily offscreen for current frame
        self.body_dict[self.number_blocks] = [60, 60]
        self.number_blocks += 1

    def move(self):
        distance = self.velocity
        # create a copy of the nested dictionary to reference later
        pos_cache = copy.deepcopy(self.body_dict)

        for block_num in self.body_dict:
            # if snake head moves past left bounds, then resets to right side; and vice versa
            # if snake head moves past upper bounds, then resets to bottom side; and vice versa
            if block_num == 0:  # if the head block
                if self.direction == 'left':
                    if self.body_dict[0][0] <= 0:
                        self.body_dict[0][0] = self.max_x
                    else:
                        self.body_dict[0][0] -= distance
                elif self.direction == 'right':
                    if self.body_dict[0][0] >= self.max_x - self.block_size:
                        self.body_dict[0][0] = 0
                    else:
                        self.body_dict[0][0] += distance
                elif self.direction == 'up':
                    if self.body_dict[0][1] <= 0:
                        self.body_dict[0][1] = self.max_y
                    else:
                        self.body_dict[0][1] -= distance
                elif self.direction == 'down':
                    if self.body_dict[0][1] >= self.max_y - self.block_size:
                        self.body_dict[0][1] = 0
                    else:
                        self.body_dict[0][1] += distance

            else:  # move body blocks to block ahead of it
                self.body_dict[block_num] = pos_cache[block_num-1]
