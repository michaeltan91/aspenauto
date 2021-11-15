"""Contains the stream class and its respective subclasses"""
from collections import Counter
from epynet import ObjectCollection

from .baseobject import BaseObject

class Stream(BaseObject):
    """Main stream class"""
    # The different aspen stream properties are stored in several property dictionaries per
    # stream type subclass. In each dictionary, the aspen stream property is the key of
    # the dictionary while part of the storage location in the COM interface is the respective value
    # Aspen Plus has different storage locations for the stream input and output,
    # thus requiring separate input and output property dictionaries
    # Additionally, there are separate dictionaries for fractional properties such as massfrac
    # and molefrac

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




class StreamSpecial(BaseObject):
    """Main special stream class for nonconventional material streams"""
    # The different aspen stream properties are stored in several property dictionaries per
    # stream type subclass. In each dictionary, the aspen stream property is the key of the
    # dictionary while part of the storage location in the COM interface is the respective value
    # Aspen Plus has different storage locations for the stream input and output, thus requiring
    # separate input and output property dictionaries. Additionally, there are separate dictionaries
    # for fractional properties such as massfrac and molefrac

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

        temp = self.process().asp.get_stream_special_value(self.uid, prop_loc)
        temp.pop('$TOTAL')

        if key == 'massflow' or key == 'moleflow' or key == 'volflow':
            return sum(temp.values())

        else:
            return max(temp.values())


    def get_obj_value_frac(self, key, prop_loc):

        temp = self.process().asp.get_stream_special_value_frac(self.uid, prop_loc)
        temp.pop('$TOTAL')
        removal = []
        total_flow = 0

        for key_1, value in temp.items():
            try:
                flow = self.process().asp.get_stream_special_flow(self.uid, self.solids[key], key_1)
                value.update((x, y*flow) for x, y in value.items())
                total_flow += flow
            except TypeError:
                removal.append(key_1)
        for key_1 in removal:
            temp.pop(key_1)

        temp2 = Counter()
        for temp_var in temp:
            temp2 += Counter(temp_var)

        for key_1, value in temp2.items():
            temp2[key_1] = value/total_flow

        return ObjectCollection(temp2)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_stream_value(self.uid, prop_loc, value)

    def set_obj_value_frac(self, prop_loc, value):
        self.process().asp.set_stream_value_frac(self.uid, prop_loc, value)


class MaterialMIXCISLD(StreamSpecial):
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


class MaterialMCINCPSD(StreamSpecial):

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


class MaterialMIXCIPSD(StreamSpecial):
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
