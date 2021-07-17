import random
import numpy as np
import matplotlib.pyplot as plt

# const
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

ACTION_STRAIGHT = 0
ACTION_RIGHT = 1
ACTION_LEFT = 2

COLOR_GRID = (0, 0, 0)
COLOR_FOOD = (255, 0, 0)
COLOR_HEAD = (0, 255, 0)
COLOR_BODY = (0, 0, 255)


class ActionSpace:
    def __init__(self):
        self.actions = [ACTION_STRAIGHT, ACTION_RIGHT, ACTION_LEFT]
    
    def valid_action(self, action):
        if action in self.actions:
            return True
        return False
    
    def sample_choice(self):
        return random.sample(self.actions, 1)[0]

class SnakeGameEnv:
    def __init__(self, boare_shape: list=[15, 15], init_head_pos: list=[7, 7], n_foods: int=1):
        self.board_shape = boare_shape
        self.init_snake_head = init_head_pos.copy()
        self.snake_head = init_head_pos.copy()
        self.n_foods = n_foods
        self.action_space = ActionSpace()

        self.direction = DIR_UP
        self.score = 0
        self.snake_body = []
        self.foods = []

        self._init_foods()
    
    def seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)
        self._init_foods()

    def _init_foods(self):
        self.foods = []
        row, col = self.board_shape

        perm = np.random.permutation(row * col)

        n_foods, index = 0, 0
        while n_foods < self.n_foods:
            new_pos = (perm[index] // col, perm[index] % col)
            if list(new_pos) == self.snake_head:
                index += 1
                continue
            self.foods.append(new_pos)
            n_foods += 1
            index += 1

    def _get_body_danger(self) -> list:
        """
        Output:
            [danger-up, danger-right, danger-down, danger-left]
        """
        danger = [0, 0, 0, 0]
        head = self.snake_head
        body = [list(b) for b in self.snake_body]
        if [head[0] - 1, head[1]] in body:
            danger[0] = 1
        if [head[0], head[1] + 1] in body:
            danger[1] = 1
        if [head[0] + 1, head[1]] in body:
            danger[2] = 1
        if [head[0], head[1] - 1] in body:
            danger[3] = 1
        return danger

    
    def _get_state(self) -> list:
        """
        Output:
            List(int): [danger-straight, danger-right, danger-left, 
                        dir-up, dir-right, dir-down, dir-left,
                        food-up, food-right, food-down, food-left]
        """
        row, col = self.board_shape
        state = [0] * 11
        body_danger = self._get_body_danger()

        if self.direction == DIR_UP:
            state[0] = 1 if self.snake_head[0] == 0 or body_danger[0] == 1 else 0
            state[1] = 1 if self.snake_head[1] == col - 1 or body_danger[1] == 1 else 0
            state[2] = 1 if self.snake_head[1] == 0 or body_danger[3] == 1 else 0
        elif self.direction == DIR_RIGHT:
            state[0] = 1 if self.snake_head[1] == col - 1 or body_danger[1] == 1 else 0
            state[1] = 1 if self.snake_head[0] == row - 1 or body_danger[2] == 1 else 0
            state[2] = 1 if self.snake_head[0] == 0 or body_danger[0] == 1 else 0
        elif self.direction == DIR_DOWN:
            state[0] = 1 if self.snake_head[0] == row - 1 or body_danger[2] == 1 else 0
            state[1] = 1 if self.snake_head[1] == 0 or body_danger[3] == 1 else 0
            state[2] = 1 if self.snake_head[1] == col - 1 or body_danger[1] == 1 else 0
        elif self.direction == DIR_LEFT:
            state[0] = 1 if self.snake_head[1] == 0 or body_danger[3] == 1 else 0
            state[1] = 1 if self.snake_head[0] == 0 or body_danger[0] == 1 else 0
            state[2] = 1 if self.snake_head[0] == row - 1 or body_danger[2] == 1 else 0
        
        state[self.direction + 3] = 1
        for food in self.foods:
            if food[0] < self.snake_head[0]:
                state[7] = 1
            if food[0] > self.snake_head[0]:
                state[9] = 1
            if food[1] > self.snake_head[1]:
                state[8] = 1
            if food[1] < self.snake_head[1]:
                state[10] = 1
        
        return state
    
    def reset(self) -> list:
        self.snake_head = self.init_snake_head.copy()
        self.snake_body = []
        self._init_foods()
        self.score = 0
        return self._get_state()
    
    def _in_map(self, pos):
        row, col = self.board_shape
        if 0 <= pos[0] < row and 0 <= pos[1] < col:
            return True
        return False
    
    def _eat_food(self):
        row, col = self.board_shape
        removed = []
        reward, eaten, index = 0, 0, 0
        for food in self.foods:
            if self.snake_head == list(food):
                reward += 1
                eaten += 1
                self.score += 1
                removed.append(food)
        
        for food in removed:
            self.foods.remove(food)
        
        perm = np.random.permutation(row * col)
        while eaten > 0:
            new_pos = (perm[index] // col, perm[index] % col)
            conflict = False
            if self.snake_head[0] == list(new_pos):
                conflict = True
            for body in self.snake_body:
                if list(body) == list(new_pos):
                    conflict = True
                    break
            for food in self.foods:
                if list(food) == list(new_pos):
                    conflict = True
                    break
            index += 1
            if conflict:
                continue
            self.foods.append(new_pos)
            eaten -= 1

        return reward
    
    def _hit_body(self, pos):
        for body in self.snake_body:
            if list(pos) == list(body):
                return True
        return False
    
    def _change_direction(self, action) -> int:
        """
        Output:
            reward: 1 for eat food, 0 for nothing, -1 for hit
        """
        dr = [-1, 0, 1, 0]
        dc = [0, 1, 0, -1]
        reward = 0
        prev_head = self.snake_head.copy()

        if action == ACTION_RIGHT:
            self.direction = (self.direction + 1) % 4
        elif action == ACTION_LEFT:
            self.direction = (self.direction + 3) % 4

        new_head = [self.snake_head[0] + dr[self.direction], self.snake_head[1] + dc[self.direction]]
        if not self._in_map(new_head):
            return -1
        elif self._hit_body(new_head):
            return -1
        else:
            self.snake_head = new_head
            prev_body = prev_head.copy()
            if len(self.snake_body):
                prev_body = self.snake_body.pop()
                self.snake_body.insert(0, prev_head)
            reward = self._eat_food()
            if reward > 0:
                self.snake_body.append(prev_body)
        
        return reward

    def step(self, action: int):
        assert(self.action_space.valid_action(action)), "Invalid Action"
        reward = self._change_direction(action)
        done = True if reward == -1 else False
        state = self._get_state()
        info = { "Info": "step" }

        return state, reward, done, info
            
    def render(self) -> np.ndarray:
        row, col = self.board_shape
        colors = np.zeros([row, col] + [3], dtype=np.uint8)
        
        colors[self.snake_head[0], self.snake_head[1], :] = list(COLOR_HEAD)
        for body in self.snake_body:
            r, c = body
            colors[r, c, :] = list(COLOR_BODY)
        
        for food in self.foods:
            r, c = food
            colors[r, c, :] = list(COLOR_FOOD)

        return colors

    def display(self, ticks: float=1.0):
        plt.clf()
        colors = self.render()
        plt.imshow(colors)        
        plt.show(block=False)
        plt.pause(ticks)
        plt.close()
    
    def get_score(self):
        return self.score
