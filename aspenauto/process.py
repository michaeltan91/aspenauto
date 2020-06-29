import os
import win32com.client as win32

from .objectcollection import ObjectCollection
from .blocks import Block
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
    MixSplit,
    Separator,
    Exchanger,
    Column,
    Reactor,
    Pressure,
    Solids,
    SolidsSeparator
)
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
        self.utilities = ObjectCollection()
        self.coolwater = ObjectCollection()
        self.llpsteam = ObjectCollection()
        self.llpsgen = ObjectCollection()
        self.lpsteam = ObjectCollection()
        self.lpsgen = ObjectCollection()
        self.mpsteam = ObjectCollection()
        self.mpsgen = ObjectCollection()
        self.hpsteam = ObjectCollection()
        self.hpsgen = ObjectCollection()
        self.electricity = ObjectCollection()
        self.refrigerant1 = ObjectCollection()
        self.refrigerant2 = ObjectCollection()
        self.refrigerant3 = ObjectCollection()
        self.refrigerant4 = ObjectCollection()
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
            if util.Name == 'CW':
                self.utilities[util.Name] = self.coolwater
            elif util.Name == 'ELECTRIC':
                self.utilities[util.Name] = self.electricity
            elif util.Name == 'LLPS':
                self.utilities[util.Name] = self.llpsteam
            elif util.Name == 'LLPS-GEN':
                self.utilities[util.Name] = self.llpsgen
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
            elif util.Name == 'RF1':
                self.utilities[util.Name] = self.refrigerant1
            elif util.Name == 'RF2':
                self.utilities[util.Name] = self.refrigerant2
            elif util.Name == 'RF3':
                self.utilities[util.Name] = self.refrigerant3
            elif util.Name == 'RF4':
                self.utilities[util.Name] = self.refrigerant4
    
        temp = []
        prefer = ['LLPS','LLPS-GEN', 'LPS', 'LPS-GEN', 'MPS', 'MPS-GEN', 'HPS', 'HPS-GEN', 'RF', 'ELECTRIC' , 'NATGAS', 'CW']
        for i in prefer:
            if i in self.utilities:
                temp.append(i)
        temp2 = ObjectCollection()
        for j in temp:
            temp2[j] = self.utilities[j]
        self.utilities = temp2
        



