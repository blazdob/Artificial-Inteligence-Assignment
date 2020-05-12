import pygame
import json




class QLearning():
    def __init__(self):
        self.gameCNT = 0  # Game count of current run, incremented after every death
        self.DUMPING_N = 500  # Number of iterations to dump Q values to JSON after
        self.discount = 0.975
        self.r = {"noObsticlecloser": 0.1,"obsticle": -1, "noObsticlefurther": -0.1, "final": 100}  # Reward function
        self.gama = 0.8
        self.load_qvalues()
        self.moves = []

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
        pass
    def update_scores(self):
        """
        Update qvalues via iterating over experiences
        """
        pass


def checkCrash(player, list_of_obsticles): 
    pass