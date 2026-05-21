import random


class Agent:
    name = "base"

    def choose_action(self, observation, legal_actions):
        raise NotImplementedError


class RandomAgent(Agent):
    name = "random"

    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def choose_action(self, observation, legal_actions):
        return self.rng.choice(legal_actions)