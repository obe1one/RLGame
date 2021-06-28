import math
import random
import numpy as np
import matplotlib.pyplot as plt
from RLGame.game2048.const import *

class ActionSpace:
    def __init__(self):
        self.actions = [DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT]
    
    def valid_action(self, action):
        if action in self.actions:
            return True
        return False
    
    def sample_choice(self):
        return random.sample(self.actions, 1)[0]

class Game2048Env:
    def __init__(self, board_edge: int=4):
        self.board_shape = [board_edge, board_edge]
        self.score = 0
        self.action_space = ActionSpace()
        self.board = np.zeros(self.board_shape, dtype=np.uint32)

        self._init_board()
    
    def seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)
    
    def _init_board(self):
        Y, X = self.board_shape
        for y in range(Y):
            for x in range(X):
                self.board[y, x] = 0

        y = random.randint(0, Y - 1)
        x = random.randint(0, X - 1)
        init_val = random.choice([1, 2])
        self.board[y, x] = init_val
    
    @staticmethod
    def _get_color(exponent):
        if exponent == 0:
            return (0, 0, 0)
        elif 255 - 32 * exponent < 0:
            return (0, 128, 128)
        else:
            return (255 - 32 * exponent, 128, 128)
        
    def _update(self):
        pass

    def reset(self) -> np.ndarray:
        self._init_board()
        self.score = 0
        return self.board
    
    def _move_up(self):
        Y, X = self.board_shape
        new_board = np.zeros([Y, X], dtype=np.uint32)
        valid_pos = [0 for _ in range(X)]
        new_board[0] = self.board[0]
        reward = 0
        n_steps = 0
        
        for y in range(1, Y):
            for x in range(X):
                if self.board[y, x] > 0:
                    vp = valid_pos[x]
                    if new_board[vp, x] == 0:
                        new_board[vp, x] = self.board[y, x]
                        if valid_pos[x] != y:
                            n_steps += 1
                    elif self.board[y, x] == new_board[vp, x]:
                        reward += 2 ** new_board[vp, x]
                        new_board[vp, x] += 1
                        valid_pos[x] += 1
                    else:
                        valid_pos[x] += 1
                        new_board[valid_pos[x], x] = self.board[y, x]
                        if valid_pos[x] != y:
                            n_steps += 1
        
        for y in range(Y):
            for x in range(X):
                self.board[y, x] = new_board[y, x]
        if n_steps == 0 and reward == 0:
            reward = -1
        return reward
    
    def _move_right(self):
        Y, X = self.board_shape
        new_board = np.zeros([Y, X], dtype=np.uint32)
        valid_pos = [X - 1 for _ in range(Y)]
        new_board[:, X - 1] = self.board[:, X - 1]
        reward = 0
        n_steps = 0

        for x in range(X - 2, -1, -1):
            for y in range(Y):
                if self.board[y, x] > 0:
                    vp = valid_pos[y]
                    if new_board[y, vp] == 0:
                        new_board[y, vp] = self.board[y, x]
                        if valid_pos[y] != x:
                            n_steps += 1
                    elif self.board[y, x] == new_board[y, vp]:
                        reward += 2 ** new_board[y, vp]
                        new_board[y, vp] += 1
                        valid_pos[y] -= 1
                        n_steps += 1
                    else:
                        valid_pos[y] -= 1
                        new_board[y, valid_pos[y]] = self.board[y, x]
                        if valid_pos[y] != x:
                            n_steps += 1
        
        for y in range(Y):
            for x in range(X):
                self.board[y, x] = new_board[y, x]
        if n_steps == 0 and reward == 0:
            reward = -1
        return reward
    
    def _move_down(self):
        Y, X = self.board_shape
        new_board = np.zeros([Y, X], dtype=np.uint32)
        valid_pos = [Y - 1 for _ in range(X)]
        new_board[Y - 1] = self.board[Y - 1]
        reward = 0
        n_steps = 0
        
        for y in range(Y - 2, -1, -1):
            for x in range(X):
                if self.board[y, x] > 0:
                    vp = valid_pos[x]
                    if new_board[vp, x] == 0:
                        new_board[vp, x] = self.board[y, x]
                        if valid_pos[x] != y:
                            n_steps += 1
                    elif self.board[y, x] == new_board[vp, x]:
                        reward += 2 ** new_board[vp, x]
                        new_board[vp, x] += 1
                        valid_pos[x] -= 1
                    else:
                        valid_pos[x] -= 1
                        new_board[valid_pos[x], x] = self.board[y, x]
                        if valid_pos[x] != y:
                            n_steps += 1
        
        for y in range(Y):
            for x in range(X):
                self.board[y, x] = new_board[y, x]
        if n_steps == 0 and reward == 0:
            reward = -1
        return reward
        
    def _move_left(self):
        Y, X = self.board_shape
        new_board = np.zeros([Y, X], dtype=np.uint32)
        valid_pos = [0 for _ in range(Y)]
        new_board[:, 0] = self.board[:, 0]
        reward = 0
        n_steps = 0

        for x in range(1, X):
            for y in range(Y):
                if self.board[y, x] > 0:
                    vp = valid_pos[y]
                    if new_board[y, vp] == 0:
                        new_board[y, vp] = self.board[y, x]
                        if valid_pos[y] != x:
                            n_steps += 1
                    elif self.board[y, x] == new_board[y, vp]:
                        reward += 2 ** new_board[y, vp]
                        new_board[y, vp] += 1
                        valid_pos[y] += 1
                    else:
                        valid_pos[y] += 1
                        new_board[y, valid_pos[y]] = self.board[y, x]
                        if valid_pos[y] != x:
                            n_steps += 1
        
        for y in range(Y):
            for x in range(X):
                self.board[y, x] = new_board[y, x]
        if n_steps == 0 and reward == 0:
            reward = -1
        return reward
    
    def _add_block(self):
        Y, X = self.board_shape
        perm = np.random.permutation(X * Y)
        for p in perm:
            y = p // X
            x = p % X
            if not self.board[y, x]:
                init_val = random.choice([1, 2])
                self.board[y, x] = init_val
                return False
        return True
        
    def step(self, action):
        assert(self.action_space.valid_action(action))
        reward = 0
        done = False
        if action == DIR_UP:
            reward = self._move_up()
        elif action == DIR_RIGHT:
            reward = self._move_right()
        elif action == DIR_DOWN:
            reward = self._move_down()
        elif action == DIR_LEFT:
            reward = self._move_left()
        
        if reward == -1:
            done = True
        else:
            self.score += reward
            done = self._add_block()

        return self.board, reward, done, { "Info": "step" }


    def render(self):
        Y, X = self.board_shape
        colors = np.zeros([Y, X] + [3], dtype=np.uint8)
        
        for y in range(Y):
            for x in range(X):
                colors[y, x, :] = list(self._get_color(self.board[y, x]))

        return colors
    
    def render_text(self):
        Y, X = self.board_shape
        texts = [[dict() for y in range(Y)] for x in range(X)]

        for y in range(Y):
            for x in range(X):
                texts[y][x]["x"] = x
                texts[y][x]["y"] = y
                texts[y][x]["s"] = str(2 ** self.board[y][x]) if self.board[y][x] > 0 else ""
                texts[y][x]["c"] = "w"

        return texts

    def display(self, ticks: float=1):
        plt.clf()
        colors = self.render()
        texts = self.render_text()
        Y, X = self.board_shape
        plt.imshow(colors)

        for y in range(Y):
            for x in range(X):
                plt.text(**texts[y][x])
        
        plt.show(block=False)
        plt.pause(ticks)
        plt.close()
    
    def get_score(self):
        return self.score



        