from .objectcollection import ObjectCollection

class ASP(object):

    block = '\\Data\\Blocks\\'
    stream = '\\Data\\Streams\\'
    utility = '\\Data\\Utilities\\'
    setup = '\\Data\\Setup\\'
    
    def __init__(self, process):

        self.aspen = process.aspen


    def get_run_error(self):
        return

    
    def get_run_error_mess(self):
        return


    def get_block_list(self, uid):
        if uid == '':
            path = self.block
        else:
            uids = uid.split('.')
            temp_path = [self.block+name for name in uids[:-1]]
            temp_path.extend(self.block)
            path=''.join(temp_path)
        return [obj for obj in self.aspen.Tree.FindNode(path).Elements]


    def get_block_type(self, uid):
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).AttributeValue(6)

    
    def get_block_value(self, uid, prop):
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend([prop])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value
    

    def get_block_value_frac(self, uid, prop):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend([prop])
        path=''.join(temp_path)
        temp = ObjectCollection()
        for element in self.aspen.Tree.FindNode(path).Elements:
            temp[element.Name] = element.Value 
        return temp


    def set_block_value(self, uid, prop, value):
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend([prop[0]])
        path=''.join(temp_path)
        if self.aspen.Tree.FindNode(path).AttributeValue(13) is not prop[1]:
            self.aspen.Tree.FindNode(path).SetAttributeValue(13,0,prop[1])
        self.aspen.Tree.FindNode(path).Value = value


    def get_stream_list(self, uid):
        if uid == '':
            path = self.stream
        else:
            uids = uid.split('.')
            temp_path = [self.block+name for name in uids[:-1]]
            temp_path.extend(self.stream)
            path=''.join(temp_path)
        return [obj for obj in self.aspen.Tree.FindNode(path).Elements]

    
    def get_stream_type(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1]])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).AttributeValue(6)


    def get_stream_value(self, uid, prop):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_stream_value_frac(self, uid, prop):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop])
        path=''.join(temp_path)
        temp = ObjectCollection()
        for element in self.aspen.Tree.FindNode(path).Elements:
            temp[element.Name] = element.Value 
        return temp


    def set_stream_value(self, uid, prop, value):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop[0]])
        path=''.join(temp_path)
        if self.aspen.Tree.FindNode(path).AttributeValue(13) is not prop[1]:
            self.aspen.Tree.FindNode(path).SetAttributeValue(13,0,prop[1])
        self.aspen.Tree.FindNode(path).Value = value   


    def set_stream_value_frac(self, uid, prop, value):

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
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop, flowtype])
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_stream_special_value_frac(self, uid, prop):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids[:-1]]
        temp_path.extend([self.stream,uids[-1],prop])
        path=''.join(temp_path)
        temp1 = ObjectCollection()
        for element1 in self.aspen.Tree.FindNode(path).Elements:
            temp2 = ObjectCollection()
            for element2 in element1.Elements:
                temp2[element2.Name] = element2.Value
            temp1[element1.Name] = temp2 
        return temp1


    def get_utility_list(self):
        path = self.utility
        return [obj for obj in self.aspen.Tree.FindNode(path).Elements]


    def get_util_type(self, util_name):
        loc = '\\Input\\UTILITY_TYPE'
        temp_path = [self.utility, util_name,loc]
        path = ''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_util_value(self, util_name, prop):
        temp_path = [self.utility, util_name, prop]
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value

    
    def set_util_value(self, util_name, prop, value):
        return

    
    def get_util_block_value(self, util_name, uid, prop):
        temp_path = [self.utility, util_name, prop, uid]
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def set_util_block_value(self, util_name, uid, prop, value):
        return


    def get_steam_type(self, util_name):
        vfracin = '\\Input\\VFRAC'
        vfracout = '\\Input\\VFRAC_OUT'
        temp_path1 = [self.utility, util_name, vfracin]
        temp_path2 = [self.utility, util_name, vfracout]
        path1 = ''.join(temp_path1)
        path2 = ''.join(temp_path2)
        self.aspen.Tree.FindNode(path1).Value
        if self.aspen.Tree.FindNode(path1).Value == 0:
            return 'STEAM-GEN'
        elif self.aspen.Tree.FindNode(path2).Value == 0:
            return 'STEAM'




    def get_heater_util(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value
    

    def get_radfrac_cond_util(self, uid):
        
        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\COND_UTIL')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_radfrac_reb_util(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\REB_UTIL')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_reactor_util(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value

    
    def get_pump_util(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value


    def get_compr_util(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\UTILITY_ID')
        path=''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value

    
    def get_mcompr_specs_util(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\SPECS_UTL')
        path=''.join(temp_path)
        stages = self.aspen.Tree.FindNode(path).Elements
        return [stage.Value for stage in stages]


    def get_mcompr_cool_util(self, uid):

        uids = uid.split('.')
        temp_path = [self.block+name for name in uids]
        temp_path.extend('\\Input\\COOLER_UTL')
        path=''.join(temp_path)
        stages = self.aspen.Tree.FindNode(path).Elements
        return [stage.Value for stage in stages]

    

    def get_simulation_unit_set(self):
        temp_path = [self.setup]
        temp_path.extend('Sim-Options\\Input\\Unit Set')
        path =''.join(temp_path)
        return self.aspen.Tree.FindNode(path).Value

    def get_simulation_units(self, unit_set, prop):
        temp_path = [self.setup]
        temp_path.extend(['Units-Sets\\',unit_set,'\\Unit-Types',prop])
        path =''.join(temp_path)      
        return self.aspen.Tree.FindNode(path).Value
    

