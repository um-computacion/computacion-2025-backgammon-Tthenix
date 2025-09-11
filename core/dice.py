import random

class Dice:
    def __init__(self):
        pass
    
    def roll(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        return (die1, die2)
    
    def is_double(self, roll_result):
        return roll_result[0] == roll_result[1]
    
    def get_moves(self, roll_result):
        if self.is_double(roll_result):
            return [roll_result[0]] * 4
        else:
            return [roll_result[0], roll_result[1]]