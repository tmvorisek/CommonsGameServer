from commons_index import CommonsIndex

class Summit(object):
    """docstring for Summit"""
    def __init__(self, round_count, player_count, commons_index):
        super(Summit, self).__init__()
        self.round_count = round_count
        self.player_count = player_count
        self.moves = \
            [["" for p in range(0,player_count)] for r in range(0,round_count)]
        self.commons_index = CommonsIndex(commons_index)        

    def add_move(self, player_index, round_index, move):
        try:
            self.moves[round_index][player_index] = move
        except IndexError as e:
            raise LogicException("Only " + self.round_count + " moves allowed per summit.")

    def get_move(self, player_index, round_index):
        return self.moves[round_index][player_index]

    def get_commons_index(self):
        return self.commons_index.value