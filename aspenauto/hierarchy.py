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
        self.hierarchy = ObjectCollection()
        # Stream dictionaries
        self.streams = ObjectCollection()
        self.material_streams = ObjectCollection()
        self.heat_streams = ObjectCollection()
        self.work_streams = ObjectCollection()
        # Utility dictionaries
        self.coolwater = ObjectCollection()
        self.lpsteam = ObjectCollection()
        self.lpsgen = ObjectCollection()
        self.mpsteam = ObjectCollection()
        self.mpsgen = ObjectCollection()
        self.hpsteam = ObjectCollection()
        self.hpsgen = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant = ObjectCollection()
        self.utilities = ObjectCollection()
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
            if block_type == 'Mixer' or block_type == 'FSplit' or block_type == 'Mixer':
                mix = MixSplit(block_type, obj.Name)
                self.mixsplits[obj.Name] = mix
                self.blocks[obj.Name] = mix
            elif block_type == 'Flash2' or block_type == 'Flash3' or block_type == 'Decanter' or block_type == 'Sep':
                sep = Separator(block_type, obj.Name)
                self.separators[obj.Name] = sep
                self.blocks[obj.Name] = sep
            elif block_type == 'Heater' or block_type == 'HeatX':
                exchange = Exchanger(block_type, obj.Name)
                self.exchangers[obj.Name] = exchange
                self.blocks[obj.Name] = exchange
                self.assign_utility_heater(obj, block_type)
            elif block_type == 'DSTWU' or block_type == 'RadFrac' or block_type == 'Extract':
                column = Column(block_type, obj.Name)
                self.columns[obj.Name] = column
                self.blocks[obj.Name] = column
                self.assign_utility_column(obj, block_type)
            elif block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs' or block_type == 'RPlug':
                reactor = Reactor(block_type, obj.Name)
                self.reactors[obj.Name] = reactor
                self.blocks[obj.Name] = reactor
                self.assign_utility_reactor(obj, block_type)
            elif block_type == 'Pump' or block_type == 'Compr' or block_type == 'MCompr' or block_type == 'Valve':
                pressure = Pressure(block_type, obj.Name)   
                self.pressurechangers[obj.Name] = pressure
                self.blocks[obj.Name] = pressure
                self.assign_utility_pressure(obj, block_type)
            ## Solids not implemented yet
            elif block_type == 'Cyclone' or block_type == 'VScrub':
                solidsep = SolidsSeparator(block_type, obj.Name)
                self.solidseparators[obj.Name] = solidsep
                self.blocks[obj.Name] = solidsep
            elif block_type == 'Hierarchy':
                hierarchy = Hierarchy(self.aspen, obj.Name, base_path)
                self.hierarchy[obj.Name] = hierarchy
                self.blocks[obj.Name] = hierarchy

        # Load and fill stream dictionaries
        for obj in streams.Elements:
            base_path = self.base_path+"\\Data\\Streams\\"
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
        util_loc = self.name+'.'+block.Name
        if block_type == 'RadFrac':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COND_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen, util_loc)
                self.coolwater[block.Name] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen, util_loc)
                self.refrigerant[block.Name] = refrig
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\REB_UTIL'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen, util_loc)
                self.lpsteam[block.Name] = lpsteam
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen, util_loc)
                self.mpsteam[block.Name] = mpsteam
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen, util_loc)
                self.hpsteam[block.Name] = hpsteam
    

    def assign_utility_heater(self, block, block_type):
        util_loc = self.name+'.'+block.Name
        if block_type == 'Heater':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen, util_loc)
                self.coolwater[block.Name] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen, util_loc)
                self.refrigerant[block.Name] = refrig
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen, util_loc)
                self.lpsteam[block.Name] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, self.aspen, util_loc)
                self.lpsgen[block.Name] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen, util_loc)
                self.mpsteam[block.Name] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, self.aspen, util_loc)
                self.mpsgen[block.Name] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen, util_loc)
                self.hpsteam[block.Name] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, self.aspen, util_loc)
                self.hpsgen[block.Name] = hpsgen
    

    def assign_utility_pressure(self, block, block_type):
        util_loc = self.name+'.'+block.Name
        if block_type == 'Pump' or block_type == 'Compr':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'ELECTRIC':
                electricity = Electricity(block.Name, self.aspen, util_loc)
                self.electricity[block.Name] = electricity

        elif block_type == 'MCompr':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\SPECS_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'ELECTRIC':
                    electricity = Electricity(block.Name, self.aspen, util_loc)
                    self.electricity[block.Name] = electricity
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\COOLER_UTL'
            stages = self.aspen.Tree.FindNode(path).Elements
            for stage in stages:
                if stage.Value == 'CW':
                    coolwater = Coolwater(block.Name, self.aspen, util_loc)
                    self.coolwater[block.Name] = coolwater
                elif stage.Value == 'RF':
                    refrigerant = Refrigerant(block.Name, self.aspen, util_loc)
                    self.refrigerant[block.Name] = refrigerant


    def assign_utility_reactor(self, block, block_type):
        util_loc = self.name+'.'+block.Name
        if block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs':
            path = self.base_path+'\\Data\\Blocks\\'+str(block.Name)+'\\Input\\UTILITY_ID'
            utility = self.aspen.Tree.FindNode(path).Value
            if utility == 'CW':
                coolwater = Coolwater(block.Name, self.aspen, util_loc)
                self.coolwater[block.Name] = coolwater
            elif utility == 'RF':
                refrig = Refrigerant(block.Name, self.aspen, util_loc)
                self.refrigerant[block.Name] = refrig
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, self.aspen, util_loc)
                self.lpsteam[block.Name] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, self.aspen, util_loc)
                self.lpsgen[block.Name] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, self.aspen, util_loc)
                self.mpsteam[block.Name] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, self.aspen, util_loc)
                self.mpsgen[block.Name] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, self.aspen, util_loc)
                self.hpsteam[block.Name] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, self.aspen, util_loc)
                self.hpsgen[block.Name] = hpsgen




    