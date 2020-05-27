import os
import win32com.client as win32

from .objectcollection import ObjectCollection
from .blocks import Blocks
from .streams import Material, Heat

class Aspen(object):


    def __init__(self, Aspen_file):

        self.aspen = win32.Dispatch('Apwn.Document')
        self.aspen.InitFromArchive2(os.path.abspath(Aspen_file))

        self.blocks = ObjectCollection()
        self.streams = ObjectCollection()
        self.material_streams = ObjectCollection()
        self.heat_streams = ObjectCollection()
        
        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")

        for obj in blocks.Elements:
            self.blocks[obj.Name] = obj

        for obj in streams.Elements:
            if hasattr(obj.Output, 'MASSFLMX'):
                self.streams[obj.Name] = Material(obj)
                self.material_streams[obj.Name] = Material(obj)

            else:
                self.streams[obj.Name] = Heat(obj)
                self.heat_streams[obj.Name] = Heat(obj)



    def Run(self):

        self.aspen.Engine.Run2()


        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")

        for obj in blocks.Elements:
            self.blocks[obj.Name] = obj


        for obj in streams.Elements:
            self.streams[obj.Name].Collect(obj)

        return