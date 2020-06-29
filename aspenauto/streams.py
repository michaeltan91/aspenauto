from .objectcollection import ObjectCollection
from .baseobject import BaseObject
import weakref

class Stream(BaseObject):
    # Main stream class
    def __init__(self, name, uid, process):
        
        if 'F-' in name:
            obj_type = 'Feed'
        elif 'P-' in name:
            obj_type = 'Product'
        elif 'W-' in name:
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
        'volflow': ['\\Input\\TOTFLOW\\MIXED', 'VOLUME']
    }
    properties_frac_in = {
        'massfrac' : ['\\Input\\FLOW\\MIXED','MASS-FRAC'],
        'molefrac' : ['\\Input\\FLOW\\MIXED','MOLE-FRAC']
    }

    properties_out = {
        'pressure': '\\Output\\PRES_OUT\\MIXED',
        'temperature': '\\Output\\TEMP_OUT\\MIXED',
        'massflow': '\\Output\\MASSFLMX\\MIXED',
        'moleflow': '\\Output\\MOLEFLMX\\MIXED',
        'volflow': '\\Output\\VOLFLMX\\MIXED'
        }
    properties_frac_out = {
        'massfrac': '\\Output\\MASSFRAC\\MIXED',
        'molefrac': '\\Output\\MOLEFRAC\\MIXED'
    }


class Work(Stream):
    """Aspen Plus Work stream class"""

    stream_type = 'Work'

    properties_in = {}
    properties_frac_in = {}

    properties_out = {
        'power': '\\Output\\POWER_OUT',
        'speed': '\\Output\\SPEED_OUT'
    }
    properties_frac_out = {}


class Heat(Stream):
    """Aspen Plus Heat stream class"""

    stream_type = 'Heat'

    properties_in = {}
    properties_frac_in = {}

    properties_out = {'Q': '\\Output\\QCALC'}
    properties_frac_out = {}
    
        