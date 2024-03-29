"""This is the file with specific methods for retrieving aspen plus object values"""
from epynet import ObjectCollection

class ASP(object):
    '''Aspen Plus Python object'''
    block = '\\Data\\Blocks\\'
    stream = '\\Data\\Streams\\'
    utility = '\\Data\\Utilities\\'
    setup = '\\Data\\Setup\\'

    def __init__(self, process):

        self.aspen = process.aspen


    def get_comp_list(self):
        
        path = "\\Data\\Components\\Specifications\\Output\\REPNAME"
        return [obj.Value for obj in self.aspen.Tree.FindNode(path).Elements]


    def get_run_error(self):
        """Retrieve the Aspen Plus error status"""
        raise NotImplementedError


    def get_run_error_mess(self):
        """Retrieve the Aspen Plus error message"""
        raise NotImplementedError


    def get_block_list(self, uid):
        '''Returns a list of all the blocks of the current aspen flowsheet'''
        if uid == '':
            path = self.block
        else:
            uids = uid.split('.')
            temp_path = [self.block+name for name in uids[:-1]]
            temp_path.extend(self.block)
            path=''.join(temp_path)
        return [obj for obj in self.aspen.Tree.FindNode(path).Elements]


    def get_block_type(self, uid):
        '''Returns the type of the block'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).AttributeValue(6)


    def get_block_value(self, uid, prop):
        '''Returns the value of a block property'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend([prop])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_block_value_frac(self, uid, prop):
        '''Returns the fractional values of a block property'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend([prop])
        path=''.join(temp_path)
        temp = ObjectCollection()
        for element in self.aspen.Tree.FindNode(path).Elements:
            temp[element.Name] = element.Value
        return temp


    def set_block_value(self, uid, prop, value):
        '''Sets the value of a block property in the aspen simulation'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend([prop[0]])
        path=''.join(temp_path)
        if self.aspen.Tree.FindNode(path).AttributeValue(13) is not prop[1]:
            self.aspen.Tree.FindNode(path).SetAttributeValue(13,0,prop[1])
        self.aspen.Tree.FindNode(path).Value = value


    def get_stream_list(self, uid):
        '''Returns a list of all the streams of the current aspen flowsheet'''
        if uid == '':
            path = self.stream
        else:
            uids = uid.split('.')
            temp_path = [self.block+name for name in uids[:-1]]
            temp_path.extend(self.stream)
            path=''.join(temp_path)
        return [obj for obj in self.aspen.Tree.FindNode(path).Elements]


    def get_stream_type(self, uid):
        '''Returns the type of the stream'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1]])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).AttributeValue(6)


    def get_stream_value(self, uid, prop):
        '''Returns the value of a stream property'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_stream_value_frac(self, uid, prop):
        '''Returns the value of a fractional stream property'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop])
        path=''.join(temp_path)
        temp = ObjectCollection()
        for element in self.aspen.Tree.FindNode(path).Elements:
            temp[element.Name] = element.Value
        return temp


    def set_stream_value(self, uid, prop, value):
        '''Sets the value of a stream property in the aspen simulation'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop[0]])
        path=''.join(temp_path)
        if self.aspen.Tree.FindNode(path).AttributeValue(13) is not prop[1]:
            self.aspen.Tree.FindNode(path).SetAttributeValue(13,0,prop[1])
        self.aspen.Tree.FindNode(path).Value = value


    def set_stream_value_frac(self, uid, prop, value):
        '''Sets the value of a fractional stream property in the aspen simulation'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop[0]])
        path=''.join(temp_path)

        if self.aspen.Tree.FindNode(path).AttributeValue(13) is not prop[1]:
            self.aspen.Tree.FindNode(path).SetAttributeValue(13,0,prop[1])

        temp1 = {}
        temp2 = value
        for element in self.aspen.Tree.FindNode(path).Elements:
            temp1[element.Name] = element.Value

        dict3 = {**temp1, **temp2}
        for key, value in dict3.items():
            if key in temp1 and key in temp2:
                dict3[key] = value
                self.aspen.Tree.FindNode(path+'\\'+key).Value = value
            elif key in temp1 and key not in temp2:
                dict3[key] = 0
                self.aspen.Tree.FindNode(path+'\\'+key).Value = 0
            elif key not in temp1 and key in temp2:
                raise AttributeError('Component not defined in Aspen simulation', key)


    def get_stream_special_flow(self, uid, prop, flowtype):
        '''Return the value of a material stream property that is not of stream class "CONVEN"'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop, flowtype])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_stream_special_value(self, uid, prop):
        '''Return the value of a material stream property that is not of stream class "CONVEN"'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop])
        path=''.join(temp_path)
        temp = ObjectCollection()
        for element in self.aspen.Tree.FindNode(path).Elements:
            if element.Value is None:
                temp[element.Name] = 0
            else:
                temp[element.Name] = element.Value
        return temp


    def get_stream_special_value_frac(self, uid, prop):
        '''Return the value of a material stream property that is not of stream class "CONVEN"'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop])
        path=''.join(temp_path)
        temp1 = ObjectCollection()
        for element1 in self.aspen.Tree.FindNode(path).Elements:
            temp2 = ObjectCollection()
            for element2 in element1.Elements:
                value2 = element2.Value
                if value2 is None:
                    temp2[element2.Name] = 0
                else:
                    temp2[element2.Name] = element2.Value
            temp1[element1.Name] = temp2
        return temp1


    def get_utility_list(self):
        '''Returns a list of the utilities of the aspen simulation'''
        path = self.utility
        return [obj for obj in self.aspen.Tree.FindNode(path).Elements]


    def get_util_type(self, util_name):
        '''Returns the utility type'''
        loc = '\\Input\\UTILITY_TYPE'
        temp_path = [self.utility, util_name,loc]
        path = ''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_util_value(self, util_name, prop):
        '''Returns the value of a utility property'''
        temp_path = [self.utility, util_name, prop]
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def set_util_value(self, util_name, prop, value):
        """Set the utitility property value"""
        raise NotImplementedError


    def get_util_block_value(self, util_name, uid, prop):
        '''Returns the value of a utility block property'''
        # Blocks using the utility
        temp_path = [self.utility, util_name, prop, uid]
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def set_util_block_value(self, util_name, uid, prop, value):
        """Set the utility block property value"""
        raise NotImplementedError


    def get_steam_type(self, util_name):
        '''Return the type of steam utility, utilization or production'''
        vfracin = '\\Input\\VFRAC'
        vfracout = '\\Input\\VFRAC_OUT'
        temp_path1 = [self.utility, util_name, vfracin]
        temp_path2 = [self.utility, util_name, vfracout]
        path1 = ''.join(temp_path1)
        path2 = ''.join(temp_path2)

        if self.aspen.Tree.FindNode(path1).Value == 0:
            return 'STEAM-GEN'
        elif self.aspen.Tree.FindNode(path2).Value == 0:
            return 'STEAM'




    def get_heater_util(self, uid):
        '''Returns the utility of a heater'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_radfrac_cond_util(self, uid):
        '''Returns the utility of a radfrac condensor'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\CONDENSER')
        path=''.join(temp_path)
        condenser_type = self.aspen.Tree.FindNode(path).Value

        if condenser_type == 'NONE':
            return

        else:
            temp_path = [self.block+name for name in uids]
            temp_path.extend('\\Input\\COND_UTIL')
            path=''.join(temp_path)
            return self.aspen.Tree.FindNode(path).Value


    def get_radfrac_reb_util(self, uid):
        '''Returns the utility of a radfrac reboiler'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\REBOILER')
        path=''.join(temp_path)
        reboiler_type = self.aspen.Tree.FindNode(path).Value

        if reboiler_type == 'NONE':
            return

        else:
            temp_path = [self.block+name for name in uids]
            temp_path.extend('\\Input\\REB_UTIL')
            path=''.join(temp_path)
            return self.aspen.Tree.FindNode(path).Value


    def get_reactor_util(self, uid):
        '''Returns the utility of a reactor'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_pump_util(self, uid):
        '''Returns the utility of a pump'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_flash2_util(self, uid):
        '''Returns the utility of flash2'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_sep_util(self, uid):
        '''Returns the utility of seperator'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_compr_util(self, uid):
        '''Returns the utility of a compressor'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_mcompr_specs_util(self, uid):
        '''Returns the main utility of a multistage compressor'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\SPECS_UTL')
        path=''.join(temp_path)
        stages = self.aspen.Tree.FindNode(path).Elements
        return [stage.Value for stage in stages]


    def get_mcompr_cool_util(self, uid):
        '''Returns the cooling utility of a multistage compressor'''
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\COOLER_UTL')
        path=''.join(temp_path)
        stages = self.aspen.Tree.FindNode(path).Elements
        return [stage.Value for stage in stages]


    def get_simulation_unit_set(self):
        """Retrieve the Aspen Plus model unit set"""
        temp_path = [self.setup]
        temp_path.extend('Sim-Options\\Input\\Unit Set')
        path =''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value

    def get_simulation_units(self, unit_set, prop):
        """Retrieve the Aspen Plus model units"""
        temp_path = [self.setup]
        temp_path.extend(['Units-Sets\\',unit_set,'\\Unit-Types',prop])
        path =''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value
