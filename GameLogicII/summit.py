from commons_index import CommonsIndex

class Summit(object):
    """docstring for Summit"""
    def __init__(self, round_count, player_count, commons_index, config):
        super(Summit, self).__init__()
        self.round_count = round_count
        self.player_count = player_count
        self.moves = \
            [["" for p in range(0,player_count)] for r in range(0,round_count)]
        self.commons_index = CommonsIndex(commons_index, config)        
        self.config = config

    def add_move(self, player_index, round_index, move):
        try:
            self.moves[round_index][player_index] = move
        except IndexError as e:
            raise LogicException("Only " + self.round_count + " moves allowed per summit.")

    def get_move(self, player_index, round_index):
        return self.moves[round_index][player_index]

    def get_commons_index(self):
        return self.commons_index.value

    def calculate_index(self):
        index = self.commons_index.value
        for r in self.moves:
            for p in r:
                if p == "sustain":
                    pass                
                elif p == "overharvest":
                    if index > -8.0:
                        index -= self.config["overharvest_index_effect"]
                elif p == "police":
                    pass
                elif  p == "invest":
                    if index < 8.0:
                        index -= self.config["restoration_index_effect"]
        return index

    def get_yield_for_player(self, player_index):
        total = 0;
        for m in self.moves:
            sustain_count = len([v for v in m if v == "sustain"])
            police_count = len([v for v in m if v == "police"])
            if m[player_index] == "sustain":
                total += self.commons_index.harvest(sustain_count)
            elif m[player_index] == "overharvest":
                total += self.commons_index.overharvest(sustain_count, police_count)
            elif m[player_index] == "police":
                total += self.commons_index.police(police_count)
            elif  m[player_index] == "invest":
                total += self.commons_index.invest()
        return total

    def get_scoreboard_for_player(self, player_index):
        scoreboard = []
        for m in self.moves:
            police_count = len([v for v in m if v == "police"])
            moves = []
            if m[player_index] == "sustain":
                for h in m:
                    if h == "police":
                        moves.append(h)
                    elif h == "overharvest" and police_count > 0:
                        moves.append(h)
                    else:
                        moves.append("")
                moves[player_index] = "sustain"
            elif m[player_index] == "overharvest":
                for h in m:
                    if h == "police":
                        moves.append(h)
                    elif h == "overharvest" and police_count > 0:
                        moves.append(h)
                    else:
                        moves.append("")
                moves[player_index] = "overharvest"
            elif m[player_index] == "police":
                scoreboard.append(m)
            elif  m[player_index] == "invest":
                for h in m:
                    if h == "police":
                        moves.append(h)
                    elif h == "overharvest" and police_count > 0:
                        moves.append(h)
                    else:
                        moves.append("")
                moves[player_index] = "invest"
            if len(moves) > 0:
                scoreboard.append(moves)

        return scoreboard

            
