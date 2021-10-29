"""Contains the baseobject class"""
import weakref

class BaseObject(object):
    """Base object class"""

    def __init__(self, process):
        self._values = {}
        self.process = weakref.ref(process)

    def reset(self):
        """Resets all retrieved class attribute values"""
        self._values = {}

    def get_obj_value(self, key, prop_loc):
        """Retrieve the object property value"""
        # Method called is in the grandchild class
        raise NotImplementedError

    def get_obj_value_frac(self, key, prop_loc):
        """Retrieve the object fractional property value"""
        # Method called is in the grandchild class
        raise NotImplementedError

    def set_obj_value(self, prop_loc, value):
        """Set the object property value"""
        # Method called is in the grandchild class
        raise NotImplementedError

    def set_obj_value_frac(self, prop_loc, value):
        """Set the object property fractional value"""
        # Method called is in the grandchild class
        raise NotImplementedError

    def __getattr__(self, key):
        # Called when the requested class attribute is not stored in the normal Python location,
        # checks whether the property is present in the class dictionaries "properties" and
        # "properties_frac"
        if key in self.properties.keys():
            return self.get_property(key)
        elif key in self.properties_frac.keys():
            return self.get_property_frac(key)
        else:
            raise AttributeError('Nonexistant Attribute', key)

    def __setattr__(self, key, value):
        # Called when a value of class attibute has to be assigned,
        # in that case the value is inserted in the Aspen Model and
        # not in the standard Python attribute storage location
        if key in self.properties_in.keys():
            self.set_property(key, value)
        elif key in self.properties_frac_in.keys():
            self.set_property_frac(key, value)
        else:
            super(BaseObject, self).__setattr__(key, value)

    def get_property(self, key):
        '''Method retrieving the property location in Aspen Plus'''
        if key not in self._values.keys():
            prop_loc = self.properties[key]
            self._values[key] = self.get_obj_value(key, prop_loc)
        return self._values[key]

    def get_property_frac(self, key):
        '''Method retrieving the fractional property location in Aspen Plus'''
        if key not in self._values.keys():
            prop_loc = self.properties_frac[key]
            self._values[key] = self.get_obj_value_frac(key, prop_loc)
        return self._values[key]

    def set_property(self, key, value):
        '''Method retrieving the property location in Aspen Plus,
        where the value has to be assigned to'''
        prop_loc = self.properties_in[key]
        self.set_obj_value(prop_loc, value)

    def set_property_frac(self, key, value):
        '''Method retrieving the fractional property location in Aspen Plus,
        where the values has to be assigned to '''
        prop_loc = self.properties_frac_in[key]
        self.set_obj_value_frac(prop_loc, value)
