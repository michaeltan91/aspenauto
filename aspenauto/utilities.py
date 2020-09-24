from .baseobject import BaseObject
from .objectcollection import ObjectCollection

class Utility(BaseObject):

    def __init__(self, util_name, process):
        self.name = util_name # Name is name set by user in Aspen Plus
        self.blocks = ObjectCollection()
        super().__init__(process)

    def get_obj_value(self, prop_loc):
        return self.process().asp.get_util_value(self.name, prop_loc)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_util_value(self.name, prop_loc, value)
        


class Electricity(Utility):
    properties_in = {}
    properties_frac_in = {}
    properties = {}   
    properties_frac = {}


class Coolwater(Utility):
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'temperature_in': '\\Output\\UTL_IN_TEMP\\',
        'temperature_out': '\\Output\\UTL_OUT_TEMP\\',
        'pressure_in': '\\Output\\UTL_IN_PRES\\',
        'pressure_out': '\\Output\\UTL_OUT_PRES\\',
        'vfrac_in': '\\Output\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\Output\\UTL_OUT_VFRAC\\'
    }
    properties_frac = {}


class Steam(Utility):
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'temperature_in': '\\Output\\UTL_IN_TEMP\\',
        'temperature_out': '\\Output\\UTL_OUT_TEMP\\',
        'pressure_in': '\\Output\\UTL_IN_PRES\\',
        'pressure_out': '\\Output\\UTL_OUT_PRES\\',
        'vfrac_in': '\\Output\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\Output\\UTL_OUT_VFRAC\\'
    }
    properties_frac = {}


class Steam_Gen(Utility):
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'temperature_in': '\\Output\\UTL_IN_TEMP\\',
        'temperature_out': '\\Output\\UTL_OUT_TEMP\\',
        'pressure_in': '\\Output\\UTL_IN_PRES\\',
        'pressure_out': '\\Output\\UTL_OUT_PRES\\',
        'vfrac_in': '\\Output\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\Output\\UTL_OUT_VFRAC\\'
    }
    properties_frac = {}


class Refrigerant(Utility):

    properties_in = {}
    properties_frac_in = {}
    properties = {
        'temperature_in': '\\Output\\UTL_IN_TEMP\\',
        'temperature_out': '\\Output\\UTL_OUT_TEMP\\',
        'pressure_in': '\\Output\\UTL_IN_PRES\\',
        'pressure_out': '\\Output\\UTL_OUT_PRES\\',
        'vfrac_in': '\\Output\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\Output\\UTL_OUT_VFRAC\\'
    }
    properties_frac = {}


class Gas(Utility):
    
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'temperature_in': '\\Output\\UTL_IN_TEMP\\',
        'temperature_out': '\\Output\\UTL_OUT_TEMP\\',
        'pressure_in': '\\Output\\UTL_IN_PRES\\',
        'pressure_out': '\\Output\\UTL_OUT_PRES\\',
        'vfrac_in': '\\Output\\UTL_IN_VFRAC\\',
        'vfrac_out': '\\Output\\UTL_OUT_VFRAC\\'
    }
    properties_frac = {}


class Utility_Block(BaseObject):

    def __init__(self, util_name, uid, process):
        self.name = util_name # Name is name set by user in Aspen Plus
        self.uid = uid # Custom identifier, combination of name of flowsheet and name of block 
        super().__init__(process)

    def get_obj_value(self, prop_loc):
        return self.process().asp.get_util_block_value(self.name, self.uid, prop_loc)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_util_block_value(self.name, self.uid, prop_loc, value)
        

class Electricity_Block(Utility_Block):
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }   
    properties_frac = {}


class Coolwater_Block(Utility_Block):
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class Steam_Block(Utility_Block):
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class Steam_Gen_Block(Utility_Block):
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}
    

class Refrigerant_Block(Utility_Block):

    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class Gas_Block(Utility_Block):
    
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}