import enum


class Action(enum.Enum):
    ACCELERATE = "ACCELERATE"
    DECCELERATE = "DECCELERATE"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    RESTART = "RESTART"
