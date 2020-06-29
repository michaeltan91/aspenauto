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
    Block,
    MixSplit,
    Separator,
    Exchanger,
    Column,
    Reactor,
    Pressure,
    Solids,
    SolidsSeparator
)



class Flowsheet(object):

    def __init__(self, process, path = '',name ='Main', uid=''):

        self.name = name
        if uid == "":
            if name == 'Main':
                self.uid = ''
                self.base_path = path
            else:
                self.uid = self.name+'.'
                self.base_path = path+str(name)
        else: 
            self.uid = uid  + self.name + '.'
            self.base_path = path+str(name)

        self.load_data(process)

    
    def load_data(self, process):
        
        # Assign dictionaries for each block and stream
        blocks = process.asp.get_block_list(self.uid)
        streams = process.asp.get_stream_list(self.uid)
        
        # Load and fill block dictionaries 
        '''for obj in blocks.Elements:'''
        for obj in blocks:
            uid = self.uid+obj.Name
            block_type = process.asp.get_block_type(uid)
            if block_type == 'Mixer' or block_type == 'FSplit' or block_type == 'Mixer':
                mix = MixSplit(block_type, obj.Name, uid, process)
                process.mixsplits[uid] = mix
                process.blocks[uid] = mix
            elif block_type == 'Flash2' or block_type == 'Flash3' or block_type == 'Decanter' or block_type == 'Sep':
                sep = Separator(block_type, obj.Name, uid, process)
                process.separators[uid] = sep
                process.blocks[uid] = sep
            elif block_type == 'Heater' or block_type == 'HeatX':
                exchange = Exchanger(block_type, obj.Name, uid, process)
                process.exchangers[uid] = exchange
                process.blocks[uid] = exchange
                self.assign_utility_heater(obj, block_type, process)
            elif block_type == 'DSTWU' or block_type == 'RadFrac' or block_type == 'Extract':
                column = Column(block_type, obj.Name, uid, process)
                process.columns[uid] = column
                process.blocks[uid] = column
                self.assign_utility_column(obj, block_type, process)
            elif block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs' or block_type == 'RPlug':
                reactor = Reactor(block_type, obj.Name, uid, process)
                process.reactors[uid] = reactor
                process.blocks[uid] = reactor
                self.assign_utility_reactor(obj, block_type, process)
            elif block_type == 'Pump' or block_type == 'Compr' or block_type == 'MCompr' or block_type == 'Valve':
                pressure = Pressure(block_type, obj.Name, uid, process)   
                process.pressurechangers[uid] = pressure
                process.blocks[uid] = pressure
                self.assign_utility_pressure(obj, block_type, process)
            ## Solids not implemented yet
            elif block_type == 'Cyclone' or block_type == 'VScrub':
                solidsep = SolidsSeparator(block_type, obj.Name, uid, process)
                process.solidseparators[uid] = solidsep
                process.blocks[uid] = solidsep
            elif block_type == 'Hierarchy' or block_type == 'HIERARCHY':
                base_path = self.base_path+'\\Data\\Blocks\\'
                hierarchy = Flowsheet(process, path = base_path ,name =obj.Name, uid = self.uid)
                process.hierarchy[uid] = hierarchy
                process.blocks[uid] = hierarchy

        # Load and fill stream dictionaries
        '''for obj in streams.Elements:'''
        for obj in streams:
            uid = self.uid+obj.Name
            stream_type = process.asp.get_stream_type(uid)

            if stream_type == 'MATERIAL':
                material = Material(obj.Name, uid, process)
                process.streams[uid] = material
                process.material_streams[uid] = material
            elif stream_type == 'WORK':
                work = Work(obj.Name, uid, process)
                process.work_streams[uid] = work
                process.streams[uid] = work
            elif stream_type == 'HEAT':
                heat = Heat(obj.Name, uid, process)
                process.streams[uid] = heat
                process.heat_streams[uid] = heat


    def assign_utility_column(self, block, block_type, process):
        # Assign column utilities
        uid = self.uid + block.Name
        if block_type == 'RadFrac':
            utility = process.asp.get_radfrac_cond_util(uid)
            if utility == 'CW':
                coolwater = Coolwater(block.Name, uid, process)
                process.coolwater[uid] = coolwater
            elif utility == 'RF1':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant1[uid] = refrig
            elif utility == 'RF2':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant2[uid] = refrig
            elif utility == 'RF3':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant3[uid] = refrig
            elif utility == 'RF4':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant4[uid] = refrig
            elif utility == 'LLPS-GEN':
                llpsgen = LLPS_Gen(block.Name, uid, process)
                process.llpsgen[uid] = llpsgen
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, uid, process)
                process.lpsgen[uid] = lpsgen
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, uid, process)
                process.mpsgen[uid] = mpsgen

            utility = process.asp.get_radfrac_reb_util(uid)
            if utility == 'LPS':
                lpsteam = LP_Steam(block.Name, uid, process)
                process.lpsteam[uid] = lpsteam
            elif utility == 'LLPS':
                llpsteam = LLP_Steam(block.Name, uid, process)
                process.llpsteam[uid] = llpsteam
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, uid, process)
                process.mpsteam[uid] = mpsteam
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, uid, process)
                process.hpsteam[uid] = hpsteam
    

    def assign_utility_heater(self, block, block_type, process):
        # Assign heater utilities
        uid = self.uid + block.Name
        if block_type == 'Heater':
            utility = process.asp.get_heater_util(uid)
            if utility == 'CW':
                coolwater = Coolwater(block.Name, uid, process)
                process.coolwater[uid] = coolwater
            elif utility == 'RF1':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant1[uid] = refrig
            elif utility == 'RF2':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant2[uid] = refrig
            elif utility == 'RF3':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant3[uid] = refrig
            elif utility == 'RF4':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant4[uid] = refrig
            elif utility == 'LLPS':
                llpsteam = LLP_Steam(block.Name, uid, process)
                process.llpsteam[uid] = llpsteam
            elif utility == 'LLPS-GEN':
                llpsgen = LLPS_Gen(block.Name, uid, process)
                process.llpsgen[uid] = llpsgen
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, uid, process)
                process.lpsteam[uid] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, uid, process)
                process.lpsgen[uid] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, uid, process)
                process.mpsteam[uid] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, uid, process)
                process.mpsgen[uid] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, uid, process)
                process.hpsteam[uid] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, uid, process)
                process.hpsgen[uid] = hpsgen
    

    def assign_utility_pressure(self, block, block_type, process):
        # Assign utilities of pumps, compressors and multistage compressors
        uid = self.uid + block.Name
        if block_type == 'Pump':
            utility = process.asp.get_pump_util(uid)
            if utility == 'ELECTRIC':
                electricity = Electricity(block.Name, uid, process)
                process.electricity[uid] = electricity
        elif block_type == 'Compr':
            utility = process.asp.get_compr_util(uid)
            if utility == 'ELECTRIC':
                electricity = Electricity(block.Name, uid, process)
                process.electricity[uid] = electricity

        elif block_type == 'MCompr':
            utility = process.asp.get_mcompr_specs_util(uid)
            if 'ELECTRIC' in utility:
                electricity = Electricity(block.Name, uid, process)
                process.electricity[uid] = electricity

            utility = process.asp.get_mcompr_cool_util(uid)
            if 'CW' in utility:
                coolwater = Coolwater(block.Name, uid, process)
                process.coolwater[uid] = coolwater
            elif 'RF1' in utility:
                refrigerant = Refrigerant(block.Name, uid, process)
                process.refrigerant1[uid] = refrigerant
            elif 'RF2' in utility:
                refrigerant = Refrigerant(block.Name, uid, process)
                process.refrigerant2[uid] = refrigerant
            elif 'RF3' in utility:
                refrigerant = Refrigerant(block.Name, uid, process)
                process.refrigerant3[uid] = refrigerant
            elif 'RF4' in utility:
                refrigerant = Refrigerant(block.Name, uid, process)
                process.refrigerant4[uid] = refrigerant


    def assign_utility_reactor(self, block, block_type, process):
        # Assign reactor utilities
        uid = self.uid + block.Name
        if block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs':
            utility = process.asp.get_reactor_util(uid)
            if utility == 'CW':
                coolwater = Coolwater(block.Name, uid, process)
                process.coolwater[uid] = coolwater
            elif utility == 'RF1':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant1[uid] = refrig
            elif utility == 'RF2':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant2[uid] = refrig
            elif utility == 'RF3':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant3[uid] = refrig
            elif utility == 'RF4':
                refrig = Refrigerant(block.Name, uid, process)
                process.refrigerant4[uid] = refrig
            elif utility == 'LLPS':
                llpsteam = LLP_Steam(block.Name, uid, process)
                process.llpsteam[uid] = llpsteam
            elif utility == 'LLPS-GEN':
                llpsgen = LLPS_Gen(block.Name, uid, process)
                process.llpsgen[uid] = llpsgen
            elif utility == 'LPS':
                lpsteam = LP_Steam(block.Name, uid, process)
                process.lpsteam[uid] = lpsteam
            elif utility == 'LPS-GEN':
                lpsgen = LPS_Gen(block.Name, uid, process)
                process.lpsgen[uid] = lpsgen
            elif utility == 'MPS':
                mpsteam = MP_Steam(block.Name, uid, process)
                process.mpsteam[uid] = mpsteam
            elif utility == 'MPS-GEN':
                mpsgen = MPS_Gen(block.Name, uid, process)
                process.mpsgen[uid] = mpsgen
            elif utility == 'HPS':
                hpsteam = HP_Steam(block.Name, uid, process)
                process.hpsteam[uid] = hpsteam
            elif utility == 'HPS-GEN':
                hpsgen = HPS_Gen(block.Name, uid, process)
                process.hpsgen[uid] = hpsgen