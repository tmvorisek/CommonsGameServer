import random


class PlayerActions:

    SUSTAIN = 'SUSTAIN'
    OVERHARVEST = 'OVERHARVEST'
    RESTORE = 'RESTORE'
    POLICE = 'POLICE'
    OPTIONS = [SUSTAIN, OVERHARVEST, RESTORE, POLICE]

    @staticmethod
    def get_random_action():
        """
        Returns a random action from options
        """
        random_index = random.randrange(0, len(PlayerActions.OPTIONS))
        action = PlayerActions.OPTIONS[random_index]
        return action

