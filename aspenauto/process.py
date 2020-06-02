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

class Process(object):

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


    def Print(self, work_book):

        self.output.Print_Mass(self.material_streams, work_book)
        #self.output.Print_Energy(self.utilities, work_book)


    def Reset(self):
        for stream in self.streams:
            stream.Reset()
        for utility in self.utilities:
            utility.Reset()
        

    def load_data(self, aspen_file):
        
        # Assign dictionaries for each block and stream
        blocks = self.aspen.Tree.FindNode("\\Data\\Blocks")
        streams = self.aspen.Tree.FindNode("\\Data\\Streams")
        utilities = self.aspen.Tree.FindNode("\\Data\\Utilities")  # Dot notation only works ???
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
                        print(obj.Name)
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
                material = Material(obj, self.aspen)
                self.streams[obj.Name] = material
                self.material_streams[obj.Name] = material
            elif hasattr(obj.Output, 'POWER_OUT'):
                work = Work(obj, self.aspen)
                self.work_streams[obj.Name] = work
                self.streams[obj.Name] = work
            else:
                heat = Heat(obj, self.aspen)
                self.streams[obj.Name] = heat
                self.heat_streams[obj.Name] = heat
        
        # Load and fill utility dictionaries
        for util in utilities.Elements:
            if util.Name == 'CW':
                self.utilities[util.Name] = self.coolwater
            elif util.Name == 'ELECTRIC':
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
            elif util.Name == 'RF':
                self.utilities[util.Name] = self.refrigerant

        temp = []
        prefer = ['LP-STEAM', 'LPS-GEN', 'MP-STEAM', 'MPS-GEN', 'HP-STEAM', 'HPS-GEN', 'REFRIG', 'ELECTRIC' , 'NATGAS', 'CW']
        for i in prefer:
            if i in self.utilities:
                temp.append(i)
        temp2 = ObjectCollection()
        for j in temp:
            temp2[j] = self.utilities[j]
        self.utilities = temp2

    def assign_utility(self, block, block_type):
        if block_type == 'RadFrac':
            utility = block.Input.COND_UTIL.Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen)
                self.coolwater[block.Name] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen)
                self.refrigerant[block.Name] = refrig
            
        elif block_type == 'Heater':
            utility = block.Input.UTILITY_ID.Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen)
                self.coolwater[block.Name] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen)
                self.refrigerant[block.Name] = refrig
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen)
                self.lpsteam[block.Name] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, self.aspen)
                self.lpsgen[block.Name] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen)
                self.mpsteam[block.Name] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, self.aspen)
                self.mpsgen[block.Name] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen)
                self.hpsteam[block.Name] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, self.aspen)
                self.hpsgen[block.Name] = hpsgen
        
        elif block_type == 'Pump' or block_type == 'Comp':
            if block.Input.UTILITY_ID.Value == 'ELECTRIC':
                electricity = Electricity(block.Name, self.aspen)
                self.electricity[block.Name] = electricity
        elif block_type == 'MComp':
            for stage in block.Input.SPECS_UTL.Elements:
                if stage.Value == 'Electricity':
                    electricity = Electricity(block.Name, self.aspen)
                    self.electricity[block.Name] = electricity
            for stage in block.Input.COOLER_UTL.Elements:
                if stage.Value == 'COOLWAT':
                    coolwater = Coolwater(block.Name, self.aspen)
                    self.coolwater[block.Name] = coolwater
                elif stage.Value == 'RF':
                    refrigerant = Refrigerant(block.Name, self.aspen)
                    self.refrigerant[block.Name] = refrigerant




