from GameLogic.ConfigReader import ConfigReader


class GameRules:

    def __init__(self, config_file_name):
        game_rules = ConfigReader.get_rules_from_config(config_file_name)
        self.NUM_PLAYERS = game_rules['number_of_players']
        self.NUM_SUMMITS = game_rules['number_of_summits']
        self.ROUNDS_PER_SUMMIT = game_rules['rounds_per_summit']
        self.STARTING_INDEX = game_rules['starting_index']
        self.OVERHARVEST_EFFECT = game_rules['overharvest_index_effect']
        self.RESTORATION_EFFECT = game_rules['restoration_index_effect']
        self.RESTORE_COST = game_rules['restoration_cost']
        self.POLICE_COST = game_rules['police_cost']
        self.SUSTAIN_YIELD = game_rules['base_sustain_yield']
        self.OVERHARVEST_YIELD = game_rules['base_overharvest_yield']
        self.OVERHARVEST_FINE = game_rules['overharvest_fine']
        self.ACTIONS_ARE_HIDDEN = game_rules['actions_are_hidden']

    def enact_rule(self, rule_proposal):
        rule_proposal.enact_rule(self)
