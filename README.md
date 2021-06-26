# RLGame

## Description

RLGame is a package provides multi-agent implementation of some classic games for Reinforcement Learning (RL).

## Dependencies

* pip
* numpy
* matplotlib

## Getting start

Take "snake" for example:

```python
import RLGame
env = RLGame.make("snake")
state = env.reset()
env.display(ticks=0.01)

for _ in range(1000):
    action = env.action_space.sample_choice()
    state, reward, done, info = env.step(action)
    if done:
        break
    env.display(ticks=0.01)
print(f"score: {env.get_score()}")
```

where ```state``` (np.ndarray) is the environment state, ```reward``` (int or float) is the reward from this action, ```done``` (boolean) is a signal which identify whether the game has ended, and ```info``` (dict) is for debugging.
