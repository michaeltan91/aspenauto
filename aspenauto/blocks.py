"""Contains the block class and its respective subclasses"""
from .baseobject import BaseObject

class Block(BaseObject):
    """Main block class"""
    # The different aspen block properties are stored in several property dictionaries per
    # block type subclass. In each dictionary, the aspen block property is the key of the
    # dictionary while part of the storage location in the COM interface is the respective value.
    # Aspen Plus has different storage locations for the block input and output, thus requiring
    # separate input and output property dictionaries. Additionally, there are separate
    # dictionaries for fractional properties.

    # Any new block properties can be added to existing block subclasses by using the same format

    def __init__(self, block_type, name, uid, process):
        self.name = name
        self.block_type = block_type
        self.uid = uid
        self.to_stream = None
        self.from_stream = None
        super().__init__(process)

    def get_obj_value(self, key, prop_loc):
        return self.process().asp.get_block_value(self.uid, prop_loc)

    def get_obj_value_frac(self, key, prop_loc):
        return self.process().asp.get_block_value_frac(self.uid, prop_loc)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_block_value(self.uid, prop_loc, value)

    def set_obj_value_frac(self, prop_loc, value):
        return


class Compr(Block):
    """Aspen Plus Compr block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME',
        'model': '\\Input\\MODEL_TYPE',
        'outlet_spec': '\\Input\\OPT_SPEC',
        'pressure': '\\Input\\PRES',
        'pressure_increase': '\\Input\\DELP',
        'type' : '\\Input\\TYPE'
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'pressure': '\\Output\\POC',
        'pressure_increase': '\\Output\\DELP_CAL',
        'utility': '\\Output\\UTL_ID',
        'utility_duty': '\\Output\\UTL_DUTY',
        'utility_usage': '\\Output\\UTL_USAGE'
        }
    properties_frac = {}


class MCompr(Block):
    """Aspen Plus MCompr block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME',
        'model':'\\Input\\TYPE',
        'outlet_spec': '\\Input\\OPT_SPEC',
        'pressure': '\\Input\\PRES',
        'stages': '\\Input\\NSTAGE',
        'type': '\\Input\\TYPE_STG'
        }
    properties_frac_in = {
        'cooler_spec': '\\Input\\OPT_CLSPEC',
        'cooler_duty': '\\Input\\DUTY',
        'cooler_temperature': '\\Input\\CL_TEMP'
    }
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        }
    properties_frac = {
        'cooler_temperature': '\\Output\\COOL_TEMP'
        }


class Pump(Block):
    """Aspen Plus Pump block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME',
        'model': '\\Input\\PUMP_TYPE',
        'outlet_spec': '\\Input\\OPT_SPEC',
        'pressure': ['\\Input\\PRES', None],
        'pressure_increase': '\\Input\\DELP'
        }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'pressure': '\\Output\\POC',
        'pressure_increase': '\\Output\\DELP_CAL',
        'utility': '\\Output\\UTL_ID',
        'utility_duty': '\\Output\\UTL_DUTY',
        'utility_usage': '\\Output\\UTL_USAGE'
    }
    properties_frac = {}




class Mixer(Block):
    """Aspen Plus Mixer block class"""
    properties_in = {'block_method': '\\Input\\OPSETNAME'}
    properties_frac_in = {}
    properties = {'block_method': '\\Input\\OPSETNAME'}
    properties_frac = {}


class Fsplit(Block):
    """Aspen Plus Fsplit block class"""
    properties_in = {'block_method': '\\Input\\OPSETNAME'}
    properties_frac_in = {
        '\\Input\\FRAC'
    }
    properties = {'block_method': '\\Input\\OPSETNAME'}
    properties_frac = {
        '\\Input\\FRAC'
    }



class Flash2(Block):
    """Aspen Plus Flash2 block class"""
    properties_in = {
        'block_method': ['\\Input\\OPSETNAME', None],
        'duty': ['\\Input\\DUTY', None],
        'pressure': ['\\Input\\PRES', None],
        'temperature': ['\\Input\\TEMP', None]
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'pressure': '\\Output\\B_PRES',
        'temperature': '\\Output\\B_TEMP'
    }
    properties_frac = {}


class Flash3(Block):
    """Aspen Plus Flash3 block class"""
    properties_in = {
        'block_method': ['\\Input\\OPSETNAME', None],
        'duty': ['\\Input\\DUTY', None],
        'pressure': ['\\Input\\PRES', None],
        'temperature': ['\\Input\\TEMP', None],
        'vfrac': ['\\Input\\VFRAC', None]
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'pressure': '\\Output\\B_PRES',
        'temperature': '\\Output\\B_TEMP',
        'vfrac': '\\Output\\B_VFRAC'
    }
    properties_frac = {}


class Decanter(Block):
    """Aspen Plus Decanter block class"""
    properties_in = {
        'block_method': ['\\Input\\OPSETNAME', None],
        'duty': ['\\Input\\DUTY', None],
        'pressure': ['\\Input\\PRES', None],
        'temperature': ['\\Input\\TEMP', None]
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'pressure': '\\Output\\B_PRES',
        'temperature': '\\Output\\B_TEMP'
    }
    properties_frac = {}


class Separator1(Block):
    """Aspen Plus Separator1 block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac = {}



class Heater(Block):
    """Aspen Plus Heater block class"""
    properties_in = {
        'block_method': ['\\Input\\OPSETNAME', None],
        'flash_spec': ['\\Input_SPEC_OPT', None] ,
        'pressure': ['\\Input\\PRES', None],
        'temperature': ['\\Input\\TEMP', None]
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'pressure': '\\Output\\B_PRES',
        'temperature': '\\Output\\B_TEMP',
        'utility': '\\Output\\UTL_ID',
        'utility_duty': '\\Output\\UTIL_DUTY',
        'utility_usage': '\\Output\\UTL_USAGE',
        'vfrac': '\\Output\\B_VFRAC'
    }
    properties_frac = {}


class HeatX(Block):
    """Aspen Plus HeatX block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME',
        'spec': '\\Input\\SPEC',
        'temperature': '\\Input\\VALUE'
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'duty': '\\Output\\HX_DUTY',
        'spec': '\\Input\\SPEC',
        'pressure_cold_in': '\\Output\\COLDINP',
        'pressure_cold_out': '\\Output\\COLD_PRES',
        'pressure_hot_in': '\\Output\\HOTINP',
        'pressure_hot_out': '\\Output\\HOT_PRES',
        'temperature_cold_in': '\\Ouput\\COLDINT',
        'temperature_cold_out': '\\Output\\COLD_TEMP',
        'temperature_hot_in': '\\Output\\HOTINT',
        'temperature_hot_out': '\\Output\\HOT_TEMP',
        'temperature_set': '\\Input\\VALUE'
    }
    properties_frac = {}



class RadFrac(Block):
    """Aspen Plus RadFrac block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME',
        'condenser': '\\Input\\CONDENSER',
        'pressure_top': '\\Input\\PRES1',
        'reboiler': '\\Input\\REBOILER',
        'reflux_ratio': '\\Input\\BASIS_RR',
        'stages': '\\Input\\NSTAGE'
    }
    properties_frac_in = {
        'feed_stage': '\\Input\\FEED_STAGE'
    }
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'condenser': '\\Input\\CONDENSER',
        'condenser_utility': '\\Output\\COND_UTIL',
        'condenser_duty': '\\Output\\COND_DUTY',
        'condenser_usage': '\\Output\\COND_USAGE',
        'reboiler': '\\Input\\REBOILER',
        'reboiler_utility': '\\Output\\REB_UTIL',
        'reboiler_duty': '\\Output\\REB_DUTY',
        'reboiler_usage': '\\Output\\REB_USAGE',
        'mole_DFR': '\\Output\\DFR',
        'mole_RR': '\\Output\\MOLE_RR',
        'pressure_top': '\\Output\\PRES1',
        'stages': '\\Input\\NSTAGE'
    }
    properties_frac = {
        'feed_stage': '\\Input\\FEED_STAGE'
    }



class RGibbs(Block):
    """Aspen Plus RGibbs block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac_in = {
        'inerts': '\\Input\\FRAC'
    }
    properties = {
        'block_method': '\\Input\\OPSETNAME',
        'pressure': '\\Output\\B_PRES',
        'temperature': '\\Output\\B_TEMP',
        'vfrac': '\\Output\\B_VFRAC',
        'utility': '\\Output\\UTL_ID',
        'utility_duty': '\\Output\\UTL_DUTY',
        'utility_usage': '\\Output\\UTL_USAGE'
    }
    properties_frac = {
        'inerts': '\\Input\\FRAC'
    }


class RPlug(Block):
    """Aspen Plus Rplug block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac = {}


class RStoic(Block):
    """Aspen Plus RStoic block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac = {}


class RYield(Block):
    """Aspen Plus RYield block class"""
    properties_in = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac_in = {}
    properties = {
        'block_method': '\\Input\\OPSETNAME'
    }
    properties_frac = {}
