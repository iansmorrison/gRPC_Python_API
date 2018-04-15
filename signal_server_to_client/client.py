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

import parameters as param
import signal_client as sc


class ComplexExponentialClient(sc.ComplexTimeSeriesClient):
    # Client which retreives a complex exonential from the server
    # a uniform sampling rate is assumed, so the sampling times
    #   can be inferred without obtaining them from the server
    
    def __init__(self,p):
        # p = instance of Parameters for storing parameter values

        # set parameters relevant at this semantics layer
        t = {}
        t['semantics'] = 'complex_exponential'
        t['frame'] = 20
        t['phase_increment'] = 0.01

        self.whole = np.array([])
        
        super().__init__(p,t)

    def receive(self,vals):
        # lists of values coming from gRPC
        #   are pushed here to be processed and interpreted
        # vals = numpy array of length self.frame

        if vals.size == 0: # entire time series received
            
            print('\nTotal received time-series of length = ',
                  self.whole.size,'\n', self.whole)
            print('\nReal-part\n', self.whole.real)
            print('\nImag-part\n', self.whole.imag)

            # make a plot for posterity
            plt.plot(self.whole.real)
            plt.plot(self.whole.imag)
##            plt.axis([0, self.whole.size * T, -1, +1])
            plt.title('Complex exponential')
            plt.show()
            
        else:
            self.whole = np.append(self.whole,vals)
            print('One frame of size = ', vals.size, '\n', np.around(vals,2))


if __name__ == '__main__':

    p = param.Parameters()
    s = ComplexExponentialClient(p)
    s.run()
