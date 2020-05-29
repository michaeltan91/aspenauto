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
    LPS_Gen,
    MP_Steam,
    MPS_Gen, 
    HP_Steam,
    HPS_Gen, 
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

    def __init__(self, aspen_file):
        
        # Load Aspen Model
        self.aspen = win32.Dispatch('Apwn.Document')
        self.aspen.InitFromArchive2(os.path.abspath(aspen_file))
        # Load print output class
        self.output = Output()

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
        self.lpsgen = ObjectCollection()
        self.mpsteam = ObjectCollection()
        self.mpsgen = ObjectCollection()
        self.hpsteam = ObjectCollection()
        self.hpsgen = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant = ObjectCollection()
        
        self.load_data(aspen_file)


    def Run(self):

        self.aspen.Engine.Run2()

        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")
        utilities = self.aspen.Tree.Data.Utilities

        #for obj in blocks.Elements:
        #    self.blocks[obj.Name] = obj

        for obj in streams.Elements:
            self.streams[obj.Name].Collect(obj)

        for obj in utilities.Elements:
            for obj2 in obj.Output.UTL_USAGE.Elements:
                self.utilities[obj.Name][obj2.Name].Collect_Usage(obj2)
            for obj2 in obj.Output.UTL_DUTY.Elements:
                self.utilities[obj.Name][obj2.Name].Collect_Duty(obj, obj2)


    def Print(self, work_book):

        self.output.Print_Mass(self.material_streams, work_book)


    def load_data(self, aspen_file):
        
        # Assign dictionaries for each block and stream
        blocks = self.aspen.Tree.FindNode("\Data\Blocks")
        streams = self.aspen.Tree.FindNode("\Data\Streams")
        utilities = self.aspen.Tree.Data.Utilities  # Dot notation only works ???
        # Load Aspen model as text file, to get block type for each block
        temp = []
        with open(aspen_file) as input_data:
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
                        self.assign_utility(obj, block_type)
                    elif block_type == 'DSTWU' or block_type == 'RadFrac' or block_type == 'Extract':
                        column = Column(block_type)
                        self.columns[obj.Name] = column
                        self.blocks[obj.Name] = column
                        self.assign_utility(obj, block_type)
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
        
        for util in utilities.Elements:
            if util.Name == 'CW':
                self.utilities[util.Name] = self.coolwater
            elif util.Name == 'Elect':
                self.utilities[util.Name] = self.electricity 
            elif util.Name == 'LP-STEAM':
                self.utilities[util.Name] = self.lpsteam
            elif util.Name == 'LPS-GEN':
                self.utilities[util.Name] = self.lpsgen
            elif util.Name == 'MP-STEAM':
                self.utilities[util.Name] = self.mpsteam
            elif util.Name == 'MPS-GEN':
                self.utilities[util.Name] = self.mpsgen
            elif util.Name == 'HP-STEAM':
                self.utilities[util.Name] = self.hpsteam
            elif util.Name == 'HPS-GEN':
                self.utilities[util.Name] = self.hpsgen
            elif util.Name == 'REFRIG':
                self.utilities[util.Name] = self.refrigerant


    def assign_utility(self, block, block_type):
        if block_type == 'RadFrac':
            if block.Input.COND_UTIL.Value == 'CW':
                coolwater = Coolwater()
                self.coolwater[block.Name] = coolwater
            elif block.Input.COND_UTIL.Value == 'REFRIG':
                refrig = Refrigerant()
                self.refrigerant[block.Name] = refrig
            
        elif block_type == 'Heater':
            if block.Input.UTILITY_ID.Value == 'CW':
                coolwater = Coolwater()
                self.coolwater[block.Name] = coolwater
            elif block.Input.UTILITY_ID.Value == 'REFRIG':
                refrig = Refrigerant()
                self.refrigerant[block.Name] = refrig
            elif block.Input.UTILITY_ID.Value == 'LP-STEAM':
                lpsteam = LP_Steam()
                self.lpsteam[block.Name] = lpsteam
            elif block.Input.UTILITY_ID.Value == 'LPS-GEN':
                lpsgen = LPS_Gen()
                self.lpsgen[block.Name] = lpsgen
            elif block.Input.UTILITY_ID.Value == 'MP-STEAM':
                mpsteam = MP_Steam()
                self.mpsteam[block.Name] = mpsteam
            elif block.Input.UTILITY_ID.Value == 'MPS-GEN':
                mpsgen = MPS_Gen()
                self.mpsgen[block.Name] = mpsgen
            elif block.Input.UTILITY_ID.Value == 'HP-STEAM':
                hpsteam = HP_Steam()
                self.hpsteam[block.Name] = hpsteam
            elif block.Input.UTILITY_ID.Value == 'HPS-GEN':
                hpsgen = HPS_Gen()
                self.hpsgen[block.Name] = hpsgen
        
        elif block_type == 'Pump' or block_type == 'Comp':
            if block.Input.UTILITY_ID.Value == 'ELECTRIC':
                electricity = Electricity()
                self.electricity[block.Name] = electricity
        elif block_type == 'MComp':
            for stage in block.Input.SPECS_UTL.Elements:
                if stage.Value == 'Electricity':
                    electricity = Electricity()
                    self.electricity[block.Name] = electricity
            for stage in block.Input.COOLER_UTL.Elements:
                if stage.Value == 'COOLWAT':
                    coolwater = Coolwater()
                    self.coolwater[block.Name] = coolwater
                elif stage.Value == 'REFRIG':
                    refrigerant = Refrigerant()
                    self.refrigerant[block.Name] = refrigerant




