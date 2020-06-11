from .objectcollection import ObjectCollection
from .baseobject import BaseObject

class Block(object):

    def __init__(self, block_type, name, uid):
        self.name = name
        self.type = block_type
        self.uid = uid
        self.to_stream = None
        self.from_stream = None

    def get_obj_value(self):

        return

    def set_obj_value(self):

        return


class MixSplit(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}
        
        
class Separator(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}
        

class Exchanger(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}
        

class Column(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}


class Reactor(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}


class Pressure(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}


class Solids(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}


class SolidsSeparator(Block):

    properties_in = {}
    properties_frac_in = {}
    properties_out = {}
    properties_frac_out = {}