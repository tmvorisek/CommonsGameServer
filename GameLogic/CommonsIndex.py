from GameLogic.RoundSubmission import RoundSubmission


class CommonsIndex:

    OVERHARVEST_EFFECT = 0.1
    RESTORATION_EFFECT = 0.1
    RESTORE_COST = 6
    POLICE_COST = 6
    SUSTAIN_YIELD = 10
    OVERHARVEST_YIELD = 20
    OVERHARVEST_FINE = 20

    def __init__(self, index):
        self.index = index

    def update_index(self, overharvest_num, restore_num):
        """
        Updates the index given the amount of overharvest and restore actions made

        :param overharvest_num: Int
        :param restore_num: Int
        """
        if overharvest_num > 0:
            self.index -= overharvest_num * self.OVERHARVEST_EFFECT
        elif restore_num > 0:
            self.index += restore_num * self.RESTORATION_EFFECT
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
        if action == RoundSubmission.SUSTAIN:
            earnings = self.get_sustain_yield(sustain_num)
        elif action == RoundSubmission.OVERHARVEST:
            earnings = self.get_overharvest_yield(sustain_num, police_num)
        elif action == RoundSubmission.RESTORE:
            earnings = self.get_restore_yield(restore_num)
        elif action == RoundSubmission.POLICE:
            earnings = self.get_police_yield(police_num)
        else:
            raise Exception(f"Invalid action type {action}")
        return earnings

    def get_sustain_yield(self, sustain_num):
        sustain_yield = self.index * self.SUSTAIN_YIELD + sustain_num
        return sustain_yield

    def get_overharvest_yield(self, sustain_num, police_num):
        if police_num > 0:
            return -self.OVERHARVEST_FINE
        else:
            overharvest_yield = self.index * self.OVERHARVEST_YIELD + sustain_num
            return overharvest_yield

    def get_restore_yield(self, restore_num):
        return -self.RESTORE_COST / restore_num

    def get_police_yield(self, police_num):
        return -self.POLICE_COST / police_num
