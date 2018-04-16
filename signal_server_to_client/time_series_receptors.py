"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
  
Programmer: David G Messerschmitt
18 March 2018
"""
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt


class ComplexExponentialClient():
    # Client which retreives a complex exonential from the server
    # a uniform sampling rate is assumed, so the sampling times
    #   can be inferred without obtaining them from the server
    
    def __init__(self):

        self.whole = np.array([])
        
        super().__init__()

    def parameters(self,t):
        # configure parameter values for this service choice
        # t = default set of parameters as starting point

        t['frame'] = 20
        t['num_samples'] = 55
        t['phase_increment'] = 0.01

        return t
        
    def receive(self,vals):
        # lists of values coming from gRPC
        #   are pushed here to be processed and interpreted
        # vals = numpy array of length self.frame

        if vals.size == 0: # entire time series received
            
            print(
                '\nTotal received time-series of length = ',
                  self.whole.size, ':'
                )
            print('\nReal-part\n', np.around(self.whole.real, 3))
            print('\nImag-part\n', np.around(self.whole.imag, 3))

            # make a plot for the benefit of posterity
            plt.plot(self.whole.real)
            plt.plot(self.whole.imag)
##            plt.axis([0, self.whole.size * T, -1, +1])
            plt.title('Complex exponential')
            plt.show()
            
        else:
            self.whole = np.append(self.whole,vals)

