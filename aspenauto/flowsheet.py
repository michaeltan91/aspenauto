"""Contains the structure and data retrieval from an Aspen Plus model flowsheet"""
from .streams import (
    Material, MaterialMIXCISLD, MaterialMCINCPSD, MaterialMIXCIPSD, MaterialMIXNC,
    Work,
    Heat
    )
from .utilities import (
    ElectricityBlock,
    CoolwaterBlock,
    SteamBlock,
    SteamGenBlock,
    RefrigerantBlock,
    GasBlock,
    FiredHeatBlock
)

from .blocks import (
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
            # In case the current flowsheet is the main flowsheet of the simulation
            if name == 'Main':
                self.uid = ''
                self.base_path = path
            # In case the current flowsheet is the first flowsheet inside a hierarcy block
            else:
                self.uid = self.name+'.'
                self.base_path = path+str(name)
        # In case the current flowsheet is a hierarchy block inside a hierarchy block
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
        for obj in blocks:
            # Assign an ID to the block, if the block is located in hierarchy block
            # the ID of the block is a combination of the hierarchy block ID and the block name
            # separated by a '.'
            # For each type of aspen block, there is a Python class
            uid = self.uid+obj.Name
            block_type = process.asp.get_block_type(uid)

            if block_type == 'Mixer':
                # Assign the Mixer class to the aspen block
                temp = Mixer(block_type, obj.Name, uid, process)
                process.mixer[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Fsplit':
                # Assign the Fsplit class to the aspen block
                temp = Fsplit(block_type, obj.Name, uid, process)
                process.fsplit[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Heater':
                # Assign the Heater class to the aspen block
                temp = Heater(block_type, obj.Name, uid, process)
                process.heater[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_heater(obj, process)
            elif block_type == 'HeatX':
                # Assign the HeatX class to the aspen block
                temp = HeatX(block_type, obj.Name, uid, process)
                process.heatx[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'RadFrac':
                # Assign the RadFrac class to the aspen block
                temp = RadFrac(block_type, obj.Name, uid, process)
                process.radfrac[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_radfrac(obj, process)
            elif block_type == 'Compr':
                # Assign the Compr class to the aspen block
                temp = Compr(block_type, obj.Name, uid, process)
                process.compr[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_compr(obj, process)
            elif block_type == 'MCompr':
                # Assign the MCompr class to the aspen block
                temp = MCompr(block_type, obj.Name, uid, process)
                process.mcompr[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_mcompr(obj, process)
            elif block_type == 'Pump':
                # Assign the Pump class to the aspen block
                temp = Pump(block_type, obj.Name, uid, process)
                process.pump[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_pump(obj, process)
            elif block_type == 'Flash2':
                # Assign the Flash2 class to the aspen block
                temp = Flash2(block_type, obj.Name, uid, process)
                process.flash2[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_flash2(obj, process)
            elif block_type == 'Flash3':
                # Assign the Flash3 class to the aspen block
                temp = Flash3(block_type, obj.Name, uid, process)
                process.flash3[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Decanter':
                # Assign the Decanter class to the aspen block
                temp = Decanter(block_type, obj.Name, uid, process)
                process.decanter[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'Sep':
                # Assign the Separator1 class to the aspen block
                temp = Separator1(block_type, obj.Name, uid, process)
                process.sep[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_sep(obj, process)
            elif block_type == 'RGibbs':
                # Assign the RGibbs class to the aspen blocck
                temp = RGibbs(block_type, obj.Name, uid, process)
                process.rgibbs[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_rgibbs(obj, process)
            elif block_type == 'RPlug':
                # Assign the RPlug class to the aspen block
                temp = RPlug(block_type, obj.Name, uid, process)
                process.rplug[uid] = temp
                process.blocks[uid] = temp
            elif block_type == 'RStoic':
                # Assign the RStoic class to the aspen block
                temp = RStoic(block_type, obj.Name, uid, process)
                process.rstoic[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_rstoic(obj, process)
            elif block_type == 'RYield':
                # Assign the RYield class to the aspen block
                temp = RYield(block_type, obj.Name, uid, process)
                process.ryield[uid] = temp
                process.blocks[uid] = temp
                self.assign_utility_ryield(obj, process)
            elif block_type == 'Hierarchy' or block_type == 'HIERARCHY':
                # Assign the Flowsheet class to the aspen block in case of a hierarchy block
                base_path = self.base_path+'\\Data\\Blocks\\'
                hierarchy = Flowsheet(process, path = base_path ,name =obj.Name, uid = self.uid)
                process.hierarchy[uid] = hierarchy
                process.blocks[uid] = hierarchy



        # Load and fill stream dictionaries
        # Iterate over all the streams in the aspen simulation
        for obj in streams:
            # Assign an ID to the stream, if the stream is located in hierarchy block
            # the ID of the stream is a combination of the hierarchy block ID and the stream name
            # separated by a '.'
            uid = self.uid+obj.Name
            stream_type = process.asp.get_stream_type(uid)

            # In case the stream is material stream
            if stream_type == 'MATERIAL':
                # Retrieve the general stream class of the aspen simulation and
                # assign material stream classes accordingly
                material_stream_type = process.aspen.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\SCLASS").Value
                if material_stream_type == 'CONVEN':
                    material = Material(obj.Name, uid, process)
                    process.streams[uid] = material
                    process.material_streams[uid] = material
                elif material_stream_type == 'MIXCISLD':
                    material = MaterialMIXCISLD(obj.Name, uid, process)
                    process.streams[uid] = material
                    process.material_streams[uid] = material
                elif material_stream_type == 'MCINCPSD':
                    material = MaterialMCINCPSD(obj.Name, uid, process)
                    process.streams[uid] = material
                    process.material_streams[uid] = material
                elif material_stream_type == 'MIXCIPSD':
                    material = MaterialMIXCIPSD(obj.Name, uid, process)
                    process.streams[uid] = material
                    process.material_streams[uid] = material
                elif material_stream_type == 'MIXNC':
                    material = MaterialMIXNC(obj.Name, uid, process)
                    process.streams[uid] = material
                    process.material_streams[uid] = material

            #
            elif stream_type == 'WORK':
                work = Work(obj.Name, uid, process)
                process.work_streams[uid] = work
                process.streams[uid] = work
            elif stream_type == 'HEAT':
                heat = Heat(obj.Name, uid, process)
                process.streams[uid] = heat
                process.heat_streams[uid] = heat


    def assign_utility_radfrac(self, block, process):
        '''Assign utilities to a RadFrac column'''

        # Assign an ID to the RadFrac block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the condensor utility
        util_name = process.asp.get_radfrac_cond_util(uid)
        try:
            # Retrieve the type of condensor utility
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, \
                    uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)

        # Retrieve the name of the reboiler utility
        util_name = process.asp.get_radfrac_reb_util(uid)
        try:
            # Retrieve the type of the reboiler utility
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, uid, \
                    process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = GasBlock(util_name, uid, process)


    def assign_utility_heater(self, block, process):
        '''Assign a utility to a Heater (heat exchanger)'''

        # Assign an ID to the Heater block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the heater utility
        util_name = process.asp.get_heater_util(uid)
        try:
            # Retrieve the type of the heater utility
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, uid, \
                process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = GasBlock(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, \
                    uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)
            elif util_type == "GENERAL" and util_name == "FIRINGH":
                process.fired_heat[util_name].blocks[uid] = FiredHeatBlock(util_name, \
                uid, process)


    def assign_utility_compr(self, block, process):
        '''Assign a utility to a Compr block'''

        # Assign an ID to the Compr block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the compressor utility
        util_name = process.asp.get_compr_util(uid)
        try:
            # Retrieve the type of the compressor utility
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, \
                uid, process)


    def assign_utility_mcompr(self, block, process):
        '''Assign utilities to a MCompr block'''

        # Assign an ID to the MCompr block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the main utility of the multistage compressor
        util_name = process.asp.get_mcompr_specs_util(uid)[0]
        try:
            # Retrieve the type of the main utility of the multistage compressor
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, \
                uid, process)

        # Retrieve the name of the cooling duty of the multistage compressor
        util_name = process.asp.get_mcompr_cool_util(uid)[0]
        try:
            # Retrieve the type of the cooling duty of the multistage compressor
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)


    def assign_utility_pump(self, block, process):
        '''Assign a utility to the Pump block'''

        # Assign an ID to the Pump block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the utility of the pump
        util_name = process.asp.get_pump_util(uid)
        try:
            # Retrieve the type of utility of the pump
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, \
                uid, process)


    def assign_utility_flash2(self, block, process):
        '''Assign a utility to the Flash2 block'''

        uid = self.uid + block.name

        util_name = process.asp.get_flash2_util(uid)
        try:
            # Retrieve the type of the utility of the flash2
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, uid, \
                process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = GasBlock(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, \
                    uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)


    def assign_utility_sep(self, block, process):
        '''Assign a utility to the separator block'''

        uid = self.uid + block.name

        util_name = process.asp.get_sep_util(uid)
        try:
            # Retrieve the type of the utility of the separator
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, uid, \
                process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = GasBlock(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, \
                    uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)


    def assign_utility_rgibbs(self, block, process):
        '''Assign a utility to the RGibbs block'''

        # Assign an ID to the RGibbs block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the RGibbs reactor
        util_name = process.asp.get_reactor_util(uid)
        try:
            # Retrieve the type of the utility of the RGibbs reactor
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, \
                uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = GasBlock(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, \
                    uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)


    def assign_utility_rstoic(self, block, process):
        '''Assign a utility to the RStoic block'''

        # Assign an ID to the RStoic block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the utility of the RStoic reactor
        util_name = process.asp.get_reactor_util(uid)
        try:
            # Retrieve the type of the utility of the RStoic reactor
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, \
                uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, \
                uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = GasBlock(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, \
                    uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)


    def assign_utility_ryield(self, block, process):
        '''Assign a utility to the RYield block'''

        # Assign an ID to the RYield block, if the block is located in hierarchy block
        # the ID of the block is a combination of the hierarchy block ID and the block name
        # separated by a '.'
        uid = self.uid + block.Name

        # Retrieve the name of the utility of the RYield reactor
        util_name = process.asp.get_reactor_util(uid)
        try:
            # Retrieve the type of the utility of the RYield reactor
            util_type = process.asp.get_util_type(util_name)
        except TypeError:
            pass
        else:
            if util_type == 'WATER':
                process.coolwater[util_name].blocks[uid] = CoolwaterBlock(util_name, \
                uid, process)
            elif util_type == 'ELECTRICITY':
                process.electricity[util_name].blocks[uid] = ElectricityBlock(util_name, \
                uid, process)
            elif util_type == 'GAS':
                process.natural_gas[util_name].blocks[uid] = GasBlock(util_name, uid, process)
            elif util_type == 'STEAM':
                steam_type = process.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    process.steam[util_name].blocks[uid] = SteamBlock(util_name, uid, process)
                elif steam_type == 'STEAM-GEN':
                    process.steam_gen[util_name].blocks[uid] = SteamGenBlock(util_name, \
                    uid, process)
            elif util_type == 'REFRIGERATIO':
                process.refrigerant[util_name].blocks[uid] = RefrigerantBlock(util_name, \
                uid, process)
