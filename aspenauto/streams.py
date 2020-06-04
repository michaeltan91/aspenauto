from .objectcollection import ObjectCollection
from .baseobject import BaseObject
import weakref

class Stream(BaseObject):

    def __init__(self, stream, aspen, path, uid):
        
        if 'F-' in stream.Name:
            obj_type = 'Feed'
        elif 'P-' in stream.Name:
            obj_type = 'Product'
        elif 'W-' in stream.Name:
            obj_type = 'Waste'
        else:
            obj_type = 'Standard'
        self.type = obj_type
        self.name = stream.Name
        self.uid = uid 
        self.base_path = path
        super().__init__(aspen)


    def get_obj_value(self, prop_loc):    
        path = self.base_path+str(self.name)+prop_loc
        return self.aspen.Tree.FindNode(path).Value

    def get_obj_value_frac(self, prop_loc):
        path = self.base_path+str(self.name)+prop_loc
        temp = ObjectCollection()
        for element in self.aspen.Tree.FindNode(path).Elements:
            temp[element.Name] = element.Value 
        return temp

    def set_obj_value(self, prop_loc, value):
        path = self.base_path+str(self.name)+prop_loc[0]
        if self.aspen.Tree.FindNode(path).AttributeValue(13) is not prop_loc[1]:
            self.aspen.Tree.FindNode(path).SetAttributeValue(13,0,prop_loc[1])
        self.aspen.Tree.FindNode(path).Value = value
        return

    def set_obj_value_frac(self):

        return

    

        
class Material(Stream):

    stream_type = 'Material'

    properties_in = {
        'pressure': ['\\Input\\PRES\\MIXED',],
        'temperature': ['\\Input\\TEMP\\MIXED',],
        'massflow': ['\\Input\\TOTFLOW\\MIXED', 'MASS'],
        'moleflow': ['\\Input\\TOTFLOW\\MIXED', 'MOLE'],
        'volflow': ['\\Input\\TOTFLOW\\MIXED', 'VOLUME']
    }
    properties_frac_in = {
        'massfrac' : '\\Input\\FLOW\\MIXED',
        'molefrac' : '\\Input\\FLOW\\MIXED'
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

    stream_type = 'Work'

    properties_in = {}
    properties_frac_in = {}

    properties_out = {
        'power': '\\Output\\POWER_OUT',
        'speed': '\\Output\\SPEED_OUT'
    }
    properties_frac_out = {}


class Heat(Stream):

    stream_type = 'Heat'

    properties_in = {}
    properties_frac_in = {}

    properties_out = {'Q': '\\Output\\QCALC'}
    properties_frac_out = {}
    
        