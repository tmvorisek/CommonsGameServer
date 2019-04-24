class Player(object):
    """docstring for Player"""
    def __init__(self, index):
        super(Player, self).__init__()
        self.index = index
        self.wealth = 0
        self.active_round = 0
        