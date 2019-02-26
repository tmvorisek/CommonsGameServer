from GameLogic.GameRules.GameRules import GameRules
from GameLogic.GameRules.RuleProposals.RuleProposal import RuleProposal


class OverharvestFineProposal(RuleProposal):

    def __init__(self, fine_change):
        self.fine_change = fine_change

    def enact_rule(self, game_rules: GameRules):
        game_rules.OVERHARVEST_FINE = self.fine_change
