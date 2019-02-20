from GameLogic.RoundScore import RoundScore


class ScoreBoard:

    STARTING_INDEX = 7

    def __init__(self, players):
        self.players = players
        self.round_scores = {}

    def get_round_score(self, game_round):
        return self.round_scores[game_round]

    def set_end_of_round_scores(self, game_round, commons_index):
        round_score = self.round_scores[game_round]
        round_score.set_end_of_round_scores(commons_index)

    def add_player_action(self, player_id, action, game_round):
        if game_round not in self.round_scores.keys():
            self.round_scores[game_round] = RoundScore(game_round)

        round_score = self.round_scores[game_round]
        round_score.set_player_action(player_id, action)

    def get_player_score(self, player_id):
        score_board = {player_id: []}
        for game_round, round_score in self.round_scores.items():
            if not round_score.is_over():
                raise Exception(f"Can't get round {game_round} scores because round isn't over")
            round_num = round_score.game_round
            player_action = round_score.get_player_action(player_id)
            player_score = round_score.get_player_score(player_id)
            score_board[player_id].append((round_num, player_action, player_score))
        return score_board
