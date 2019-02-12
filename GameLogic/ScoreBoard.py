from GameLogic.RoundScore import RoundScore


class ScoreBoard:
    """
    Holds the score of each round for all the players
    """

    def __init__(self, players, commons_index):
        self.players = players
        self.commons_index = commons_index
        self.round_scores = {}

    def add_player_submissions(self, player_submissions):
        """
        Given a list player round submissions, adds them to the total rounds scores
        and calculates the earnings/commons index for each round

        :param player_submissions: List<List<RoundSubmission>>
        """
        self.add_round_scores(player_submissions)
        self.calculate_player_earnings()

    def add_round_scores(self, player_submissions):
        """ Adds round submissions to the score board given player submissions

        :param player_submissions: List<List<RoundSubmission>>
        """
        round_scores = self.round_scores
        for player_submission in player_submissions:
            for round_submission in player_submission:
                round_num = round_submission.round_num
                if round_num not in round_scores:
                    round_score = RoundScore(round_num)
                    round_scores[round_num] = round_score
                round_score = round_scores[round_num]
                round_score.add_submission(round_submission)

    def calculate_player_earnings(self):
        """
        Calculates each player's earnings for any round that hasn't been calculated yet
        """
        for round_score_key in sorted(self.round_scores.keys()):
            round_score = self.round_scores[round_score_key]
            if not round_score.is_calculated:
                self.commons_index = round_score.calculate_player_earnings(self.commons_index)

    def get_total_player_earnings(self, player_num):
        """
        :param player_num: Int
        :return: Decimal of the player's total earnings
        """
        player_earnings = 0
        for round_num, round_score in self.round_scores.items():
            player_earnings += round_score.get_player_earnings(player_num)
        return player_earnings

    def __str__(self):
        """
        :return: String of all the scores of each round
        """
        to_string = "\n***Score Board***\n"
        for key, round_score in self.round_scores.items():
            to_string += str(round_score)
        return to_string
