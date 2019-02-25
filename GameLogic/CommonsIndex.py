from GameLogic.PlayerActions import PlayerActions


class CommonsIndex:

    def __init__(self, game_rules):
        self.game_rules = game_rules
        self.index = game_rules.STARTING_INDEX

    def update_index(self, overharvest_num, restore_num):
        """
        Updates the index given the amount of overharvest and restore actions made

        :param overharvest_num: Int
        :param restore_num: Int
        """
        if overharvest_num > 0:
            self.index -= overharvest_num * self.game_rules.OVERHARVEST_EFFECT
        elif restore_num > 0:
            self.index += restore_num * self.game_rules.RESTORATION_EFFECT
        self.index = max(0, self.index)

    def get_yield(self, round_score, action):
        """
        Given the round score and an action taken,
        returns the total earnings for that action

        :param round_score: RoundScore
        :param action: RoundSubmission.ACTION
        :return: Decimal of action's earnings
        """
        sustain_num = round_score.total_sustain
        restore_num = round_score.total_restore
        police_num = round_score.total_police
        if action == PlayerActions.SUSTAIN:
            earnings = self.get_sustain_yield(sustain_num)
        elif action == PlayerActions.OVERHARVEST:
            earnings = self.get_overharvest_yield(sustain_num, police_num)
        elif action == PlayerActions.RESTORE:
            earnings = self.get_restore_yield(restore_num)
        elif action == PlayerActions.POLICE:
            earnings = self.get_police_yield(police_num)
        else:
            raise Exception(f"Invalid action type {action}")
        return earnings

    def get_sustain_yield(self, sustain_num):
        sustain_yield = self.index * self.game_rules.SUSTAIN_YIELD + sustain_num
        return sustain_yield

    def get_overharvest_yield(self, sustain_num, police_num):
        if police_num > 0:
            return -self.game_rules.OVERHARVEST_FINE
        else:
            overharvest_yield = self.index * self.game_rules.OVERHARVEST_YIELD + sustain_num
            return overharvest_yield

    def get_restore_yield(self, restore_num):
        if restore_num == 0:
            return 0
        return -self.game_rules.RESTORE_COST / restore_num

    def get_police_yield(self, police_num):
        if police_num == 0:
            return 0
        return -self.game_rules.POLICE_COST / police_num

