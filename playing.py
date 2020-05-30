"""
Once a model is learned, use this to play it.
"""
import numpy as np
from nn import neural_net

from game import Game

NUM_SENSORS = 5


def play(model):

    car_distance = 0
    game = Game()

    # Do nothing to get initial.
    _, state = game.step(2)

    # Move.
    while True:
        car_distance += 1

        # Choose action.
        action = (np.argmax(model.predict(state)))
        
        # Take action.
        _, state = game.step(action)

        # Tell us something.
        if car_distance % 1000 == 0:
            print("Current distance: %d frames." % car_distance)


if __name__ == "__main__":
    saved_model = 'saved-models/128-128-64-50000-75000.h5'
    model = neural_net(NUM_SENSORS, [128, 128], saved_model)
    play(model)
