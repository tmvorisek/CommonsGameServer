import asyncio
import random

from GameLogic.RoundSubmission import RoundSubmission


class Player:

    def __init__(self, player_num, game):
        self.player_num = player_num
        self.game = game

    async def get_round_submissions(self, start_round, end_round):
        """
        Gets random round submissions for the given round interval

        :param start_round: Int
        :param end_round: Int
        :return: List<RoundSubmission>
        """
        random_time = random.randrange(0, 3)
        await asyncio.sleep(random_time)
        round_submissions = []
        for current_round in range(start_round, end_round):
            round_submission = RoundSubmission.get_random_round_submission(self.player_num, current_round)
            round_submissions.append(round_submission)
        print(f"\tPlayer {self.player_num} returning round submissions for {start_round} to {end_round}")
        return round_submissions


