"""
Time-series receptors the connect to a client stub.
For each time-series generator, there needs to be a coordinated
time-series receptor.
  
Programmer: David G Messerschmitt
18 April 2018
"""

from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

import time_series_client as tsc

'''
For each time-series generator, add a time-receptor class here.
It is often convenient to inherit one of the preceding base classes,
which receives frames of the time-series. This inherited class encapsulates
knowledge of how the time-series was generated, including its parameterization.
It is convenient to give this the same class name as the corresponding
generator class (there is no namespace clash since client and server run
in different processes).

Each receptor is assumed to have the following attributes:

    __handle__ = a 'popular' name for the receptor which is shared
        with the time-series generator with which it is coordinated
        (it is used to pair a generator and receptor)

    parameters() = a method that returns a dictonary containing
        parameter values it has set

    receive() = a method used to push each time-division list of
        time-series to the receptor

    wrapup() = a method that is called after the entire time-series
        has been accumulated; typically it does something with the final
        time-series like printing or plotting
'''

class CExpPlusTimeR(tsc.MultiplexedTimeSeries):

    __handle__ = 'complex_exponential_with_times_and_real_transport'

    def parameters(self):
        # configure parameter values for this service choice
        # t = default set of parameters as starting point
        # parameters not explicitly set here will assume default values

        t = {}
        
        t['frame'] = 15 # samples
        
        t['time_duration'] = 100. # seconds
        
        t['frequency'] = 0.03 # Hz

        t['sampling_interval'] = 1. # seconds

        return t

    def receive(self,vals):
        # lists of values pulled from buffer
        #   are pushed here to be processed and interpreted
        # vals = list of numpy arrays with vals.dtype = complex,
        #   one for each time-multiplexed time-series

        # in this receptor, we are interested only in the whole
        #   time-series, so we call on accumlate()
        self.accumulate(vals)
        
    def wrapup(self):

        self.print(
            'Sampling times:', 3,
            self.whole[0]
            )
        self.print(
            'Real parts:', 3,
            self.whole[1]
            )
        self.print(
            'Imag parts:', 3,
            self.whole[2]
            )
        
        self.plot(
            'Complex exponential',
            [0, self.time_duration, -1, +1], # range of axes
            [self.whole[1],self.whole[2]]
            )
        
    
class CExpC(tsc.MultiplexedTimeSeries):

    __handle__ = 'complex_exponential_with_complex_transport'

    def parameters(self):
        # configure parameter values for this service choice
        # t = default set of parameters as starting point
        # parameters not explicitly set here will assume default values

        t = {}
        
        t['frame'] = 15
        
        t['num_samples'] = 100
        
        t['phase_increment'] = 0.01

        return t

    def receive(self,vals):
        # lists of values pulled from buffer
        #   are pushed here to be processed and interpreted
        # vals = list of numpy arrays with vals.dtype = complex,
        #   one for each time-multiplexed time-series    

        # in this receptor, we are interested only in the whole
        #   time-series, so we ask them to be accumlate()'ed
        self.accumulate(vals)
        
    def wrapup(self):
        
        self.print(
            'Real part:', 3,
            self.whole[0].real
            )
        self.print(
            'Imag part:', 3,
            self.whole[0].imag
            )
        
        self.plot(
            'Complex exponential',
            [0, self.num_samples, -1, +1], # range of axes
            [self.whole[0].real,self.whole[0].imag]
            )
