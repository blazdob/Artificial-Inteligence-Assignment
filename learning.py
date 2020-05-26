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
        self.r = {"noObsticlecloser": 0.1, "obsticle": -1, "noObsticlefurther": -0.1}  # Reward function
        self.gama = 0.8
        self.load_qvalues()
        self.last_state = "400_200_-10"
        self.last_action = 0 #TODO na nek način je treba označin posamezne akcije, ki so možne
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
            fill = open("qvalues.json", "r")
        except IOError:
            return
        self.qvalues = json.load(fill)
        fill.close()

    def dump_qvalues(self, force=True):
        """
        Dump the qvalues to the JSON file
        """
        if self.gameCNT % self.DUMPING_N == 0 or force:
            fill = open("qvalues.json", "w")
            json.dump(self.qvalues, fill)
            fill.close()
            print("Q-values updated on local file.")

    def act(self, xdif, ydif, vel):
        """
        Chooses the best action with respect to the current state
        """
        #### POLICY
        state = self.map_state(xdif, ydif, vel, self.game.get_sensor_values())


        self.moves.append(
            (self.last_state, self.last_action, state)
        )  # dodamo potezo

        self.last_state = state  # posodobimo staro stanje

        ##### STEP
        # move forward
        if True:
             #TODO
            action = Action.RIGHT.value
            QLearning.mock_game_event(action)
            self.last_action = 0
            pass
        elif True:
             #TODO
            action = Action.LEFT.value
            QLearning.mock_game_event(action)
            self.last_action = 0
            pass

    def update_scores(self):
        """
        Update qvalues via iterating over experiences
        """
        history = list(reversed(self.moves))
        
        #pogoj na to, če se zaletimo
        crash = True if True else False

        # Q-learning score updates
        t = 1
        for exp in history:
            state = exp[0] #trenutni state
            act = exp[1] #akcija
            res_state = exp[2] # naslednji state
            # Select reward
            cur_reward = self.r[0] #TODO

            # Update
            self.qvalues[state][act] = (1-self.lr) * (self.qvalues[state][act]) + self.lr * ( cur_reward + self.discount*max(self.qvalues[res_state]) )
            t += 1

        self.gameCNT += 1  # povečamo številko
        if dump_qvalues:
            self.dump_qvalues()  
        self.moves = []  # izbrišemo zgodovino

    def map_state(self, xdif, ydif, vel, sensorVal):
        """
        Map the (xdif, ydif, vel) to the respective state, with regards to the grids
        The state is a string, "xdif_ydif_vel"

        X -> [0,5,10,...400]
        Y -> [0,5,10,...200]
        vel -> [-20,-19,-18,...20]
        """
        print(sensorVal)
        return "0_0_10"

    @staticmethod
    def mock_game_event(action):
        if action == Action.RIGHT.value:
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
