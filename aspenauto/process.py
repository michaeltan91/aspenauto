import os
import win32com.client as win32

from .objectcollection import ObjectCollection
from .output import Output
from .flowsheet import Flowsheet
from .asp import ASP
import warnings

class Process(object):
    # Main class

    def __init__(self, aspen_file):
        
        # Load Aspen Model
        self.aspen = win32.Dispatch('Apwn.Document')
        self.aspen.InitFromArchive2(os.path.abspath(aspen_file))
        # Load print output class
        self.output = Output()
        self.ready = False

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
        self.naturalgas = ObjectCollection()
        self.coolwater = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant = ObjectCollection()
        self.steam = ObjectCollection()
        self.steamgen = ObjectCollection()
        self.utilities = ObjectCollection()
        
        # Assign classes to all Aspen Plus simulation objects

        self.asp = ASP(self)
        self.load_utilities()
        self.flowsheet = Flowsheet(self)


    def run(self):
        """Run the Aspen Engine"""
        self.aspen.Engine.Run2()
        # Check whether Aspen reported an error
        error_path = "\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR"
        error = self.aspen.Tree.FindNode(error_path).Value
        if error == 1:
            report = ''
            for sentence in self.aspen.Tree.FindNode(error_path).Elements:
                report = report + str(sentence.Value)+'\n'
            print(report)
            #raise RuntimeError('Error/Warning in Aspen Plus simulation')
        
        self.ready = True
            

    def print(self, work_book):
        """Prints the output in an excel file"""
        if self.ready == True:
            self.output.Print_Mass(self.material_streams, work_book)
            self.output.Print_Energy(self.utilities, work_book)
        else:
            warnings.warn('Requesting data from unsolved simulation')


    def reset(self):
        """Resets the aspen simulations and resets all class attribute values"""
        # Resets aspen simulation
        self.aspen.Reinit()
        # Resets all class attribute values
        for stream in self.streams:
            stream.reset()
        for utility in self.utilities:
            for block in utility:
                block.reset()
        self.ready = False
    

    def close(self):
        """Closes the Aspen Plus Engine"""
        self.aspen.Close()


    def load_utilities(self):
        utilities = self.asp.get_utility_list()
        # Load and fill utility dictionaries
        for util in utilities:
            util_name = util.Name
            util_type = self.asp.get_util_type(util_name)
            if util_type == 'WATER':
                self.coolwater[util_name] = ObjectCollection()
                self.utilities[util_name] = self.coolwater[util_name]
            elif util_type == 'ELECTRICITY':
                self.electricity[util_name] = ObjectCollection()
                self.utilities[util_name] = self.electricity[util_name]
            elif util_type == 'GAS':
                self.naturalgas[util_name] = ObjectCollection()
                self.utilities[util_name] = self.naturalgas[util_name]
            elif util_type == 'STEAM':
                steam_type = self.asp.get_steam_type(util_name)
                if steam_type == 'STEAM':
                    self.steam[util_name] = ObjectCollection()
                    self.utilities[util_name] = self.steam[util_name]
                elif steam_type == 'STEAM-GEN':
                    self.steamgen[util_name] = ObjectCollection()
                    self.utilities[util_name] = self.steamgen[util_name]
            elif util_type == 'REFRIGERATIO':
                self.refrigerant[util_name] = ObjectCollection()
                self.utilities[util_name] = self.refrigerant[util_name]
        



