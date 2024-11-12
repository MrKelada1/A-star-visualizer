import pygame.color
import math


class Cell:
    def __init__(self, x, y, parent=None, init_state="clear"):
        # set array indices
        self.x = x
        self.y = y
        # set initial state
        self.state = ""
        self.color = pygame.Color("white")
        self.set_state(init_state)
        # initial a* values
        self.f = math.inf
        self.h = math.inf
        self.g = 0

        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def calc_f(self) -> int:
        """
        Using the current cell's
        :param :
        :return:
        """
        if self.parent is None:
            self.g = 0
            self.h = math.inf
            self.f = math.inf
        else:
            # calculate distance traveled from start to this cell
            self.g = int(self.parent.g + 10 * math.dist((self.parent.x, self.parent.y), (self.x, self.y)))
            # calculate ideal distance to goal
            dxh = abs(goal.x - self.x)
            dyh = abs(goal.y - self.y)
            straight = abs(dxh - dyh)
            diag = max(dxh, dyh) - straight
            self.h = 10 * straight + 14 * diag
            # add both to get f value
            self.f = self.g + self.h
        return self.f

    def set_state(self, state):
        global goal
        self.state = state
        match state:
            case "start":
                self.color = pygame.Color("green")
                self.g = 0
                self.calc_f()
            case "goal":
                self.color = pygame.Color("red")
            case "unwalkable":
                self.color = pygame.Color("black")
            case "clear":
                self.color = pygame.Color("white")
            case "path":
                self.color = pygame.Color("gold")
            case "closed":
                self.color = pygame.Color("blue")
            case "open":
                self.color = pygame.Color("pink")
            case _:
                self.state = "error"
                self.color = pygame.Color("purple")
                print("tried assigning unknown state")


start = Cell(0, 0, init_state="clear")
goal = Cell(0, 0, init_state="clear")

start.set_state("start")
goal.set_state("goal")
