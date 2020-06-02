import weakref
from .objectcollection import ObjectCollection 

class BaseObject(object):

    properties = {}
    properties_frac = {}

    def __init__(self, aspen):
        
        self._values = {}
        self.aspen = aspen
    
    def reset(self):
        self._values = {}

    def get_obj_value(self, object_loc):
        raise NotImplementedError

    def get_obj_value_frac(self, object_loc):
        raise NotImplementedError

    def set_obj_value(self, object_loc, value):
        raise NotImplementedError

    def set_obj_value_frac(self, object_loc, value):
        raise NotImplementedError

    def __getattr__(self, prop):

        if prop in self.properties_out.keys():
            return self.get_property(self.properties_out[prop])

        elif prop in self.properties_frac_out.keys():
            return self.get_property_frac(self.properties_frac_out[prop])

        else:
            raise AttributeError('Nonexistant Attribute', prop)
                

    def __setattr__(self, prop, value):

        if prop in self.properties_in.keys():
            self.set_property(self.properties[prop], value)

        else:
            super(BaseObject, self).__setattr__(prop, value)


    def get_property(self, obj_loc):
        if obj_loc not in self._values.keys():
            self._values[obj_loc] = self.get_obj_value(obj_loc)
        return self._values[obj_loc]

    def get_property_frac(self, obj_loc):
        if obj_loc not in self._values.keys():
            self._values[obj_loc] = self.get_obj_value_frac(obj_loc)
        return self._values[obj_loc]

    
    def set_property(self, obj_loc, value):
        self.set_obj_value(obj_loc, value)

