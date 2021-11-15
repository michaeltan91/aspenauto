"""Contains the main structure and methods"""
import os
import warnings
import win32com.client as win32
from epynet import ObjectCollection

from .output import Output
from .flowsheet import Flowsheet
from .asp import ASP

from .utilities import (
    Electricity,
    Coolwater,
    Steam,
    Steam_Gen,
    Refrigerant,
    Gas
)

class Model(object):
    '''Main aspen auto class'''

    def __init__(self, aspen_file):

        # Load Aspen Model
        self.aspen = win32.Dispatch('Apwn.Document')
        self.aspen.InitFromArchive2(os.path.abspath(aspen_file))
        # Load print output class
        self.output = Output(self)
        self.ready = False

        # Prepate dictionaries for the blocks of the same type
        self.blocks = ObjectCollection()
        self.hierarchy = ObjectCollection()

        self.mixsplits = ObjectCollection()
        self.separators = ObjectCollection()
        self.exchangers = ObjectCollection()
        self.columns = ObjectCollection()
        self.reactors = ObjectCollection()
        self.pressurechangers = ObjectCollection()
        self.solids = ObjectCollection()
        self.solidseparators = ObjectCollection()

        ### Prepate dictionaries for the specific blocks in Apen Plus
        self.compr = ObjectCollection()
        self.mcompr = ObjectCollection()
        self.pump = ObjectCollection()

        self.mixer = ObjectCollection()
        self.fsplit = ObjectCollection()

        self.flash2 = ObjectCollection()
        self.flash3 = ObjectCollection()
        self.decanter = ObjectCollection()
        self.sep = ObjectCollection()

        self.heater = ObjectCollection()
        self.heatx = ObjectCollection()

        self.radfrac = ObjectCollection()

        self.rgibbs = ObjectCollection()
        self.rstoic = ObjectCollection()
        self.rplug = ObjectCollection()
        self.ryield = ObjectCollection()


        # Prepare stream dictionaries for the individual stream types and the combined collection
        self.streams = ObjectCollection()
        self.material_streams = ObjectCollection()
        self.heat_streams = ObjectCollection()
        self.work_streams = ObjectCollection()
        # Utility dictionaries
        self.natural_gas = ObjectCollection()
        self.coolwater = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant = ObjectCollection()
        self.steam = ObjectCollection()
        self.steam_gen = ObjectCollection()
        self.utilities = ObjectCollection()

        # Assign classes to all Aspen Plus simulation objects

        self.asp = ASP(self)
        self.load_utilities()
        #self.units = Units(self)
        self.flowsheet = Flowsheet(self)


    def run(self, report_error = True):
        """Run the Aspen Engine"""
        # Reset the Aspen simulation and delete the previously retrieved values from the simulation
        self.reset()
        # Run the Aspen simulation
        self.aspen.Engine.Run2()
        version_path = "\\Settings\\startupdir"
        print(self.aspen.Tree.FindNode(version_path).Value)
        # Check whether Aspen reported an error
        error_path = "\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR"
        error = self.aspen.Tree.FindNode(error_path).Value
        if report_error is True and error == 1:
            report = ''
            for sentence in self.aspen.Tree.FindNode(error_path).Elements:
                report = report + str(sentence.Value)+'\n'
            print(report)
            #raise RuntimeError('Error/Warning in Aspen Plus simulation')

        self.ready = True


    def print(self, work_book):
        """Prints the output in an excel file"""
        if self.ready is True:
            self.output.Print_Mass(self.material_streams, work_book)
            self.output.Print_Energy(self.utilities, work_book)
        else:
            warnings.warn('Requesting data from unsolved simulation')


    def reset(self):
        """Reset the aspen simulations and reset all class attribute values"""
        # Reset aspen simulation
        self.aspen.Reinit()
        # Reset all retrieved class attribute values
        for stream in self.streams:
            stream.reset()
        for utility in self.utilities:
            for block in utility.blocks:
                block.reset()
        self.ready = False


    def reset2(self):
        """Reset the values retrieved from the Aspen simulation"""
        for stream in self.streams:
            stream.reset()
        for utility in self.utilities:
            for block in utility.blocks:
                block.reset()


    def close(self):
        """Closes the Aspen Plus Engine"""
        self.aspen.Close()


    def load_utilities(self):
        """Loads the utilities from the Aspen Model"""
        utilities = self.asp.get_utility_list()
        # Load and fill utility dictionaries
        for util in utilities:
            util_name = util.Name
            util_type = self.asp.get_util_type(util_name)
            if util_type == 'WATER':
                self.coolwater[util_name] = Coolwater(util_name, self)
                self.utilities[util_name] = self.coolwater[util_name]
            elif util_type == 'ELECTRICITY':
                self.electricity[util_name] = Electricity(util_name, self)
                self.utilities[util_name] = self.electricity[util_name]
            elif util_type == 'GAS':
                self.natural_gas[util_name] = Gas(util_name, self)
                self.utilities[util_name] = self.natural_gas[util_name]
            elif util_type == 'STEAM':
                steam_type = self.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    self.steam[util_name] = Steam(util_name, self)
                    self.utilities[util_name] = self.steam[util_name]
                elif steam_type == 'STEAM-GEN':
                    self.steam_gen[util_name] = Steam_Gen(util_name, self)
                    self.utilities[util_name] = self.steam_gen[util_name]
            elif util_type == 'REFRIGERATIO':
                self.refrigerant[util_name] = Refrigerant(util_name, self)
                self.utilities[util_name] = self.refrigerant[util_name]
