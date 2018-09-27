class GameStats():
    """ Track game states """

    def __init__(self, ai_settings):
        """ initial states """
        self.ai_settings = ai_settings
        self.game_active = False
        self.reset_stats()
        # high score
        self.high_score = 0

    def reset_stats(self):
        """ initial the game run-timing states """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
