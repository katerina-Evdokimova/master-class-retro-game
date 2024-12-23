class Parameters:
    def __init__(self):
        self.FPS = 60
        self.SIZE = self.WIDTH, self.HEIGHT = 500, 600
        self.SCORE = 0
        self.LAST_SCORE_BOOST = 0
        self.SIZE_SPRITES = 50
        self.BOOST = 0

    def set_score(self, score):
        self.SCORE += score
        # Увеличиваем скорость каждые 20 очков
        if self.SCORE - self.LAST_SCORE_BOOST >= 20:
            self.BOOST += 0.05
            self.LAST_SCORE_BOOST += 20

    def get_score(self):
        return self.SCORE

    def get_boost(self):
        return self.BOOST

    def get_size(self):
        return self.SIZE

    def get_width(self):
        return self.WIDTH

    def get_height(self):
        return self.HEIGHT


params = Parameters()
