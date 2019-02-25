class GameRules:

    def __init__(self, summits, rounds_per_summit, num_players):
        self.NUM_SUMMITS = summits
        self.ROUNDS_PER_SUMMIT = rounds_per_summit
        self.NUM_PLAYERS = num_players
        self.STARTING_INDEX = 7.0
        self.OVERHARVEST_EFFECT = 0.1
        self.RESTORATION_EFFECT = 0.1
        self.RESTORE_COST = 6
        self.POLICE_COST = 6
        self.SUSTAIN_YIELD = 10
        self.OVERHARVEST_YIELD = 20
        self.OVERHARVEST_FINE = 20

    def enact_rule(self, rule_proposal):
        rule_proposal.enact_rule(self)
