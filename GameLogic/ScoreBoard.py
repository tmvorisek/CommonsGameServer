from GameLogic.PlayerActions import PlayerActions
from GameLogic.RoundScore import RoundScore


class ScoreBoard:

    def __init__(self, players):
        self.players = players
        self.round_scores = {}
        self.hidden_rounds = {}

    def get_round_score(self, game_round):
        if game_round not in self.round_scores.keys():
            self.round_scores[game_round] = RoundScore(game_round)
        return self.round_scores[game_round]

    def set_end_of_round_scores(self, game_round, commons_index):
        round_score = self.round_scores[game_round]
        round_score.set_end_of_round_scores(commons_index)

    def add_player_action(self, player_id, action, game_round):
        if game_round not in self.round_scores.keys():
            self.round_scores[game_round] = RoundScore(game_round)

        self.round_scores[game_round].set_player_action(player_id, action)

    def get_player_score(self, player_id):
        score_board = {player_id: []}
        for game_round, round_score in self.round_scores.items():
            if not round_score.is_over():
                raise Exception("Can't get round " + str(game_round) 
                    + " scores because round isn't over")
            round_num = round_score.game_round
            player_action = round_score.get_player_action(player_id)
            player_score = round_score.get_player_score(player_id)
            score_board[player_id].append((round_num, player_action, player_score))
        return score_board

    def get_score_board(self, player_id, game_rules):
        score_board = {}
        for game_round, round_score in self.round_scores.items():
            for player in self.players:
                player_action = round_score.get_player_action(player)
                player_score = round_score.get_player_score(player)
                if game_round not in self.hidden_rounds.keys():
                    self.hidden_rounds[game_round] = game_rules.ACTIONS_ARE_HIDDEN
                if self.hidden_rounds[game_round] and player != player_id:
                    score = self.get_hidden_score(player, player_action, player_score)
                else:
                    score = (player, player_action, player_score)
                if game_round not in score_board.keys():
                    score_board[game_round] = []
                score_board[game_round].append(score)
        return score_board

    def get_hidden_score(self, player, player_action, score):
        if player_action == PlayerActions.OVERHARVEST and score < 0:
            score = (player, player_action, score)
        else:
            score = (player, '-', '-')
        return score
