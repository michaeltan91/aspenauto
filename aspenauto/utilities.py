from.baseobject import BaseObject

class Utility(BaseObject):

    def __init__(self, block_name, aspen):
        self.name = block_name
        super().__init__(aspen)

    def get_obj_value(self, obj_loc):
        path = '\\Data\\Utilities'+obj_loc+str(self.name) 
        return self.aspen.Tree.FindNode(path).Value

    def set_obj_value(self, obj_loc, value):
        path = '\\Data\\Streams\\'+str(self.name)+obj_loc
        self.aspen.Tree.FindNode(path).Value = value
        return 

class Electricity(Utility):
    properties_in = {}
    properties_out = {
        'duty': '\\ELECTRIC\\Output\\UTL_DUTY\\',
        'usage':'\\ELECTRIC\\Output\\UTL_USAGE\\',
    }   


class Coolwater(Utility):
    properties_in = {}
    properties_out = {
        'duty': '\\CW\\Output\\UTL_DUTY\\',
        'usage':'\\CW\\Output\\UTL_USAGE\\',
        'Tin': '\\CW\\UTL_IN_TEMP\\',
        'Tout': '\\CW\\UTL_OUT_TEMP\\',
        'Pin': '\\CW\\UTL_IN_PRES\\',
        'Pout': '\\CW\\UTL_OUT_PRES\\',
        'vfrac_in': '\\CW\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\CW\\UTL_OUT_VFRAC\\'
    }



class HP_Steam(Utility):
    properties_in = {}
    properties_out = {
        'duty': '\\HPS\\Output\\UTL_DUTY\\',
        'usage':'\\HPS\\Output\\UTL_USAGE\\',
        'Tin': '\\HPS\\UTL_IN_TEMP\\',
        'Tout': '\\HPS\\UTL_OUT_TEMP\\',
        'Pin': '\\HPS\\UTL_IN_PRES\\',
        'Pout': '\\HPS\\UTL_OUT_PRES\\',
        'vfrac_in': '\\HPS\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\HPS\\UTL_OUT_VFRAC\\'
    }


class HPS_Gen(Utility):
    properties_in = {}
    properties_out = {
        'duty': '\\HPS-GEN\\Output\\UTL_DUTY\\',
        'usage':'\\HPS-GEN\\Output\\UTL_USAGE\\',
        'Tin': '\\HPS-GEN\\UTL_IN_TEMP\\',
        'Tout': '\\HPS-GEN\\UTL_OUT_TEMP\\',
        'Pin': '\\HPS-GEN\\UTL_IN_PRES\\',
        'Pout': '\\HPS-GEN\\UTL_OUT_PRES\\',
        'vfrac_in': '\\HPS-GEN\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\HPS-GEN\\UTL_OUT_VFRAC\\'
    }


class MP_Steam(Utility):
    
    properties_in = {}
    properties_out = {
        'duty': '\\MPS\\Output\\UTL_DUTY\\',
        'usage':'\\MPS\\Output\\UTL_USAGE\\',
        'Tin': '\\MPS\\UTL_IN_TEMP\\',
        'Tout': '\\MPS\\UTL_OUT_TEMP\\',
        'Pin': '\\MPS\\UTL_IN_PRES\\',
        'Pout': '\\MPS\\UTL_OUT_PRES\\',
        'vfrac_in': '\\MPS\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\MPS\\UTL_OUT_VFRAC\\'
    }
    

class MPS_Gen(Utility):

    properties_in = {}
    properties_out = {
        'duty': '\\MPS-GEN\\Output\\UTL_DUTY\\',
        'usage':'\\MPS-GEN\\Output\\UTL_USAGE\\',
        'Tin': '\\MPS-GEN\\UTL_IN_TEMP\\',
        'Tout': '\\MPS-GEN\\UTL_OUT_TEMP\\',
        'Pin': '\\MPS-GEN\\UTL_IN_PRES\\',
        'Pout': '\\MPS-GEN\\UTL_OUT_PRES\\',
        'vfrac_in': '\\MPS-GEN\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\MPS-GEN\\UTL_OUT_VFRAC\\'
    }

    

class LP_Steam(Utility):

    properties_in = {}
    properties_out = {
        'duty': '\\LPS\\Output\\UTL_DUTY\\',
        'usage':'\\LPS\\Output\\UTL_USAGE\\',
        'Tin': '\\LPS\\UTL_IN_TEMP\\',
        'Tout': '\\LPS\\UTL_OUT_TEMP\\',
        'Pin': '\\LPS\\UTL_IN_PRES\\',
        'Pout': '\\LPS\\UTL_OUT_PRES\\',
        'vfrac_in': '\\LPS\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\LPS\\UTL_OUT_VFRAC\\'
    }


class LPS_Gen(Utility):

    properties_in = {}
    properties_out = {
        'duty': '\\LPS-GEN\\Output\\UTL_DUTY\\',
        'usage':'\\LPS-GEN\\Output\\UTL_USAGE\\',
        'Tin': '\\LPS-GEN\\UTL_IN_TEMP\\',
        'Tout': '\\LPS-GEN\\UTL_OUT_TEMP\\',
        'Pin': '\\LPS-GEN\\UTL_IN_PRES\\',
        'Pout': '\\LPS-GEN\\UTL_OUT_PRES\\',
        'vfrac_in': '\\LPS-GEN\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\LPS-GEN\\UTL_OUT_VFRAC\\'
    }


class Refrigerant(Utility):

    properties_in = {}
    properties_out = {
        'duty': '\\RF\\Output\\UTL_DUTY\\',
        'usage':'\\RF\\Output\\UTL_USAGE\\',
        'Tin': '\\RF\\UTL_IN_TEMP\\',
        'Tout': '\\RF\\UTL_OUT_TEMP\\',
        'Pin': '\\RF\\UTL_IN_PRES\\',
        'Pout': '\\RF\\UTL_OUT_PRES\\',
        'vfrac_in': '\\RF\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\RF\\UTL_OUT_VFRAC\\'
    }


