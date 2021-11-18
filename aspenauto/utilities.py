'''Contains the Utility class and its subclasses, the UtilityBlock class and its subclasses'''
from epynet import ObjectCollection
from .baseobject import BaseObject

class Utility(BaseObject):
    '''Main utility class'''
    # The different aspen utility properties are stored in several property dictionaries
    # per utility type subclass. In each dictionary, the aspen utility property is the key
    # of the dictionary while part of the storage location in the COM interface is
    # the respective value. Aspen Plus has different storage locations for
    # the utility input and output, thus requiring separate input and output property dictionaries
    # Additionally, there are separate dictionaries for fractional properties.

    # Any new block properties can be added to existing stream subclasses by using the same format
    def __init__(self, util_name, process):
        self.name = util_name # Name is name set by user in Aspen Plus
        self.blocks = ObjectCollection()
        super().__init__(process)

    def get_obj_value(self, key, prop_loc):
        return self.process().asp.get_util_value(self.name, prop_loc)

    def get_obj_value_frac(self, key, prop_loc):
        return

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_util_value(self.name, prop_loc, value)

    def set_obj_value_frac(self, prop_loc, value):
        return

class Electricity(Utility):
    '''Aspen Plus Electricity class'''
    properties_in = {}
    properties_frac_in = {}
    properties = {}
    properties_frac = {}


class Coolwater(Utility):
    '''Aspen Plus Cooling water class'''
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
    '''Aspen Plus Steam class'''
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


class SteamGen(Utility):
    '''Aspen Plus Steam generation class'''
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
    '''Aspen Plus Refrigerant class'''
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
    '''Aspen Plus Natural gas class'''
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


class UtilityBlock(BaseObject):
    '''Main Utility Block class'''
    # The different aspen utility block properties are stored in several property dictionaries
    # per utility block type subclass. In each dictionary, the aspen utility block property is
    # the key of the dictionary while part of the storage location in the COM interface
    # is the respective value. Aspen Plus has different storage locations for
    # the utility block input and output, thus requiring separate input and
    # output property dictionaries.
    # Additionally, there are separate dictionaries for fractional properties.

    # Any new utility block properties can be added to existing
    # stream subclasses by using the same format

    def __init__(self, util_name, uid, process):
        self.name = util_name # Name is name set by user in Aspen Plus
        self.uid = uid # Custom identifier, combination of name of flowsheet and name of block
        super().__init__(process)

    def get_obj_value(self, key, prop_loc):
        return self.process().asp.get_util_block_value(self.name, self.uid, prop_loc)

    def get_obj_value_frac(self, key, prop_loc):
        return

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_util_block_value(self.name, self.uid, prop_loc, value)

    def set_obj_value_frac(self, prop_loc, value):
        return


class ElectricityBlock(UtilityBlock):
    '''Aspen Plus Electricity utility per block class'''
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class CoolwaterBlock(UtilityBlock):
    '''Aspen Plus Cooling water utility per block class'''
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class SteamBlock(UtilityBlock):
    '''Aspen Plus Steam utility per block class'''
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class SteamGenBlock(UtilityBlock):
    '''Aspen Plus Steam generation utility per block class'''
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class RefrigerantBlock(UtilityBlock):
    '''Aspen Plus Refrigerant utility per block class'''
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}


class GasBlock(UtilityBlock):
    '''Aspen Plus Gas utility per block class'''
    properties_in = {}
    properties_frac_in = {}
    properties = {
        'duty': '\\Output\\UTL_DUTY\\',
        'usage':'\\Output\\UTL_USAGE\\',
    }
    properties_frac = {}
