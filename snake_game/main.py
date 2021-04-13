import pygame
import snake
import os

DISPLAY_WIDTH = 300  # should be multiples of block size
DISPLAY_HEIGHT = 300
FPS = 10

BLOCK_SIZE = 20

# os.environ["SDL_VIDEODRIVER"] = "dummy" # run simulations headlessly
pygame.init()

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Lil Noodle')
clock = pygame.time.Clock()


infinite_loop = True
show_grid = False


def main_loop():

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
    while play:
        # snake.draw_grid(gameDisplay, BLOCK_SIZE, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        # snake.draw_score(score, gameDisplay)  # display the score

        for event in pygame.event.get():  # retrieve all events (inputs)
            if event.type == pygame.QUIT:  # if click on the X of window to quit
                play = False  # break from main loop

            if event.type == pygame.KEYDOWN:  # change direction of snake based on keypress
                if event.key == pygame.K_LEFT and s.direction != 'right':
                    s.direction = 'left'
                elif event.key == pygame.K_RIGHT and s.direction != 'left':
                    s.direction = 'right'
                elif event.key == pygame.K_UP and s.direction != 'down':
                    s.direction = 'up'
                elif event.key == pygame.K_DOWN and s.direction != 'up':
                    s.direction = 'down'
                elif event.key == pygame.K_p:  # press p to pause/unpause the game
                    if snake_is_stopped:
                        s.velocity = snake_velocity
                        snake_is_stopped = False
                    else:
                        s.velocity = 0
                        snake_is_stopped = True

        s.move()  # move snake
        # draw background, snake, and food
        snake.draw_window(gameDisplay, s, food_block, score, show_grid)
        s, food_block, score, crashed = snake.process_game_logic(
            s, food_block, score)  # check if scored point/game over

        if crashed and infinite_loop:  # quit current session and reruns another instance
            main_loop()
            play = False
        elif crashed and not infinite_loop:  # exit out of session
            play = False

        clock.tick(FPS)  # input is the frames per second

    print('Game over')


main_loop()
pygame.quit()
quit()
