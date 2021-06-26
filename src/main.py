from matplotlib.colors import to_hex
import RLGame
from argparse import ArgumentParser

def random_demo(game_name, ticks):
    env = RLGame.make(game_name)
    state = env.reset()
    env.display(ticks=ticks)

    while True:
        action = env.action_space.sample_choice()
        state, reward, done, _ = env.step(action)
        if done:
            break
        env.display(ticks=ticks)
    
    score = env.get_score()
    print(f"score: {score}")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--game_name", type=str, default="2048")
    parser.add_argument("--ticks", type=float, default=1.0)
    args, unknown = parser.parse_known_args()
    kargs = vars(args)

    random_demo(**kargs)