from ConfigReader import ConfigReader
from logic_exception import LogicException
from player import Player
from summit import Summit

class Game(object):
    """docstring for Game"""
    def __init__(self, player_count):
        super(Game, self).__init__()
        self.player_count = player_count
        self.config = ConfigReader.get_rules_from_config("config.json")
        self.summits = \
            [Summit(self.config["rounds_per_summit"], 
                self.player_count,
                self.config["starting_index"])]
        self.players = [Player(p) for p in range(0,player_count)]
        self.active_summit = 0

    def add_move(self, player_index, move):
        player = self.players[player_index]
        if player.active_round < (self.active_summit+1)*self.config["rounds_per_summit"]:
            summit_index = int(player.active_round / self.config["rounds_per_summit"])
            summit = self.summits[self.active_summit]
            summit.add_move(player_index, 
                player.active_round % self.config["rounds_per_summit"], 
                move)
            player.active_round += 1
        else:
            raise LogicException("Only " + str(self.config["rounds_per_summit"]) + " moves allowed per summit.")

    def finish_summit(self):
        self.summits.append(Summit(self.config["rounds_per_summit"], self.player_count))
        if self.active_summit < self.config["number_of_summits"]:
            self.active_summit += 1
        for summit in summits:
            for round_index in range(0,self.config["rounds_per_summit"]):
                for player in self.players:
                    print(summit.get_move(player.index, round_index))


    def get_player(self, player_index):
        return self.players[player_index]

    def get_commons_index(self):
        return self.summits[self.active_summit].get_commons_index()


