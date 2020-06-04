from .objectcollection import ObjectCollection
from .streams import (
    Material,
    Work, 
    Heat
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
class Hierarchy(object):

    def __init__(self, process, name, path, uid=""):

        self.aspen = process.aspen
        self.base_path = path+str(name)
        self.name = name
        if uid == "":
            self.uid = self.name
            
        else: 
            self.uid = uid + '.' + self.name

        # Declare dictionaries for easy access of Aspen Results/Variables
        # Block dictionaries
        self.blocks = process.blocks
        self.mixsplits = process.mixsplits
        self.separators = process.separators
        self.exchangers = process.exchangers
        self.columns = process.columns
        self.reactors = process.reactors
        self.pressurechangers = process.pressurechangers
        self.solids = process.solids
        self.solidseparators = process.solidseparators
        self.hierarchy = process.hierarchy
        # Stream dictionaries
        self.streams = process.streams
        self.material_streams = process.material_streams
        self.heat_streams = process.heat_streams
        self.work_streams = process.work_streams
        # Utility dictionaries
        self.coolwater = process.coolwater
        self.lpsteam = process.lpsteam
        self.lpsgen = process.lpsgen
        self.mpsteam = process.mpsteam
        self.mpsgen = process.mpsgen
        self.hpsteam = process.hpsteam
        self.hpsgen = process.hpsgen
        self.electricity = process.electricity
        self.refrigerant = process.refrigerant
        self.utilities = process.utilities
        # Load input
        self.load_data()

    def load_data(self):
        blocks = self.aspen.Tree.FindNode(self.base_path+"\\Data\\Blocks")
        streams = self.aspen.Tree.FindNode(self.base_path+"\\Data\\Streams")
        utilities = self.aspen.Tree.FindNode("\\Data\\Utilities")
        
        # Load and fill block dictionaries 
        for obj in blocks.Elements:
            base_path = self.base_path+'\\Data\\Blocks\\'+str(obj.Name)
            block_type = self.aspen.Tree.FindNode(base_path).AttributeValue(6)
            uid = self.uid+'.'+obj.Name
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
            elif block_type == 'HIERARCHY':
                base_path = self.base_path+'\\Data\\Blocks\\'
                hierarchy = Hierarchy(self, obj.Name, base_path, self.uid)
                self.hierarchy[uid] = hierarchy
                self.blocks[uid] = hierarchy

        # Load and fill stream dictionaries
        for obj in streams.Elements:
            base_path = self.base_path+"\\Data\\Streams\\"
            path = base_path+str(obj.Name)
            stream_type = self.aspen.Tree.FindNode(path).AttributeValue(6)
            uid = self.uid+'.'+obj.Name
            if stream_type == 'MATERIAL':
                material = Material(obj, self.aspen, base_path, uid)
                self.streams[uid] = material
                self.material_streams[uid] = material
            elif stream_type == 'HEAT':
                work = Work(obj, self.aspen, base_path, uid)
                self.work_streams[uid] = work
                self.streams[uid] = work
            else:
                heat = Heat(obj, self.aspen, base_path, uid)
                self.streams[uid] = heat
                self.heat_streams[uid] = heat


            
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
        uid = self.uid+'.'+block.Name
        if block_type == 'RadFrac':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COND_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen, uid)
                self.coolwater[uid] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen, uid)
                self.refrigerant[uid] = refrig
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\REB_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen, uid)
                self.lpsteam[uid] = lpsteam
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen, uid)
                self.mpsteam[uid] = mpsteam
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen, uid)
                self.hpsteam[uid] = hpsteam
    

    def assign_utility_heater(self, block, block_type):
        uid = self.uid+'.'+block.Name
        if block_type == 'Heater':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen, uid)
                self.coolwater[uid] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen, uid)
                self.refrigerant[uid] = refrig
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen, uid)
                self.lpsteam[uid] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, self.aspen, uid)
                self.lpsgen[uid] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen, uid)
                self.mpsteam[uid] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, self.aspen, uid)
                self.mpsgen[uid] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen, uid)
                self.hpsteam[uid] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, self.aspen, uid)
                self.hpsgen[uid] = hpsgen
    

    def assign_utility_pressure(self, block, block_type):
        uid = self.uid+'.'+block.Name
        if block_type == 'Pump' or block_type == 'Compr':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'ELECTRIC':
                electricity = Electricity(block.Name, self.aspen, uid)
                self.electricity[uid] = electricity

        elif block_type == 'MCompr':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\SPECS_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'ELECTRIC':
                    electricity = Electricity(block.Name, self.aspen, uid)
                    self.electricity[uid] = electricity
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COOLER_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'CW':
                    coolwater = Coolwater(block.Name, self.aspen, uid)
                    self.coolwater[uid] = coolwater
                elif stage.Value == 'RF':
                    refrigerant = Refrigerant(block.Name, self.aspen, uid)
                    self.refrigerant[uid] = refrigerant


    def assign_utility_reactor(self, block, block_type):
        uid = self.uid+'.'+block.Name
        if block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen, uid)
                self.coolwater[uid] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen, uid)
                self.refrigerant[uid] = refrig
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen, uid)
                self.lpsteam[uid] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, self.aspen, uid)
                self.lpsgen[uid] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen, uid)
                self.mpsteam[uid] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, self.aspen, uid)
                self.mpsgen[uid] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen, uid)
                self.hpsteam[uid] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, self.aspen, uid)
                self.hpsgen[uid] = hpsgen




    