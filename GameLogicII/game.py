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
                self.config["starting_index"],
                self.config)]
        self.players = [Player(p) for p in range(0,player_count)]
        self.active_summit_index = 0

    def add_move(self, player_index, move):
        player = self.players[player_index]
        if player.active_round < (self.active_summit_index+1)*self.config["rounds_per_summit"]:
            summit_index = int(player.active_round / self.config["rounds_per_summit"])
            summit = self.summits[self.active_summit_index]
            summit.add_move(player_index, 
                player.active_round % self.config["rounds_per_summit"], 
                move)
            player.active_round += 1
        else:
            raise LogicException("Only " + str(self.config["rounds_per_summit"]) + " moves allowed per summit.")

    def get_scoreboard_for_player(self, player_id):
        scoreboard = []
        for summit in self.summits:
            scoreboard.append(summit.get_scoreboard_for_player(player_id))
        return scoreboard


    def finish_summit(self):
        active_summit = self.summits[self.active_summit_index]
        new_index = active_summit.calculate_index()
        self.summits.append(
            Summit( self.config["rounds_per_summit"], 
                    self.player_count, 
                    new_index, 
                    self.config))
        if self.active_summit_index < self.config["number_of_summits"]:
            self.active_summit_index += 1
        for player in self.players:
            player.wealth += active_summit.get_yield_for_player(player.index)

    def is_last_summit(self):
        return self.active_summit_index < self.config["number_of_summits"]


    def get_player(self, player_index):
        return self.players[player_index]

    def get_commons_index(self):
        return self.summits[self.active_summit_index].get_commons_index()


