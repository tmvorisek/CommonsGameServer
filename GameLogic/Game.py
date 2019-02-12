from GameLogic.CommonsIndex import CommonsIndex
from GameLogic.Player import Player
from GameLogic.ScoreBoard import ScoreBoard
import asyncio


class Game:
    """
    Start Round
        Display passed proposals
        Allow players to send in actions, votes (can't vote until second summit), and proposals
        Wait X time then End Round
    End Round
        Calculate money and index for each round
        Update the score board
        Calculate votes, and update game rules from votes
        Update each player's score boards and game rules
        If the game isn't over Start Round again
    Game Over
        Print player earnings
    """

    MAX_ROUNDS = 9
    SUMMIT_INTERVAL = 3
    COMMONS_INDEX_START = 5.0

    def __init__(self, num_players):
        self.players = []
        for player_num in range(num_players):
            player = Player(player_num, self)
            self.players.append(player)
        self.players_responded = 0
        self.commons_index = CommonsIndex(self.COMMONS_INDEX_START)
        self.score_board = ScoreBoard(self.players, self.commons_index)

    def run_game_loop(self):
        """
        Runs rounds from 0 to MAX_ROUNDS collecting RoundSubmissions from players each summit interval
        Then prints the earnings of each player
        """
        summit = 0
        current_round = 0
        while current_round < self.MAX_ROUNDS:
            print(f"Summit {summit}")
            summit += 1
            end_round = min(current_round + self.SUMMIT_INTERVAL, self.MAX_ROUNDS)
            player_submissions = asyncio.run(self.get_player_submissions(current_round, end_round))
            self.score_board.add_player_submissions(player_submissions)
            current_round = end_round
        print(str(self.score_board))
        self.print_player_earnings()

    async def get_player_submissions(self, current_round, end_round):
        """
        Returns a list of a list of RoundSubmissions for a given round interval

        :param current_round: Int
        :param end_round: Int
        :return: List<List<RoundSubmission>>
        """
        tasks = []
        for player in self.players:
            get_round_submissions_task = asyncio.create_task(player.get_round_submissions(current_round, end_round))
            tasks.append(get_round_submissions_task)
        player_submissions = await asyncio.gather(*tasks)
        return player_submissions

    def print_player_earnings(self):
        """"
        Prints the players earnings sorted from poorest to richest
        """
        all_player_earnings = []
        for player in self.players:
            player_num = player.player_num
            player_earnings = self.score_board.get_total_player_earnings(player_num)
            all_player_earnings.append((player_num, player_earnings))
        print(str(self.score_board))
        print("*** Player Earnings ***")
        for player_num, player_earnings in sorted(all_player_earnings, key=lambda earnings: earnings[1]):
            print(f"Player {player_num}: {player_earnings}")


if __name__ == '__main__':
    number_players = 5
    game = Game(number_players)
    game.run_game_loop()
