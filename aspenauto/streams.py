from .objectcollection import ObjectCollection
from .baseobject import BaseObject
import weakref

class Stream(BaseObject):
    # Main stream class
    def __init__(self, name, uid, path, process):
        
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
        self.base_path = path
        self.to_block = None
        self.from_block = None
        super().__init__(process)


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

    def set_obj_value_frac(self, prop_loc, val):
        path = self.base_path+str(self.name)+prop_loc[0]
        
        if self.aspen.Tree.FindNode(path).AttributeValue(13) is not prop_loc[1]:
            self.aspen.Tree.FindNode(path).SetAttributeValue(13,0,prop_loc[1])
        
        temp1 = {}
        temp2 = val
        for element in self.aspen.Tree.FindNode(path).Elements:
            temp1[element.Name] = element.Value 
        
        dict3 = {**temp1, **temp2}
        print(dict3)
        for key, value in dict3.items():
            if key in temp1 and key in temp2:
                dict3[key] = value
                self.aspen.Tree.FindNode(path+'\\'+key).Value = value
            elif key in temp1 and key not in temp2:
                dict3[key] = 0
                self.aspen.Tree.FindNode(path+'\\'+key).Value = value
            elif key not in temp1 and key in temp2:
                raise AttributeError('Component not defined in Aspen simulation', key)


        
class Material(Stream):
    # Material stream subclass

    stream_type = 'Material'

    properties_in = {
        'pressure': ['\\Input\\PRES\\MIXED',],
        'temperature': ['\\Input\\TEMP\\MIXED',],
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
    # Work stream subclass

    stream_type = 'Work'

    properties_in = {}
    properties_frac_in = {}

    properties_out = {
        'power': '\\Output\\POWER_OUT',
        'speed': '\\Output\\SPEED_OUT'
    }
    properties_frac_out = {}


class Heat(Stream):
    # Heat stream subclass

    stream_type = 'Heat'

    properties_in = {}
    properties_frac_in = {}

    properties_out = {'Q': '\\Output\\QCALC'}
    properties_frac_out = {}
    
        