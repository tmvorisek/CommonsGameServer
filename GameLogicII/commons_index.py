class CommonsIndex(object):
    """docstring for CommonsIndex"""
    def __init__(self, value, config):
        super(CommonsIndex, self).__init__()
        self.value = float(value)
        self.config = config

    def harvest(self, harvest_count):
        return self.config["base_sustain_yield"] + (5000*self.value) + (harvest_count*2000)

    def overharvest(self, harvest_count, police_count):
        if police_count == 0:
            return self.config["base_overharvest_yield"] + (5000*self.value) \
                + (harvest_count*2000)
        else:
            return self.config["overharvest_fine"]

    def police(self, police_count):
        return int(self.config["police_cost"]/police_count)

    def invest(self):
        return self.config["restoration_cost"]

