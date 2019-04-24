class CommonsIndex(object):
    """docstring for CommonsIndex"""
    def __init__(self, value):
        super(CommonsIndex, self).__init__()
        self.value = float(value)

    def harvest(self, count):
        return 40000 + (5000*self.value) + (count*2000)

    def overharvest(self, count):
        return 80000 + (5000*self.value) + (count*2000)
