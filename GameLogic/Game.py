from GameLogic.CommonsIndex import CommonsIndex
from GameLogic.ScoreBoard import ScoreBoard


class Game:

    def __init__(self, game_rules):
        self.game_rules = game_rules
        self.players = [player for player in range(game_rules.NUM_PLAYERS)]
        self.score_board = ScoreBoard(self.players)
        self.current_round = 0
        self.commons_index = CommonsIndex(self.game_rules)

    def end_summit(self, num_rounds):
        for _ in range(num_rounds):
            self.play_to_next_round()

    def enact_new_rule(self, rule_proposal):
        self.game_rules.enact_rule(rule_proposal)

    def play_to_next_round(self):
        self.update_score_board()
        self.update_commons_index()
        self.current_round += 1

    def update_score_board(self):
        score_board = self.score_board
        score_board.set_end_of_round_scores(self.current_round, self.commons_index)

    def update_commons_index(self):
        round_score = self.score_board.get_round_score(self.current_round)
        overharvest = round_score.total_overharvest
        restore = round_score.total_restore
        self.commons_index.update_index(overharvest, restore)

    def add_player_action(self, player_id, player_action, game_round):
        self.score_board.add_player_action(player_id, player_action, game_round)

    def print_score_board(self):
        for player in self.players:
            player_score = self.score_board.get_player_score(player)
            print(f"Player {player}: {player_score}")

