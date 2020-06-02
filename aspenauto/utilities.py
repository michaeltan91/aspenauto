from.baseobject import BaseObject

class Utility(BaseObject):

    def __init__(self, block_name, aspen):
        self.name = block_name
        super().__init__(aspen)

    def get_obj_value(self, obj_loc):    
        return self.aspen.Tree.FindNode('\\Data\\Utilities'+obj_loc+str(self.name)).Value

    def set_obj_value(self, obj_loc, value):
        path = '\\Data\\Streams\\'+str(self.name)+obj_loc
        self.aspen.Tree.FindNode(path).Value = value
        return 

class Electricity(Utility):

    properties_out = {
        'duty': '\\ELECTRIC\\Output\\UTL_DUTY\\',
        'usage':'\\ELECTRIC\\Output\\UTL_USAGE\\',
    }   


class Coolwater(Utility):
    
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

    properties_out = {
        'duty': '\\HP-STEAM\\Output\\UTL_DUTY\\',
        'usage':'\\HP-STEAM\\Output\\UTL_USAGE\\',
        'Tin': '\\HP-STEAM\\UTL_IN_TEMP\\',
        'Tout': '\\HP-STEAM\\UTL_OUT_TEMP\\',
        'Pin': '\\HP-STEAM\\UTL_IN_PRES\\',
        'Pout': '\\HP-STEAM\\UTL_OUT_PRES\\',
        'vfrac_in': '\\HP-STEAM\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\HP-STEAM\\UTL_OUT_VFRAC\\'
    }


class HPS_Gen(Utility):
    
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

    properties_out = {
        'duty': '\\MP-STEAM\\Output\\UTL_DUTY\\',
        'usage':'\\MP-STEAM\\Output\\UTL_USAGE\\',
        'Tin': '\\MP-STEAM\\UTL_IN_TEMP\\',
        'Tout': '\\MP-STEAM\\UTL_OUT_TEMP\\',
        'Pin': '\\MP-STEAM\\UTL_IN_PRES\\',
        'Pout': '\\MP-STEAM\\UTL_OUT_PRES\\',
        'vfrac_in': '\\MP-STEAM\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\MP-STEAM\\UTL_OUT_VFRAC\\'
    }
    

class MPS_Gen(Utility):

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

    properties_out = {
        'duty': '\\LP-STEAM\\Output\\UTL_DUTY\\',
        'usage':'\\LP-STEAM\\Output\\UTL_USAGE\\',
        'Tin': '\\LP-STEAM\\UTL_IN_TEMP\\',
        'Tout': '\\LP-STEAM\\UTL_OUT_TEMP\\',
        'Pin': '\\LP-STEAM\\UTL_IN_PRES\\',
        'Pout': '\\LP-STEAM\\UTL_OUT_PRES\\',
        'vfrac_in': '\\LP-STEAM\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\LP-STEAM\\UTL_OUT_VFRAC\\'
    }


class LPS_Gen(Utility):

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

    properties_out = {
        'duty': '\\REFRIG\\Output\\UTL_DUTY\\',
        'usage':'\\REFRIG\\Output\\UTL_USAGE\\',
        'Tin': '\\REFRIG\\UTL_IN_TEMP\\',
        'Tout': '\\REFRIG\\UTL_OUT_TEMP\\',
        'Pin': '\\REFRIG\\UTL_IN_PRES\\',
        'Pout': '\\REFRIG\\UTL_OUT_PRES\\',
        'vfrac_in': '\\REFRIG\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\REFRIG\\UTL_OUT_VFRAC\\'
    }


