from .streams import (
    Material, Material_MIXCISLD, Material_MCINCPSD,
    Work, 
    Heat
    )
from .output import Output
from .utilities import (
    Electricity_Block,
    Coolwater_Block,
    Steam_Block,
    Steam_Gen_Block,
    Refrigerant_Block,
    Gas_Block
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
    SolidsSeparator,

    Compr,
    MCompr,
    Pump,
    Mixer,
    Fsplit,
    Flash2,
    Flash3,
    Decanter,
    Separator1,
    Heater,
    HeatX,
    RadFrac,
    RGibbs,
    RPlug,
    RStoic,
    RYield
)



class Flowsheet(object):
    """Aspen flowsheet object"""
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
        """Load the simulation of the current Aspen flowsheet"""
        # Assign dictionaries for each block and stream
        blocks = process.asp.get_block_list(self.uid)
        streams = process.asp.get_stream_list(self.uid)
        
        # Load and fill block dictionaries
        # Block functionality is Work in Progress  
        '''for obj in blocks.Elements:'''
        for obj in blocks:
            uid = self.uid+obj.Name
            block_type = process.asp.get_block_type(uid)
            '''
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
            '''

            if block_type == 'Mixer':
                temp = Mixer(block_type, obj.Name, uid, process)
                process.mixer[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Fsplit':
                temp = Fsplit(block_type, obj.Name, uid, process)
                process.fsplit[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Heater':
                temp = Heater(block_type, obj.Name, uid, process)
                process.heater[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_heater(obj, process)
            elif block_type == 'HeatX':
                temp = HeatX(block_type, obj.Name, uid, process)
                process.heatx[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'RadFrac':
                temp = RadFrac(block_type, obj.Name, uid, process)
                process.radfrac[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_radfrac(obj, process)
            elif block_type == 'Compr':
                temp = Compr(block_type, obj.Name, uid, process)
                process.compr[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_compr(obj, process)
            elif block_type == 'MCompr':
                temp = MCompr(block_type, obj.Name, uid, process)
                process.mcompr[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_mcompr(obj, process)
            elif block_type == 'Pump':
                temp = Pump(block_type, obj.Name, uid, process)
                process.pump[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_pump(obj, process)
            elif block_type == 'Flash2':
                temp = Flash2(block_type, obj.Name, uid, process)
                process.flash2[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Flash3':
                temp = Flash3(block_type, obj.Name, uid, process)
                process.flash3[uid] = temp  
                process.blocks[uid] = temp
            elif block_type == 'Decanter':
                temp = Decanter(block_type, obj.Name, uid, process)
                process.decanter[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Sep':
                temp = Separator1(block_type, obj.Name, uid, process)
                process.sep[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'RGibbs':
                temp = RGibbs(block_type, obj.Name, uid, process)
                process.rgibbs[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'RPlug':
                temp = RPlug(block_type, obj.Name, uid, process)
                process.rplug[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'RStoic':
                temp = RStoic(block_type, obj.Name, uid, process)
                process.rstoic[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'RYield':
                temp = RYield(block_type, obj.Name, uid, process)
                process.ryield[uid] = temp
                process.blocks[uid] = temp
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
                material_stream_type = process.aspen.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\SCLASS").Value
                if material_stream_type == 'CONVEN':
                    material = Material(obj.Name, uid, process)
                    process.streams[uid] = material
                    process.material_streams[uid] = material
                elif material_stream_type == 'MIXCISLD':
                    material = Material_MIXCISLD(obj.Name, uid, process)
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
                

    def assign_utility_radfrac(self, block, process):
        # Assign radfrac utilities
        uid = self.uid + block.Name
        util_name = process.asp.get_radfrac_cond_util(uid)
        try: 
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else: 
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)
        
        util_name = process.asp.get_radfrac_reb_util(uid)
        try: 
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else: 
            if util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)

    def assign_utility_heater(self, block, process):
        # Assign heater utilities
        uid = self.uid + block.Name
        util_name = process.asp.get_heater_util(uid)
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)

    def assign_utility_compr(self, block, process):
        uid = self.uid + block.Name
        util_name = process.asp.get_compr_util(uid)
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)


    def assign_utility_mcompr(self, block, process):
        uid = self.uid + block.Name
        util_name = process.asp.get_mcompr_specs_util(uid)[0]
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)

        util_name = process.asp.get_mcompr_cool_util(uid)[0]
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)


    def assign_utility_pump(self, block, process):
        uid = self.uid + block.Name
        util_name = process.asp.get_pump_util(uid)
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)


    def assign_utility_rgibbs(self, block, process):
        uid = self.uid + block.Name
        util_name = process.asp.get_reactor_util(uid)
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)

    def assign_utility_rstoic(self, block, process):
        uid = self.uid + block.Name
        util_name = process.asp.get_reactor_util(uid)
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)
    
    def assign_utility_ryield(self, block, process):
        uid = self.uid + block.Name
        util_name = process.asp.get_reactor_util(uid)
        try:
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)


'''
    def assign_utility_column(self, block, block_type, process):
        # Assign column utilities
        uid = self.uid + block.Name
        if block_type == 'RadFrac':
            util_name = process.asp.get_radfrac_cond_util(uid)
            try: 
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else: 
                if util_type == 'WATER':
                    process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
                elif util_type == 'STEAM':
                    steam_type = process.asp.get_steam_type(util_name)
                    if steam_type == 'STEAM':
                        process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                    elif steam_type == 'STEAM-GEN':
                        process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
                elif util_type == 'REFRIGERATIO':
                    process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)

            util_name = process.asp.get_radfrac_reb_util(uid)
            try: 
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else: 
                if util_type == 'STEAM':
                    steam_type = process.asp.get_steam_type(util_name)
                    if steam_type == 'STEAM':
                        process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                    elif steam_type == 'STEAM-GEN':
                        process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
                elif util_type == 'GAS':
                    process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)


    def assign_utility_heater(self, block, block_type, process):
        # Assign heater utilities
        uid = self.uid + block.Name
        if block_type == 'Heater':
            util_name = process.asp.get_heater_util(uid)
            try:
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else:
                if util_type == 'WATER':
                    process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
                elif util_type == 'ELECTRICITY':
                    process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
                elif util_type == 'GAS':
                    process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)
                elif util_type == 'STEAM':
                    steam_type = process.asp.get_steam_type(util_name)
                    if steam_type == 'STEAM':
                        process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                    elif steam_type == 'STEAM-GEN':
                        process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
                elif util_type == 'REFRIGERATIO':
                    process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)
    

    def assign_utility_pressure(self, block, block_type, process):
        # Assign utilities of pumps, compressors and multistage compressors
        uid = self.uid + block.Name
        if block_type == 'Pump':
            util_name = process.asp.get_pump_util(uid)
            try:
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else:
                if util_type == 'ELECTRICITY':
                    process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
        
        elif block_type == 'Compr':
            util_name = process.asp.get_compr_util(uid)
            try:
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else:
                if util_type == 'ELECTRICITY':
                    process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
        
        elif block_type == 'MCompr':
            util_name = process.asp.get_mcompr_specs_util(uid)[0]
            try:
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else:
                if util_type == 'ELECTRICITY':
                    process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)

            util_name = process.asp.get_mcompr_cool_util(uid)[0]
            try:
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else:
                if util_type == 'WATER':
                    process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
                elif util_type == 'REFRIGERATIO':
                    process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)

    def assign_utility_reactor(self, block, block_type, process):
        # Assign reactor utilities
        uid = self.uid + block.Name
        if block_type == 'RStoic' or block_type == 'RYield' or block_type == 'RGibbs':
            util_name = process.asp.get_reactor_util(uid)
            try:
                util_type = process.asp.get_util_type(util_name)
            except TypeError:
                pass
            else:
                if util_type == 'WATER':
                    process.coolwater[util_name].blocks[uid] = Coolwater_Block(util_name, uid, process)
                elif util_type == 'ELECTRICITY':
                    process.electricity[util_name].blocks[uid] = Electricity_Block(util_name, uid, process)
                elif util_type == 'GAS':
                    process.natural_gas[util_name].blocks[uid] = Gas_Block(util_name, uid, process)
                elif util_type == 'STEAM':
                    steam_type = process.asp.get_steam_type(util_name)
                    if steam_type == 'STEAM':
                        process.steam[util_name].blocks[uid] = Steam_Block(util_name, uid, process)
                    elif steam_type == 'STEAM-GEN':
                        process.steam_gen[util_name].blocks[uid] = Steam_Gen_Block(util_name, uid, process)
                elif util_type == 'REFRIGERATIO':
                    process.refrigerant[util_name].blocks[uid] = Refrigerant_Block(util_name, uid, process)
'''