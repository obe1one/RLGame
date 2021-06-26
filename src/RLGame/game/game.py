from RLGame.game2048 import Game2048Env
from RLGame.snake import SnakeGameEnv

def make(game_name, kargs={}):
    if game_name == "2048":
        return Game2048Env(**kargs)
    elif game_name == "snake":
        return SnakeGameEnv(**kargs)

class Controller:
    def __init__(self, env, ticks=0.1):
        self.env = env
        self.ticks = ticks
    
    def start(self):
        self.env.reset()
    