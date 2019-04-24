from GameLogic.PlayerActions import PlayerActions


class RoundScore:

    def __init__(self, game_round):
        self.game_round = game_round
        self.player_actions = {}
        self.player_scores = {}
        self.total_sustain = 0
        self.total_overharvest = 0
        self.total_police = 0
        self.total_restore = 0
        self.round_over = 0

    def is_over(self):
        return self.round_over

    def set_end_of_round_scores(self, commons_index):
        self.round_over = True
        self.calculate_totals()
        for player, action in self.player_actions.items():
            player_score = commons_index.get_yield(self, action)
            self.player_scores[player] = player_score

    def calculate_totals(self):
        total_sustain = 0
        total_overharvest = 0
        total_police = 0
        total_restore = 0
        for player, action in self.player_actions.items():
            if action == PlayerActions.OVERHARVEST:
                total_overharvest += 1
            elif action == PlayerActions.SUSTAIN:
                total_sustain += 1
            elif action == PlayerActions.RESTORE:
                total_restore += 1
            elif action == PlayerActions.POLICE:
                total_police += 1
        self.total_sustain = total_sustain
        self.total_overharvest = total_overharvest
        self.total_police = total_police
        self.total_restore = total_restore

    def set_player_action(self, player_id, action):
        self.player_actions[player_id] = action

    def get_player_action(self, player_id):
        return self.player_actions.get(player_id, {})

    def get_player_score(self, player_id):
        return self.player_scores.get(player_id, {})
