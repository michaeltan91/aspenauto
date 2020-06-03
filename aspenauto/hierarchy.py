from .objectcollection import ObjectCollection
from .streams import (
    Material,
    Work, 
    Heat
    )

class Hierarchy(object):

    def __init__(self, aspen, name, path):

        self.aspen = aspen
        self.base_path = path+str(name)
        self.name = name

        # Declare dictionaries for easy access of Aspen Results/Variables
        # Block dictionaries
        self.blocks = ObjectCollection()
        self.mixsplits = ObjectCollection()
        self.separators = ObjectCollection()
        self.exchangers = ObjectCollection()
        self.columns = ObjectCollection()
        self.reactors = ObjectCollection()
        self.pressurechangers = ObjectCollection()
        self.solids = ObjectCollection()
        self.solidseparators = ObjectCollection()
        # Stream dictionaries
        self.streams = ObjectCollection()
        self.material_streams = ObjectCollection()
        self.heat_streams = ObjectCollection()
        self.work_streams = ObjectCollection()


    def load_data(self):

        return


    