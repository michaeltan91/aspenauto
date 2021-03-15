import weakref
from .objectcollection import ObjectCollection 

class BaseObject(object):
    """Base object"""

    def __init__(self, process):
        
        self._values = {}
        self.process = weakref.ref(process)

    def reset(self):
        """Resets all retrieved class attribute values"""
        self._values = {}

    def get_obj_value(self, prop_loc):
        raise NotImplementedError

    def get_obj_value_frac(self, prop_loc):
        raise NotImplementedError

    def set_obj_value(self, prop_loc, value):
        raise NotImplementedError

    def set_obj_value_frac(self, prop_loc, value):
        raise NotImplementedError

    def __getattr__(self, key):
        if key in self.properties.keys():
            return self.get_property(key)
        elif key in self.properties_frac.keys():
            return self.get_property_frac(key)
        else:
            raise AttributeError('Nonexistant Attribute', key)
                
    def __setattr__(self, key, value):
        if key in self.properties_in.keys():
            self.set_property(key, value)
        elif key in self.properties_frac_in.keys():
            self.set_property_frac(key, value)
        else:
            super(BaseObject, self).__setattr__(key, value)

    def get_property(self, key):
        if key not in self._values.keys():
            prop_loc = self.properties[key]
            self._values[key] = self.get_obj_value(prop_loc)
        return self._values[key]

    def get_property_frac(self, key):
        if key not in self._values.keys():
            prop_loc = self.properties_frac[key]
            self._values[key] = self.get_obj_value_frac(prop_loc)
        return self._values[key]

    def set_property(self, key, value):
        prop_loc = self.properties_in[key]
        self.set_obj_value(prop_loc, value)

    def set_property_frac(self, key, value):
        prop_loc = self.properties_frac_in[key]
        self.set_obj_value_frac(prop_loc, value)

    