import pygame
import snake
import os


DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600
FPS = 60

colors = {'black': (0, 0, 0),
          'white': (255, 255, 255),
          'red':   (255, 0, 0)}

# os.environ["SDL_VIDEODRIVER"] = "dummy" # run simulations headlessly
pygame.init()

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Lil Noodle')
clock = pygame.time.Clock()

def display_head(x, y):
    # head_img = pygame.image.load('head.png') # load the snakehead
    pygame.draw.rect(gameDisplay, colors['white'], [x, y, 20, 20])
    # gameDisplay.blit(head_img, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, colors['white'])
    return textSurface, textSurface.get_rect() # allows us to position text

def draw_score(score, x=0, y=0): # display score
    score_text = pygame.font.SysFont('arial', 30)
    text_surf, text_rect = text_objects(f"Score: {score}", score_text)
    text_rect.top = x
    text_rect.left = y
    gameDisplay.blit(text_surf, text_rect)
    pygame.display.update()



def main_loop():
    
    
    x = (DISPLAY_WIDTH * 0.5)
    y = (DISPLAY_HEIGHT * 0.5)

    play = True

    while play:
        draw_score(score) # display the score

        x_change = 0

        for event in pygame.event.get(): # retrieve all events (inputs)
            if event.type == pygame.QUIT: # if click on the X of window to quit
                play = False # break from main loop
            
            if event.type == pygame.KEYDOWN: # if keypress
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                
        x += x_change

        # draw background, snake, and food
        gameDisplay.fill(colors['black']) # draw background 
        display_head(x, y)

        pygame.display.update() # update the entire surface

        clock.tick(FPS) # input is the frames per second


score = 0

main_loop()
pygame.quit()
quit()