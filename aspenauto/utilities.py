

class Utility(object):

    def __init__(self):

        return


class Electricity(Utility):

    def __init__(self):
        
        return

    def Collect(self):
        return


class Coolwater(Utility):

    def __init__(self):
        self.duty = []
        self.usage = []

    def Collect(self, block):
        self.duty = block.Output.UTIL_DUTY.Value
        self.usage = block.Output.UTL_USAGE.Value


class HP_Steam(Utility):

    def __init__(self):
        self.duty = []
        self.usage = []

    def Collect(self, block):
        self.duty = block.Output.UTIL_DUTY.Value
        self.usage = block.Output.UTL_USAGE.Value


class MP_Steam(Utility):

    def __init__(self):
        self.duty = []
        self.usage = []

    def Collect(self, block):
        self.duty = block.Output.UTIL_DUTY.Value
        self.usage = block.Output.UTL_USAGE.Value


class LP_Steam(Utility):

    def __init__(self):
        self.duty = []
        self.usage = []

    def Collect(self, block):
        self.duty = block.Output.UTIL_DUTY.Value
        self.usage = block.Output.UTL_USAGE.Value


class Refrigerant(Utility):

    def __init__(self):
        self.duty = []
        self.usage = []

