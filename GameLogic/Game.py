from GameLogic.CommonsIndex import CommonsIndex
from GameLogic.ScoreBoard import ScoreBoard


class Game:

    START_INDEX = 7.0

    def __init__(self, num_players):
        self.players = [None] * num_players
        for player_num in range(num_players):
            self.players[player_num] = player_num
        self.score_board = ScoreBoard(self.players)
        self.current_round = 0
        self.commons_index = CommonsIndex(self.START_INDEX)

    def end_summit(self, num_rounds):
        for _ in range(num_rounds):
            self.play_to_next_round()

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

