from .objectcollection import ObjectCollection
from .baseobject import BaseObject

class Stream(BaseObject):
    # Main stream class
    def __init__(self, name, uid, process):
        
        if 'FS-' in name:
            obj_type = 'Feed'
        elif 'PS-' in name:
            obj_type = 'Product'
        elif 'WS-' in name:
            obj_type = 'Waste'
        else:
            obj_type = 'Standard'
        self.type = obj_type
        self.name = name
        self.uid = uid 
        self.to_block = None
        self.from_block = None
        super().__init__(process)


    def get_obj_value(self, prop_loc):    
        return self.process().asp.get_stream_value(self.uid, prop_loc)

    def get_obj_value_frac(self, prop_loc):
        return self.process().asp.get_stream_value_frac(self.uid, prop_loc)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_stream_value(self.uid, prop_loc, value)

    def set_obj_value_frac(self, prop_loc, value):
        self.process().asp.set_stream_value_frac(self.uid, prop_loc, value)


        
class Material(Stream):
    """Aspen Plus Material stream class"""

    stream_type = 'Material'

    properties_in = {
        'pressure': ['\\Input\\PRES\\MIXED',None],
        'temperature': ['\\Input\\TEMP\\MIXED',None],
        'massflow': ['\\Input\\TOTFLOW\\MIXED', 'MASS'],
        'moleflow': ['\\Input\\TOTFLOW\\MIXED', 'MOLE'],
        'volflow': ['\\Input\\TOTFLOW\\MIXED', 'VOLUME'],
        'vfrac': ['\\Input\\VFRAC\\MIXED',None]
    }
    properties_frac_in = {
        'massfrac' : ['\\Input\\FLOW\\MIXED','MASS-FRAC'],
        'molefrac' : ['\\Input\\FLOW\\MIXED','MOLE-FRAC']
    }
    properties = {
        'pressure': '\\Output\\PRES_OUT\\MIXED',
        'temperature': '\\Output\\TEMP_OUT\\MIXED',
        'massflow': '\\Output\\MASSFLMX\\MIXED',
        'moleflow': '\\Output\\MOLEFLMX\\MIXED',
        'volflow': '\\Output\\VOLFLMX\\MIXED',
        'vfrac': '\\Output\\VFRAC_OUT\\MIXED'
        }
    properties_frac = {
        'massfrac': '\\Output\\MASSFRAC\\MIXED',
        'molefrac': '\\Output\\MOLEFRAC\\MIXED'
    }


class Work(Stream):
    """Aspen Plus Work stream class"""

    stream_type = 'Work'

    properties_in = {}
    properties_frac_in = {}

    properties = {
        'power': '\\Output\\POWER_OUT',
        'speed': '\\Output\\SPEED_OUT'
    }
    properties_frac = {}


class Heat(Stream):
    """Aspen Plus Heat stream class"""

    stream_type = 'Heat'

    properties_in = {}
    properties_frac_in = {}

    properties = {'duty': '\\Output\\QCALC'}
    properties_frac = {}