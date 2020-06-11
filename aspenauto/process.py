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
    LLP_Steam,
    LLPS_Gen,
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
from .hierarchy import Hierarchy

class Process(object):
    # Main class

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
        self.hierarchy = ObjectCollection()
        # Stream dictionaries
        self.streams = ObjectCollection()
        self.material_streams = ObjectCollection()
        self.heat_streams = ObjectCollection()
        self.work_streams = ObjectCollection()
        # Utility dictionaries
        self.utilities = ObjectCollection()
        self.coolwater = ObjectCollection()
        self.llpsteam = ObjectCollection()
        self.llpsgen = ObjectCollection()
        self.lpsteam = ObjectCollection()
        self.lpsgen = ObjectCollection()
        self.mpsteam = ObjectCollection()
        self.mpsgen = ObjectCollection()
        self.hpsteam = ObjectCollection()
        self.hpsgen = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant1 = ObjectCollection()
        self.refrigerant2 = ObjectCollection()
        self.refrigerant3 = ObjectCollection()
        self.refrigerant4 = ObjectCollection()
        # Assign classes to all Aspen Plus simulation objects
        self.load_data()


    def Run(self):
        # Run the Aspen Engine
        self.aspen.Engine.Run2()
        error_path = "\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR"
        error = self.aspen.Tree.FindNode(error_path).Value
        if error == 1:
            report = ''
            for sentence in self.aspen.Tree.FindNode(error_path).Elements:
                report = report + str(sentence.Value)+'\n'
            print(report)
            #raise RuntimeError('Error/Warning in Aspen Plus simulation')
            

    def Print(self, work_book):
        # Print output in excel file
        self.output.Print_Mass(self.material_streams, work_book)
        self.output.Print_Energy(self.utilities, work_book)


    def Reset(self):
        self.aspen.Reinit()
        # Resets all class attribute values
        for stream in self.streams:
            stream.reset()
        for utility in self.utilities:
            for block in utility:
                block.reset()
    
    def Close(self):
        # Closes the Aspen Plus Engine IMPORTANT!!!
        self.aspen.Close()
        

    def load_data(self):
        
        # Assign dictionaries for each block and stream
        blocks = self.aspen.Tree.FindNode("\\Data\\Blocks")
        streams = self.aspen.Tree.FindNode("\\Data\\Streams")
        utilities = self.aspen.Tree.FindNode("\\Data\\Utilities")  
        
        # Load and fill block dictionaries 
        for obj in blocks.Elements:
            base_path = '\\Data\\Blocks\\'
            path = base_path+str(obj.Name)
            block_type = self.aspen.Tree.FindNode(path).AttributeValue(6)
            uid = obj.Name
            if block_type == 'Mixer' or block_type == 'FSplit' or block_type == 'Mixer':
                mix = MixSplit(block_type, obj.Name, uid)
                self.mixsplits[uid] = mix
                self.blocks[uid] = mix
            elif block_type == 'Flash2' or block_type == 'Flash3' or block_type == 'Decanter' or block_type == 'Sep':
                sep = Separator(block_type, obj.Name, uid)
                self.separators[uid] = sep
                self.blocks[uid] = sep
            elif block_type == 'Heater' or block_type == 'HeatX':
                exchange = Exchanger(block_type, obj.Name, uid)
                self.exchangers[uid] = exchange
                self.blocks[uid] = exchange
                self.assign_utility_heater(obj, block_type)
            elif block_type == 'DSTWU' or block_type == 'RadFrac' or block_type == 'Extract':
                column = Column(block_type, obj.Name, uid)
                self.columns[uid] = column
                self.blocks[uid] = column
                self.assign_utility_column(obj, block_type)
            elif block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs' or block_type == 'RPlug':
                reactor = Reactor(block_type, obj.Name, uid)
                self.reactors[uid] = reactor
                self.blocks[uid] = reactor
                self.assign_utility_reactor(obj, block_type)
            elif block_type == 'Pump' or block_type == 'Compr' or block_type == 'MCompr' or block_type == 'Valve':
                pressure = Pressure(block_type, obj.Name, uid)   
                self.pressurechangers[uid] = pressure
                self.blocks[uid] = pressure
                self.assign_utility_pressure(obj, block_type)
            ## Solids not implemented yet
            elif block_type == 'Cyclone' or block_type == 'VScrub':
                solidsep = SolidsSeparator(block_type, obj.Name, uid)
                self.solidseparators[uid] = solidsep
                self.blocks[uid] = solidsep
            elif block_type == 'Hierarchy':
                hierarchy = Hierarchy(self, obj.Name, base_path)
                self.hierarchy[uid] = hierarchy
                self.blocks[uid] = hierarchy

        # Load and fill stream dictionaries
        for obj in streams.Elements:
            base_path = '\\Data\\Streams\\'
            path = base_path+str(obj.Name)
            uid = obj.Name
            stream_type = self.aspen.Tree.FindNode(path).AttributeValue(6)
            if stream_type == 'MATERIAL':
                material = Material(obj.Name, uid, base_path, self)
                self.streams[uid] = material
                self.material_streams[uid] = material
            elif stream_type == 'HEAT':
                work = Work(obj.Name, uid, base_path, self)
                self.work_streams[uid] = work
                self.streams[uid] = work
            else:
                heat = Heat(obj.Name, uid, base_path, self)
                self.streams[uid] = heat
                self.heat_streams[uid] = heat
        
        # Load and fill utility dictionaries
        for util in utilities.Elements:
            if util.Name == 'CW':
                self.utilities[util.Name] = self.coolwater
            elif util.Name == 'ELECTRIC':
                self.utilities[util.Name] = self.electricity
            elif util.Name == 'LLPS':
                self.utilities[util.Name] = self.llpsteam
            elif util.Name == 'LLPS-GEN':
                self.utilities[util.Name] = self.llpsgen
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
            elif util.Name == 'RF1':
                self.utilities[util.Name] = self.refrigerant1
            elif util.Name == 'RF2':
                self.utilities[util.Name] = self.refrigerant2
            elif util.Name == 'RF3':
                self.utilities[util.Name] = self.refrigerant3
            elif util.Name == 'RF4':
                self.utilities[util.Name] = self.refrigerant4
    
        temp = []
        prefer = ['LLPS','LLPS-GEN', 'LPS', 'LPS-GEN', 'MPS', 'MPS-GEN', 'HPS', 'HPS-GEN', 'RF', 'ELECTRIC' , 'NATGAS', 'CW']
        for i in prefer:
            if i in self.utilities:
                temp.append(i)
        temp2 = ObjectCollection()
        for j in temp:
            temp2[j] = self.utilities[j]
        self.utilities = temp2


    def assign_utility_column(self, block, block_type):
        # Assign column utilities
        uid = block.Name
        if block_type == 'RadFrac':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COND_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, uid, self)
                self.coolwater[uid] = coolwater
            elif utility == 'RF1':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant1[uid] = refrig
            elif utility == 'RF2':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant2[uid] = refrig
            elif utility == 'RF3':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant3[uid] = refrig
            elif utility == 'RF4':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant4[uid] = refrig
            elif utility == 'LLPS-GEN':
                llpsgen = LLPS_Gen(block.Name, uid, self)
                self.llpsgen[uid] = llpsgen
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, uid, self)
                self.lpsgen[uid] = lpsgen
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, uid, self)
                self.mpsgen[uid] = mpsgen

            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\REB_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'LPS':
                lpsteam = LP_Steam(block.Name, uid, self)
                self.lpsteam[uid] = lpsteam
            elif utility == 'LLPS':
                llpsteam = LLP_Steam(block.Name, uid, self)
                self.llpsteam[uid] = llpsteam
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, uid, self)
                self.mpsteam[uid] = mpsteam
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, uid, self)
                self.hpsteam[uid] = hpsteam
    

    def assign_utility_heater(self, block, block_type):
        # Assign heater utilities
        uid = block.Name
        if block_type == 'Heater':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, uid, self)
                self.coolwater[uid] = coolwater
            elif utility == 'RF1':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant1[uid] = refrig
            elif utility == 'RF2':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant2[uid] = refrig
            elif utility == 'RF3':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant3[uid] = refrig
            elif utility == 'RF4':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant4[uid] = refrig
            elif utility == 'LLPS':
                llpsteam = LLP_Steam(block.Name, uid, self)
                self.llpsteam[uid] = llpsteam
            elif utility == 'LLPS-GEN':
                llpsgen = LLPS_Gen(block.Name, uid, self)
                self.llpsgen[uid] = llpsgen
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, uid, self)
                self.lpsteam[uid] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, uid, self)
                self.lpsgen[uid] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, uid, self)
                self.mpsteam[uid] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, uid, self)
                self.mpsgen[uid] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, uid, self)
                self.hpsteam[uid] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, uid, self)
                self.hpsgen[uid] = hpsgen
    

    def assign_utility_pressure(self, block, block_type):
        # Assign utilities of pumps, compressors and multistage compressors
        uid = block.Name
        if block_type == 'Pump' or block_type == 'Compr':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'ELECTRIC':
                electricity = Electricity(block.Name, uid, self)
                self.electricity[uid] = electricity

        elif block_type == 'MCompr':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\SPECS_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'ELECTRIC':
                    electricity = Electricity(block.Name, uid, self)
                    self.electricity[uid] = electricity
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COOLER_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'CW':
                    coolwater = Coolwater(block.Name, uid, self)
                    self.coolwater[uid] = coolwater
                elif stage.Value == 'RF1':
                    refrigerant = Refrigerant(block.Name, uid, self)
                    self.refrigerant1[uid] = refrigerant
                elif stage.Value == 'RF2':
                    refrigerant = Refrigerant(block.Name, uid, self)
                    self.refrigerant2[uid] = refrigerant
                elif stage.Value == 'RF3':
                    refrigerant = Refrigerant(block.Name, uid, self)
                    self.refrigerant3[uid] = refrigerant
                elif stage.Value == 'RF4':
                    refrigerant = Refrigerant(block.Name, uid, self)
                    self.refrigerant4[uid] = refrigerant


    def assign_utility_reactor(self, block, block_type):
        # Assign reactor utilities
        uid = block.Name
        if block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs':
            path = '\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, uid, self)
                self.coolwater[uid] = coolwater
            elif utility == 'RF1':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant1[uid] = refrig
            elif utility == 'RF2':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant2[uid] = refrig
            elif utility == 'RF3':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant3[uid] = refrig
            elif utility == 'RF4':
                refrig = Refrigerant(block.Name, uid, self)
                self.refrigerant4[uid] = refrig
            elif utility == 'LLPS':
                llpsteam = LLP_Steam(block.Name, uid, self)
                self.llpsteam[uid] = llpsteam
            elif utility == 'LLPS-GEN':
                llpsgen = LLPS_Gen(block.Name, uid, self)
                self.llpsgen[uid] = llpsgen
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, uid, self)
                self.lpsteam[uid] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, uid, self)
                self.lpsgen[uid] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, uid, self)
                self.mpsteam[uid] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, uid, self)
                self.mpsgen[uid] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, uid, self)
                self.hpsteam[uid] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, uid, self)
                self.hpsgen[uid] = hpsgen

