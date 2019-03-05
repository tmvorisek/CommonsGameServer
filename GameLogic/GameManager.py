from GameLogic.Game import Game
from GameLogic.GameRules.GameRules import GameRules
from GameLogic.GameRules.RuleProposals.ActionVisibilityProposal import ActionVisibilityProposal
from GameLogic.GameRules.RuleProposals.OverharvestFineProposal import OverharvestFineProposal
from GameLogic.PlayerActions import PlayerActions


class GameManager:

    def __init__(self, summits, rounds_per_summit, num_players):
        self.summits = summits
        self.rounds_per_summit = rounds_per_summit
        self.num_players = num_players
        self.game_rules = GameRules(summits, rounds_per_summit, num_players)

    def start_game(self):
        current_round = 0
        game = Game(self.game_rules)
        fine = 1
        is_visible = False
        for summit in range(self.summits):
            print(f'\nSummit {summit}')
            player_actions = self.get_random_player_actions()
            for game_round_num in range(self.rounds_per_summit):
                round_actions = player_actions[game_round_num]
                for player_id in range(self.num_players):
                    action = round_actions[player_id]
                    game.add_player_action(player_id, action, current_round)
                current_round += 1
            game.end_summit(self.rounds_per_summit)
            player_score_boards = game.get_player_score_boards()
            for player, player_score_board in player_score_boards.items():
                as_str = f"Player {player} Score Board"
                for game_round, player_score in player_score_board.items():
                    if game_round % self.rounds_per_summit == 0:
                        as_str += f'\n\tSummit {int(game_round / self.rounds_per_summit)}'
                    as_str += f"\n\t\tRound {game_round}: {player_score}"
                print(as_str)
            overharvest_fine_rule = OverharvestFineProposal(fine)
            action_visible_rule = ActionVisibilityProposal(is_visible)
            fine *= 10
            is_visible = not is_visible
            game.enact_new_rule(overharvest_fine_rule)
            game.enact_new_rule(action_visible_rule)

    def get_random_player_actions(self):
        game_actions = []
        for _ in range(self.rounds_per_summit):
            actions_in_round = []
            for player in range(self.num_players):
                actions_in_round.append(PlayerActions.get_random_action())
            game_actions.append(actions_in_round)
        return game_actions
