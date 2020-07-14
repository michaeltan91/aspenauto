from .objectcollection import ObjectCollection
import weakref

class Units(object):

    unit_init = {
        'density': '\\DENSITY',
        'energy': '\\ENERGY',
        'enthalpy': '\\ENTHALPY',
        'entropy': '\\ENTROPY',
        'massflow': '\\MASS-FLOW',
        'moleflow': '\\MOLE-FLOW',
        'volflow': '\\VOLUME-FLOW',
        'duty': '\\ENTHALPY-FLO',
        'power': '\\POWER',
        'pressure': '\\PRESSURE',
        'temperature': '\\TEMPERATURE'
    } 

    unit_dict = {
        'density':  {
            'kg/cum': 1,
            'gm/cc': 3,
            'gm/cum': 4
        },
        'energy': {
            'J': 1,
            'cal': 3,
            'kcal': 4,
            'kWhr': 5,
            'GJ': 7,
            'kJ': 8,
            'N-m': 9,
            'MJ': 10,
            'Mcal': 11,
            'Gcal': 12
        },
        'enthalpy': {
            'J/kmol': 1,
            'cal/mol': 3,
            'J/kg': 4,
            'cal/gm': 6
        },
        'entropy' : {
            'J/lmol-K': 1,
            'cal/mol-K': 3,
            'J/kg-K': 4,
            'cal/gm-K': 6,
            'MJ/kmol-K': 7,
            'kcal/kmol-K': 8,
            'Gcal/kmol-K': 9,
            'kJ/mol-K': 11,
            'kJ/kmol-K': 12
        },
        'massflow': {
            'kg/hr': 3,
            'tons/day': 6,
            'gm/sec': 7,
            'tonne/hr': 8,
            'kg/day': 10,
            'tonne/year': 14,
            'kg/year': 16,
            'ktonne/year': 39,
            'ktonne/oper-year': 50
        },
        'moleflow': {
            'kmol/sec': 1,
            'kmol/hr': 3,
            'mol/sec': 6,
            'kmol/day': 10,
            'mol/min': 14,
            'kmol/week': 29,
            'kmol/month': 30,
            'kmol/year': 31,
            'kmol/oper-year': 32
        },
        'volflow': {
            'cum/sec': 1,
            'l/min': 3,
            'cum/hr': 7,
            'cum/day': 11,
            'cum/year': 12,
            'cum/oper-year': 40
        },
        'duty': {
            'Watt': 1,
            'cal/sec': 3,
            'J/sec': 4,
            'GJ/hr': 5,
            'kcal/hr': 6,
            'kJ/sec': 13,
            'kW': 14,
            'MW': 15,
            'GW': 16,
            'MJ/hr':17,
            'Gcal/hr': 18,
            'Gcal/day': 20,
            'Mcal/hr': 21,
            'kJ/hr': 22
        },
        'power': {
            'Watt': 1,
            'hp': 2,
            'kW': 3,
            'MW': 7,
            'GW': 8,
            'MJ/hr': 9
        },
        'pressure': {
            'N/sqm': 1,
            'atm': 3,
            'bar': 5,
            'kPa': 10,
            'barg': 16,
            'Pa': 19,
            'MPa': 20,
            'Pag': 21,
            'kPag': 22,
            'MPag': 23
        },
        'temperature': {
            'K': 1,
            'C': 4
        },
        'electric_power': {
            'Watt': 1,
            'kW': 2,
            'MW':4
        } 
    }


    def __init__(self, process):
        
        self._values = {}
        self.process = weakref.ref(process)
        
        unit_set = self.process().asp.get_simulation_unit_set()
        for key, prop in self.unit_init.items():
            unit = self.process().asp.get_simulation_units(unit_set,prop)
            self._values[key] =  {unit:self.unit_dict[key][unit]}



    def __getattr__(self, prop):
        if prop in self.unit_dict:
            return self._values[prop] 
        else:
            raise AttributeError('Nonexistant Attribute', prop)


    def __setattr__(self, prop, value):
        if prop in self.unit_dict:
            if value in self.unit_dict[prop]:
                self._values[prop] = {value:self.unit_dict[prop][value]}
                self.process().reset2()
            else:
                raise AttributeError('Units not recognized', value)
        else:
            object.__setattr__(self, prop, value)

        
    def get_unit_numb(self, prop):

        if prop in self._values:
            for unit in self._values[prop]:
                return self._values[prop][unit]
        else:
            raise AttributeError('Property not recognized for unit assigment', prop)






    