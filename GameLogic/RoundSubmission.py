import random


class RoundSubmission:

    SUSTAIN = 'SUSTAIN'
    OVERHARVEST = 'OVERHARVEST'
    RESTORE = 'RESTORE'
    POLICE = 'POLICE'
    OPTIONS = [SUSTAIN, OVERHARVEST, RESTORE, POLICE]

    def __init__(self, action, player_num, round_num):
        self.player_action = action
        self.player_num = player_num
        self.round_num = round_num

    @staticmethod
    def get_random_round_submission(player_num, round_num):
        """
        Returns a RoundSubmission with a random action

        :param player_num: Int
        :param round_num: Int
        :return: RoundSubmission
        """
        random_index = random.randrange(0, len(RoundSubmission.OPTIONS))
        action = RoundSubmission.OPTIONS[random_index]
        round_submission = RoundSubmission(action, player_num, round_num)
        return round_submission

    def __str__(self):
        return f"Round {self.round_num}, Player: {self.player_num}, Action: {self.player_action}"
