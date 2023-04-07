class Game:
    def __init__(self):
        self.is_pot_active = False
        self.total_pot = 0
    
    def reset(self):
        self.is_pot_active = False
        self.total_pot = 0
