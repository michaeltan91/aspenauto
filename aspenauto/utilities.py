

class Utility(object):

    def __init__(self):
        self.duty = []
        self.usage = []
        self.Tin = []
        self.Tout = []
        self.Pin = []
        self.Pout = []

class Electricity(Utility):

    def __init__(self):
        self.duty = []
        self.usage = []

    def Collect_Duty(self, param, block):
        self.duty = block.Value

    def Collect_Usage(self, block):
        self.usage = block.Value


class Coolwater(Utility):

    def Collect_Duty(self, param, block):
        self.duty = block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = block.Value


class HP_Steam(Utility):

    def Collect_Duty(self, param, block):
        self.duty = block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = block.Value

class HPS_Gen(Utility):

    def Collect_Duty(self, param, block):
        self.duty = -block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = -block.Value

class MP_Steam(Utility):

    def Collect_Duty(self, param, block):
        self.duty = block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = block.Value

class MPS_Gen(Utility):

    def Collect_Duty(self, param, block):
        self.duty = -block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = -block.Value

class LP_Steam(Utility):

    def Collect_Duty(self, param, block):
        self.duty = -block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = -block.Value

class LPS_Gen(Utility):

    def Collect_Duty(self, param, block):
        self.duty = block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = block.Value

class Refrigerant(Utility):

    def Collect_Duty(self, param, block):
        self.duty = block.Value
        self.Tin = param.Output.UTL_IN_TEMP.Value
        self.Tout = param.Output.UTL_OUT_TEMP.Value
        self.Pin = param.Output.UTL_IN_PRES.Value
        self.Pout = param.Output.UTL_OUT_PRES.Value

    def Collect_Usage(self, block):
        self.usage = block.Value

