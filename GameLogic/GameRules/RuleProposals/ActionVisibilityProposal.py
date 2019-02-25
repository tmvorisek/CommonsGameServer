from GameLogic.GameRules.GameRules import GameRules
from GameLogic.GameRules.RuleProposals.RuleProposal import RuleProposal


class ActionVisibilityProposal(RuleProposal):

    def __init__(self, are_hidden):
        self.are_hidden = are_hidden

    def enact_rule(self, game_rules: GameRules):
        game_rules.ACTIONS_ARE_HIDDEN = self.are_hidden
