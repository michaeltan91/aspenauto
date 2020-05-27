from .objectcollection import ObjectCollection

class Streams(object):

    def __init__(self):

        return



class Material(Streams):

    def __init__(self, stream):
        
        self.pressure = []
        self.temperature = []   
        self.volflow = []

        self.massfrac = ObjectCollection()
        self.massflow = ObjectCollection()
        self.moleflow = ObjectCollection()

        if 'F-' in stream.Name:
            self.type = 'Feed'
        elif 'P-' in stream.Name:
            self.type = 'Product'
        elif 'W-' in stream.Name:
            self.type = 'Waste'
        else:
            self.type = 'Standard'


    def Collect(self, stream):
        
        self.temperature = stream.Output.TEMP_OUT.MIXED.Value
        self.pressure = stream.Output.PRES_OUT.MIXED.Value
        self.volflow = stream.Output.VOLFLMX.MIXED.Value

        for obj in stream.Output.MASSFRAC.MIXED.Elements:
            self.massfrac[obj.Name] = obj.Value

        for obj in stream.Output.MASSFLOW.MIXED.Elements:
            self.massflow[obj.Name] = obj.Value
        self.massflow['total'] = stream.Output.MASSFLMX.MIXED.Value

        for obj in stream.Output.MOLEFLOW.MIXED.Elements:
            self.moleflow[obj.Name] = obj.Value
        self.moleflow['total'] = stream.Output.MOLEFLMX.MIXED.Value



class Heat(Streams):

    def __init__(self, stream):

    
        self.Q = []
        self.type = 'Thermal'

    def Collect(self, stream):

        self.Q = stream.Output.QCALC.Value

    
        