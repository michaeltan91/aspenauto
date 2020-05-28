import os
import win32com.client as win32

from .objectcollection import ObjectCollection
from .blocks import Block
from .streams import (
    Material,
    Work, 
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
from .blocks import (
    MixSplit,
    Separator,
    Exchanger,
    Column,
    Reactor,
    Pressure,
    Solids,
    SolidsSeparator
)

class Aspen(object):

    def __init__(self, Aspen_file):
        
        # Load Aspen Model
        self.aspen = win32.Dispatch('Apwn.Document')
        self.aspen.InitFromArchive2(os.path.abspath(Aspen_file))

        # Load Aspen model as text file, to get block type for each block
        temp = []
        with open(Aspen_file) as input_data:
            for line in input_data:
                if line.strip() == ';':
                    break
            for line in input_data:
                temp.append(line)
                if '? SETUP MAIN ?' in line.strip():
                    break
        temp = [x.strip() for x in temp]
        del temp[-1]    # Remove last entry from list
        del temp[0:1]   # Remove first two entries from list 
        temp2 = {}
        for x in range(int(len(temp)/5)):
            temp2[temp[1+ 5*x]] = temp[2 + 5*x] 

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
        # Utility dictionaries
        self.utilities = ObjectCollection()
        self.coolwater = ObjectCollection()
        self.lpsteam = ObjectCollection()
        self.mpsteam = ObjectCollection()
        self.hpsteam = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant = ObjectCollection()

        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")

        
        # Load and fill block dictionaries
        for obj in blocks.Elements:
            for name2, block_type in temp2.items():
                if obj.Name == name2:
                    if block_type == 'Mixer' or block_type == 'FSplit' or block_type == 'Mixer':
                        mix = MixSplit(block_type)
                        self.mixsplits[obj.Name] = mix
                        self.blocks[obj.Name] = mix
                    elif block_type == 'Flash2' or block_type == 'Flash3' or block_type == 'Decanter' or block_type == 'Sep':
                        sep = Separator(block_type)
                        self.separators[obj.Name] = sep
                        self.blocks[obj.Name] = sep
                    elif block_type == 'Heater' or block_type == 'HeatX':
                        exchange = Exchanger(block_type)
                        self.exchangers[obj.Name] = exchange
                        self.blocks[obj.Name] = exchange
                    elif block_type == 'DSTWU' or block_type == 'RadFrac' or block_type == 'Extract':
                        column = Column(block_type)
                        self.columns[obj.Name] = column
                        self.blocks[obj.Name] = column
                    elif block_type == 'RStroic' or block_type == 'RYield' or block_type == 'RGibbs':
                        reactor = Reactor(block_type)
                        self.reactors[obj.Name] = reactor
                        self.blocks[obj.Name] = reactor
                    elif block_type == 'Pump' or block_type == 'Comp' or block_type == 'MComp' or block_type == 'Valve':
                        pressure = Pressure(block_type)
                        self.pressurechangers[obj.Name] = pressure
                        self.blocks[obj.Name] = pressure
                    ## Solids not implemented yet
                    elif block_type == 'Cyclone' or block_type == 'VScrub':
                        solidsep = SolidsSeparator(block_type)
                        self.solidseparators[obj.Name] = solidsep
                        self.blocks[obj.Name] = solidsep

        # Load and fill stream dictionaries
        for obj in streams.Elements:
            if hasattr(obj.Output, 'MASSFLMX'):
                material = Material(obj)
                self.streams[obj.Name] = material
                self.material_streams[obj.Name] = material
            elif hasattr(obj.Output, 'POWER_OUT'):
                work = Work(obj)
                self.work_streams[obj.Name] = work
                self.streams[obj.Name] = work
            else:
                heat = Heat(obj)
                self.streams[obj.Name] = heat
                self.heat_streams[obj.Name] = heat
        
        self.output = Output()




    def Run(self):

        self.aspen.Engine.Run2()

        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")

        #for obj in blocks.Elements:
        #    self.blocks[obj.Name] = obj

        for obj in streams.Elements:
            self.streams[obj.Name].Collect(obj)



    def Print(self, work_book):

        self.output.Print(self.material_streams, work_book)