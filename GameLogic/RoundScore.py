from GameLogic.RoundSubmission import RoundSubmission


class RoundScore:
    """
    Holds the score of each player and their actions for a given round
    """

    def __init__(self, round_num):
        self.round_num = round_num
        self.player_actions = {}
        self.player_earnings = {}
        self.total_sustain = 0
        self.total_overharvest = 0
        self.total_restore = 0
        self.total_police = 0
        self.initial_commons_index = 0
        self.final_commons_index = 0
        self.is_calculated = False

    def add_submission(self, round_submission):
        """
        Given a RoundSubmission, the player action is set for the round

        :param round_submission: RoundSubmission
        """
        if round_submission.round_num != self.round_num:
            raise Exception(f"Round nums don't match: {round_submission.round_num} != {self.round_num}")
        player_num = round_submission.player_num
        player_action = round_submission.player_action
        self.player_actions[player_num] = player_action
        self.add_action_to_total(player_action)

    def add_action_to_total(self, action):
        """
        :param action: The action taken to be added to the total
        """
        if action == RoundSubmission.SUSTAIN:
            self.total_sustain += 1
        elif action == RoundSubmission.OVERHARVEST:
            self.total_overharvest += 1
        elif action == RoundSubmission.RESTORE:
            self.total_restore += 1
        elif action == RoundSubmission.POLICE:
            self.total_police += 1
        else:
            raise Exception(f"Invalid action {action}")

    def calculate_player_earnings(self, commons_index):
        """
        Calculates the players' earnings for the round and updates the commons index

        :param commons_index: CommonsIndex to be used to calculate earnings
        :return: CommonsIndex that is updated with new index based on number of overharvests and restores
        """
        self.initial_commons_index = commons_index.index
        for player_num, action in self.player_actions.items():
            earnings = commons_index.get_yield(self, action)
            self.player_earnings[player_num] = earnings
        commons_index.update_index(self.total_overharvest, self.total_restore)
        self.final_commons_index = commons_index.index
        self.is_calculated = True
        return commons_index

    def get_player_earnings(self, player_num):
        """
        :param player_num: The number of the player
        :return: Decimal value of the player's earnings
        """
        return self.player_earnings[player_num]

    def __str__(self):
        """
        :return: The round score in a string format
        """
        to_string = f"Round {self.round_num}\n"
        to_string += f"Commons: {self.initial_commons_index} to {self.final_commons_index}\n"
        for player_num in self.player_actions.keys():
            action = self.player_actions[player_num]
            earnings = self.player_earnings[player_num]
            to_string += f"\tPlayer: {player_num}, Action: {action}, Earnings: {earnings}\n"
        return to_string
