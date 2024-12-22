class Parameters:
    def __init__(self):
        self.FPS = 60
        self.SCORE = 0
        self.SIZE_SPRITES = 50

    def set_score(self, score):
        self.SCORE += score
    
    def get_score(self):
        return self.SCORE
    

params = Parameters()