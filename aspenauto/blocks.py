from .objectcollection import ObjectCollection
from .baseobject import BaseObject

class Block(BaseObject):

    def __init__(self, block_type, name, uid, process):
        self.name = name
        self.type = block_type
        self.uid = uid
        self.to_stream = None
        self.from_stream = None
        super().__init__(process)

    def get_obj_value(self, prop_loc):
        return self.process().get_block_value(self.uid, prop_loc)

    def set_obj_value(self, prop_loc, value):
        self.process().asp.set_block_value(self.uid, prop_loc, value)


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




class Heater(Block):

    properties_in = {}
    '''
    Input
    pressure:  Application.Tree.FindNode("\Data\Blocks\E-105\Input\PRES")
    temperature: Application.Tree.FindNode("\Data\Blocks\E-105\Input\TEMP")
    flash specifications    Application.Tree.FindNode("\Data\Blocks\E-107\Input\SPEC_OPT")

    '''

    '''
    Output
    pressure    Application.Tree.FindNode("\Data\Blocks\E-106\Output\B_PRES")
    temperature Application.Tree.FindNode("\Data\Blocks\E-106\Output\B_TEMP")
    vaporfrac   Application.Tree.FindNode("\Data\Blocks\E-106\Output\B_VFRAC")

    util duty   Application.Tree.FindNode("\Data\Blocks\E-106\Output\\UTIL_DUTY")
    util usage  Application.Tree.FindNode("\Data\Blocks\E-106\Output\\UTL_USAGE")
    util id     Application.Tree.FindNode("\Data\Blocks\E-106\Output\\UTL_ID")
    '''

class HeatX(Block):

    properties_in = {}


    '''
    Input
    Model fidelity: (Shortcut)    Application.Tree.FindNode("\Data\Blocks\E-104\Input\MODE")
    Calculation mode: (Design)   Application.Tree.FindNode("\Data\Blocks\E-104\Input\MODE0")
    Calculation mode: (Design)   Application.Tree.FindNode("\Data\Blocks\E-104\Input\PROGRAM_MODE")
    Specification: (T-Cold)      Application.Tree.FindNode("\Data\Blocks\E-104\Input\SPEC")
    Specification unit: (C)      Application.Tree.FindNode("\Data\Blocks\E-104\Input\SPECUN")
    Specification value: (160)   Application.Tree.FindNode("\Data\Blocks\E-104\Input\VALUE")
    Heaterexchanger type (countercurrent): Application.Tree.FindNode("\Data\Blocks\E-104\Input\TYPE")
    '''

    '''
    Output
    Cold T Out          Application.Tree.FindNode("\Data\Blocks\E-104\Output\TEMP_CLD\INLET") 1st entry
    Cold P Out          Application.Tree.FindNode("\Data\Blocks\E-104\Output\PRES_CLD\INLET") 1st entry

    Hot T Out           Application.Tree.FindNode("\Data\Blocks\E-104\Output\TEMP_HOT\INLET") last entry
    Hot P Out           Application.Tree.FindNode("\Data\Blocks\E-104\Output\PRES_HOT\INLET") last entry

    Duty                Application.Tree.FindNode("\Data\Blocks\E-104\Output\DUTY_CLD\INLET") last entry
    '''


    