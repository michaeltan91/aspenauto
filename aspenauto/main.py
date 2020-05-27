import os
import win32com.client as win32

class Aspen(object):


    def __init__(self, Aspen_file):

        self.aspen = win32.Dispatch('Apwn.Document')
        self.aspen.InitFromArchive2(os.path.abspath(Aspen_file))
        
    def Run(self):


        return