import pygame
import json
from _thread import start_new_thread
from time import sleep

from game import Game
from action import Action


class QLearning:
    def __init__(self):
        self.gameCNT = 0  # Game count of current run, incremented after every death
        self.DUMPING_N = 500  # Number of iterations to dump Q values to JSON after
        self.discount = 0.975
        self.r = {"noObsticlecloser": 0.1,"obsticle": -1, "noObsticlefurther": -0.1, "final": 100}  # Reward function
        self.gama = 0.8
        self.load_qvalues()
        self.moves = []
        self.game = Game()

    def run_game(self):
        while not self.game.exit and not self.game.is_crashed():
            self.act("", "", "")
            sleep(0.3)

    def load_qvalues(self):
        """
        Load q values from a JSON file
        """
        self.qvalues = {}
        try:
            fill = open("data/qvalues.json", "r")
        except IOError:
            return
        self.qvalues = json.load(fill)
        fill.close()

    def dump_qvalues(self, force=False):
        """
        Dump the qvalues to the JSON file
        """
        if self.gameCNT % self.DUMPING_N == 0 or force:
            fill = open("qvalues.json", "w")
            json.dump(self.qvalues, fill)
            fill.close()
            print("Q-values updated on local file.")

    def act(self, xdif, ydif, velocity):
        """
        Chooses the best action with respect to the current state
        """
        action = Action.ACCELERATE.value
        QLearning.mock_game_event(action)

    def update_scores(self):
        """
        Update qvalues via iterating over experiences
        """
        pass

    @staticmethod
    def mock_game_event(action):
        if action == Action.ACCELERATE.value:
            event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
        elif action == Action.DECCELERATE.value:
            event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
        elif action == Action.RIGHT.value:
            event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        elif action == Action.LEFT.value:
            event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        elif action == Action.RESTART.value:
            event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
        pygame.event.post(event)


if __name__ == "__main__":
    game = QLearning()
    start_new_thread(game.game.run, ())
    game.run_game()
