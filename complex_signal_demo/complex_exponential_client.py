"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Programmer: David G Messerschmitt
2 March 2018
"""
from numpy import round

import complex_signal_client as csc

class ComplexExponentialClient(csc.ComplexSignalClient):
    # Client which retreives a complex exonential, making use of the
    # ComplexSignalClient (which retreives a generic complex signal)
    
    def __init__(self):
        super().__init__()

    # This method provides the configuration of the server
    # phaseBegin and phaseIncrement are fractions of 2*pi radians
    # Note that phaseIncrement = analog frequency * analog sampling interval

    def parameters(self):
        return {'phaseBegin':0,'phaseIncrement':0.1,'numSamples':105}

    # The following methods invokes super class to instantiate the run the client
    #   assumed to implemment get()
    def run(self):
        # run the client to return complex exponential with parameters()
        [self.reals,self.imags] = self.get()

    def report(self, resolution=3):
        # print result to standard output with specified resolution
        print('\nReal part of complex exponential ({0} samples):\n'.format(len(self.reals)))
        print(round(self.reals,resolution))
        print('\nImag part of complex exponential ({0} samples):\n'.format(len(self.imags)))
        print(round(self.imags,resolution))
                  

if __name__ == '__main__':
 c = ComplexExponentialClient()
 c.run()
 c.report()
