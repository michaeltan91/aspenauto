import weakref
from .objectcollection import ObjectCollection 

class BaseObject(object):

    def __init__(self, process):
        
        self._values = {}
        self.process = weakref.ref(process)

    def reset(self):
        self._values = {}

    def get_obj_value(self, prop_loc):
        raise NotImplementedError

    def get_obj_value_frac(self, prop_loc):
        raise NotImplementedError

    def set_obj_value(self, prop_loc, value):
        raise NotImplementedError

    def set_obj_value_frac(self, prop_loc, value):
        raise NotImplementedError

    def __getattr__(self, prop):
        if prop in self.properties.keys():
            #return self.get_property(self.properties[prop])
            return self.get_property(prop)
        elif prop in self.properties_frac.keys():
            #return self.get_property_frac(self.properties_frac[prop])
            return self.get_property_frac(prop)

        else:
            raise AttributeError('Nonexistant Attribute', prop)
                
    def __setattr__(self, prop, value):
        if prop in self.properties_in.keys():
            #self.set_property(self.properties_in[prop], value)
            self.set_property(prop, value)
        elif prop in self.properties_frac_in.keys():
            #self.set_property_frac(self.properties_frac_in[prop], value)
            self.set_property_frac(prop, value)
        else:
            super(BaseObject, self).__setattr__(prop, value)

    def get_property(self, prop):
        if prop not in self._values.keys():
            prop_loc = self.properties[prop]
            self._values[prop] = self.get_obj_value(prop_loc)
        return self._values[prop]

    def get_property_frac(self, prop):
        if prop not in self._values.keys():
            prop_loc = self.properties_frac[prop]
            self._values[prop] = self.get_obj_value_frac(prop_loc)
        return self._values[prop]

    def set_property(self, prop, value):
        prop_loc = self.properties_in[prop]
        self.set_obj_value(prop_loc, value)

    def set_property_frac(self, prop, value):
        prop_loc = self.properties_frac_in[prop]
        self.set_obj_value_frac(prop_loc, value)

    