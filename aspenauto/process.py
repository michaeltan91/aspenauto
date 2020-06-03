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
        self.output.Print_Energy(self.utilities, work_book)


    def Reset(self):
        for stream in self.streams:
            stream.Reset()
        for utility in self.utilities:
            utility.Reset()
    
    def Close(self):
        self.aspen.Close()
        

    def load_data(self, aspen_file):
        
        # Assign dictionaries for each block and stream
        blocks = self.aspen.Tree.FindNode("\\Data\\Blocks")
        streams = self.aspen.Tree.FindNode("\\Data\\Streams")
        utilities = self.aspen.Tree.FindNode("\\Data\\Utilities")  
        
        # Load and fill block dictionaries 
        for obj in blocks.Elements:
            base_path = '\\Data\\Blocks\\'
            path = base_path+str(obj.Name)
            block_type = self.aspen.Tree.FindNode(path).AttributeValue(6)
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
                self.assign_utility_heater(obj, block_type)
            elif block_type == 'DSTWU' or block_type == 'RadFrac' or block_type == 'Extract':
                column = Column(block_type)
                self.columns[obj.Name] = column
                self.blocks[obj.Name] = column
                self.assign_utility_column(obj, block_type)
            elif block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs' or block_type == 'RPlug':
                reactor = Reactor(block_type)
                self.reactors[obj.Name] = reactor
                self.blocks[obj.Name] = reactor
                self.assign_utility_reactor(obj, block_type)
            elif block_type == 'Pump' or block_type == 'Compr' or block_type == 'MCompr' or block_type == 'Valve':
                pressure = Pressure(block_type)   
                self.pressurechangers[obj.Name] = pressure
                self.blocks[obj.Name] = pressure
                self.assign_utility_pressure(obj, block_type)
            ## Solids not implemented yet
            elif block_type == 'Cyclone' or block_type == 'VScrub':
                solidsep = SolidsSeparator(block_type)
                self.solidseparators[obj.Name] = solidsep
                self.blocks[obj.Name] = solidsep

        # Load and fill stream dictionaries
        for obj in streams.Elements:
            base_path = '\\Data\\Streams\\'
            path = base_path+str(obj.Name)
            stream_type = self.aspen.Tree.FindNode(path).AttributeValue(6)
            if stream_type == 'MATERIAL':
                material = Material(obj, self.aspen, base_path)
                self.streams[obj.Name] = material
                self.material_streams[obj.Name] = material
            elif stream_type == 'HEAT':
                work = Work(obj, self.aspen, base_path)
                self.work_streams[obj.Name] = work
                self.streams[obj.Name] = work
            else:
                heat = Heat(obj, self.aspen, base_path)
                self.streams[obj.Name] = heat
                self.heat_streams[obj.Name] = heat
        
        # Load and fill utility dictionaries
        for util in utilities.Elements:
            if util.Name == 'CW':
                self.utilities[util.Name] = self.coolwater
            elif util.Name == 'ELECTRIC':
                self.utilities[util.Name] = self.electricity 
            elif util.Name == 'LPS':
                self.utilities[util.Name] = self.lpsteam
            elif util.Name == 'LPS-GEN':
                self.utilities[util.Name] = self.lpsgen
            elif util.Name == 'MPS':
                self.utilities[util.Name] = self.mpsteam
            elif util.Name == 'MPS-GEN':
                self.utilities[util.Name] = self.mpsgen
            elif util.Name == 'HPS':
                self.utilities[util.Name] = self.hpsteam
            elif util.Name == 'HPS-GEN':
                self.utilities[util.Name] = self.hpsgen
            elif util.Name == 'RF':
                self.utilities[util.Name] = self.refrigerant

        temp = []
        prefer = ['LPS', 'LPS-GEN', 'MPS', 'MPS-GEN', 'HPS', 'HPS-GEN', 'RF', 'ELECTRIC' , 'NATGAS', 'CW']
        for i in prefer:
            if i in self.utilities:
                temp.append(i)
        temp2 = ObjectCollection()
        for j in temp:
            temp2[j] = self.utilities[j]
        self.utilities = temp2


    def assign_utility_column(self, block, block_type):
        if block_type == 'RadFrac':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COND_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen)
                self.coolwater[block.Name] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen)
                self.refrigerant[block.Name] = refrig
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\REB_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen)
                self.lpsteam[block.Name] = lpsteam
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen)
                self.mpsteam[block.Name] = mpsteam
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen)
                self.hpsteam[block.Name] = hpsteam
    

    def assign_utility_heater(self, block, block_type):
        if block_type == 'Heater':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
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
    

    def assign_utility_pressure(self, block, block_type):
        if block_type == 'Pump' or block_type == 'Compr':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'ELECTRIC':
                electricity = Electricity(block.Name, self.aspen)
                self.electricity[block.Name] = electricity

        elif block_type == 'MCompr':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\SPECS_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'ELECTRIC':
                    electricity = Electricity(block.Name, self.aspen)
                    self.electricity[block.Name] = electricity
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COOLER_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'CW':
                    coolwater = Coolwater(block.Name, self.aspen)
                    self.coolwater[block.Name] = coolwater
                elif stage.Value == 'RF':
                    refrigerant = Refrigerant(block.Name, self.aspen)
                    self.refrigerant[block.Name] = refrigerant


    def assign_utility_reactor(self, block, block_type):
        if block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
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

