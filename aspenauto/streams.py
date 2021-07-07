from .objectcollection import ObjectCollection
from .baseobject import BaseObject
from collections import Counter

class Stream(BaseObject):
    """Main stream class"""
    # The different aspen stream properties are stored in several property dictionaries per stream type subclass.
    # In each dictionary, the aspen stream property is the key of the dictionary while part of the storage location in the COM interface 
    # is the respective value
    # Aspen Plus has different storage locations for the stream input and output, thus requiring separate input and output property dictionaries
    # Additionally, there are separate dictionaries for fractional properties such as massfrac and molefrac

    # Any new stream properties can be added to existing stream subclasses by using the same format

    def __init__(self, name, uid, process):
        
        # Assign feed, product, waste and standard stream tags
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


    def get_obj_value(self, key, prop_loc):    
        return self.process().asp.get_stream_value(self.uid, prop_loc)

    def get_obj_value_frac(self, key, prop_loc):
        return self.process().asp.get_stream_value_frac(self.uid, prop_loc)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_stream_value(self.uid, prop_loc, value)

    def set_obj_value_frac(self, prop_loc, value):
        self.process().asp.set_stream_value_frac(self.uid, prop_loc, value)


        
class Material(Stream):
    """Aspen Plus Material stream subclass"""

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
        'molefrac' : ['\\Input\\FLOW\\MIXED','MOLE-FRAC'],
        'massflow_comp' : ['\\Input\\FLOW\\MIXED','MASS-FLOW']
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
    
    """Aspen Plus Work stream subclass"""

    stream_type = 'Work'

    properties_in = {}
    properties_frac_in = {}

    properties = {
        'power': '\\Output\\POWER_OUT',
        'speed': '\\Output\\SPEED_OUT'
    }
    properties_frac = {}


class Heat(Stream):
    """Aspen Plus Heat stream subclass"""

    stream_type = 'Heat'

    properties_in = {}
    properties_frac_in = {}

    properties = {'duty': '\\Output\\QCALC'}
    properties_frac = {}




class Stream_Special(BaseObject):
    """Main special stream class for nonconventional material streams"""
    # The different aspen stream properties are stored in several property dictionaries per stream type subclass.
    # In each dictionary, the aspen stream property is the key of the dictionary while part of the storage location in the COM interface 
    # is the respective value
    # Aspen Plus has different storage locations for the stream input and output, thus requiring separate input and output property dictionaries
    # Additionally, there are separate dictionaries for fractional properties such as massfrac and molefrac

    # Any new stream properties can be added to existing stream subclasses by using the same format

    def __init__(self, name, uid, process):
        
        # Assign feed, product, waste and standard stream tags
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


    def get_obj_value(self, key, prop_loc):

        y = self.process().asp.get_stream_special_value(self.uid, prop_loc)
        y.pop('$TOTAL')
        
        if key == 'massflow' or key == 'moleflow' or key == 'volflow':
            return sum(y.values())

        else:
            return max(y.values())
        

    def get_obj_value_frac(self, prop, prop_loc):
        
        temp = self.process().asp.get_stream_special_value_frac(self.uid, prop_loc)
        temp.pop('$TOTAL')
        removal = []
        total_flow = 0

        for key, value in temp.items():
            try:
                flow = self.process().asp.get_stream_special_flow(self.uid, self.solids[prop], key)
                value.update((x, y*flow) for x, y in value.items())
                total_flow += flow
            except TypeError:
                removal.append(key)
                pass
        for key in removal:
            temp.pop(key)

        a = Counter()
        for b in temp:
            a += Counter(b)

        for key, value in a.items():
            a[key] = value/total_flow

        return ObjectCollection(a)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_stream_value(self.uid, prop_loc, value)

    def set_obj_value_frac(self, prop_loc, value):
        self.process().asp.set_stream_value_frac(self.uid, prop_loc, value)


class Material_MIXCISLD(Stream_Special):
    """Aspen Plus MIXCISLD Material stream class"""
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
        'molefrac' : ['\\Input\\FLOW\\MIXED','MOLE-FRAC'],
        'massflow_comp' : ['\\Input\\FLOW\\MIXED','MASS-FLOW']
    }

    properties = {
        'massflow': '\\Output\\MASSFLMX',
        'moleflow': '\\Output\\MOLEFLMX',
        'volflow': '\\Output\\VOLFLMX',
        'pressure': '\\Output\\PRES_OUT',
        'temperature': '\\Output\\TEMP_OUT'
    }

    properties_frac = {
        'massfrac': '\\Output\\MASSFRAC',
        'molefrac': '\\Output\\MOLEFRAC'
    }

    solids = {
        'massfrac': '\\Output\\MASSFLMX\\',
        'molefrac': '\\Output\\MOLEFLMX\\'
    }


class Material_MCINCPSD(Stream_Special):
    
    """Aspen Plus MCINCPSD Material stream class"""
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
        'molefrac' : ['\\Input\\FLOW\\MIXED','MOLE-FRAC'],
        'massflow_comp' : ['\\Input\\FLOW\\MIXED','MASS-FLOW']
    }

    properties = {
        'massflow': '\\Output\\MASSFLMX',
        'moleflow': '\\Output\\MOLEFLMX',
        'volflow': '\\Output\\VOLFLMX',
        'pressure': '\\Output\\PRES_OUT',
        'temperature': '\\Output\\TEMP_OUT'
    }

    properties_frac = {
        'massfrac': '\\Output\\MASSFRAC',
        'molefrac': '\\Output\\MOLEFRAC'
    }

    solids = {
        'massfrac': '\\Output\\MASSFLMX\\',
        'molefrac': '\\Output\\MOLEFLMX\\'
    }


class Material_MIXCIPSD(Stream_Special):
    """Aspen Plus MIXCIPSD Material stream class"""
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
        'molefrac' : ['\\Input\\FLOW\\MIXED','MOLE-FRAC'],
        'massflow_comp' : ['\\Input\\FLOW\\MIXED','MASS-FLOW']
    }

    properties = {
        'massflow': '\\Output\\MASSFLMX',
        'moleflow': '\\Output\\MOLEFLMX',
        'volflow': '\\Output\\VOLFLMX',
        'pressure': '\\Output\\PRES_OUT',
        'temperature': '\\Output\\TEMP_OUT'
    }

    properties_frac = {
        'massfrac': '\\Output\\MASSFRAC',
        'molefrac': '\\Output\\MOLEFRAC'
    }

    solids = {
        'massfrac': '\\Output\\MASSFLMX\\',
        'molefrac': '\\Output\\MOLEFLMX\\'
    }