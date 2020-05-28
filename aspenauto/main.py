import os
import win32com.client as win32

from .objectcollection import ObjectCollection
from .blocks import Block
from .streams import (
    Material, 
    Heat
    )
from .output import Output
from .utilities import (
    LP_Steam, 
    MP_Steam, 
    HP_Steam, 
    Coolwater,
    Refrigerant,
    Electricity
)

class Aspen(object):

    def __init__(self, Aspen_file):

        self.aspen = win32.Dispatch('Apwn.Document')
        self.aspen.InitFromArchive2(os.path.abspath(Aspen_file))

        self.blocks = ObjectCollection()
        self.streams = ObjectCollection()
        self.material_streams = ObjectCollection()
        self.heat_streams = ObjectCollection()
        
        self.utilities = ObjectCollection()
        self.coolwater = ObjectCollection()
        self.lpsteam = ObjectCollection()
        self.mpsteam = ObjectCollection()
        self.hpsteam = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant = ObjectCollection()

        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")

        for obj in blocks.Elements:
            self.blocks[obj.Name] = obj


        for obj in streams.Elements:
            if hasattr(obj.Output, 'MASSFLMX'):
                material = Material(obj)
                self.streams[obj.Name] = material
                self.material_streams[obj.Name] = material

            else:
                heat = Heat(obj)
                self.streams[obj.Name] = heat
                self.heat_streams[obj.Name] = heat
        
        self.output = Output()




    def Run(self):

        self.aspen.Engine.Run2()


        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")

        for obj in blocks.Elements:
            self.blocks[obj.Name] = obj

            if hasattr(obj.Input, 'UTILITY_ID') and obj.Input.UTILITY_ID.Value is not None:
                self.utilities[obj.Name].Collect(obj)

        for obj in streams.Elements:
            self.streams[obj.Name].Collect(obj)



    def Print(self, work_book):

        self.output.Print(self.material_streams, work_book)