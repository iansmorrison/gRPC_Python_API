"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
  
Programmer: David G Messerschmitt
18 March 2018
"""
from pprint import pprint

import parameters as param
import signal_client as sc
import buffer as buff


class ComplexExponentialClient(sc.TimeSeriesClient):
    # Client which retreives a complex exonential, making use of the
    # ComplexSignalClient (which retreives a generic complex signal)
    
    def __init__(self,p):
        # p = instance of Parameters for storing parameter values

        # set parameters relevant at this semantics layer
        t = {}
        t['semantics'] = 'complex_exponential'
        t['frame'] = 20
        t['phase_increment'] = 0.1
        
        super().__init__(p,t)                

if __name__ == '__main__':

    p = param.Parameters()
    s = ComplexExponentialClient(p)
    b = buff.TimeSeriesBuffer(s)
    s.connect(b)
    s.discovery()
    s.configuration()
    s.run()
