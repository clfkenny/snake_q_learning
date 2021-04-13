import pygame

class Snake:
    '''snake that user controls
        - snake has a constant velocity
        - pressing a key changes the velocity
        - when 'head' of snake passes over 'food', 'food disappears and 
        snake's body increases in length
        - game instance ends when snake 'head' runs into its 'body'
    '''

    def __init__(self, x, y, velocity=10, direction='up'):
        self.x = x
        self.y = y
        self.velocity = velocity # speed at which snake moves
        self.direction = direction # direction of velocity


class Game():
    ''' game constructer class
        - represents instance of game
        - if want to replay/reset, then instantiate another instance
    '''
  
    def __init__(self):
        self.score = 0

  