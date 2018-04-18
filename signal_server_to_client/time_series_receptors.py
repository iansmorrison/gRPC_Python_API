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

'''
For the convenience of the different receptors, we implement some
base classes that capture common functionality.
New receptor classes are added below.
'''

class SingleTimeSeriesComplex():
    '''
    Time-series receptor for any generator that streams a time-series with complex
    values. The time-values are not streamed. This base class generally has no
    knowledge of how the time-series was generated, only its structure.
    '''

    # class variables (same values for all instances)
    __handle__ = '' # specified by an inherited class
    __transport__ = 'complex_valued_streaming'
    
    def __init__(self):

        self.whole = np.array([])
        
    def receive(self,vals):
        # lists of values coming from buffer
        #   are pushed here to be processed and interpreted
        # vals = numpy.ndarray with dtype = complex

        if vals.size == 0: # entire time series received
            self.wrapup()           
        else:
            self.whole = np.append(self.whole,vals)

    def print(self,vals):
        # print out the real- and imag-parts of a time series
        # vals = numpy.ndarray with dtype = complex

            print(
                '\nTotal received time-series of length = ',
                  self.whole.size, ':'
                )
            print('\nReal-part\n', np.around(self.whole.real, 3))
            print('\nImag-part\n', np.around(self.whole.imag, 3))

    def plot(self,vals):
        # make a plot of the real- and imag-parts of a time-series
        # vals = numpy.ndarray with dtype = complex

            plt.plot(self.whole.real)
            plt.plot(self.whole.imag)
##            plt.axis([0, self.whole.size * T, -1, +1])
            plt.title('Complex exponential')
            plt.show()

'''
For each time-series generator, add a time-receptor class here.
It is often convenient to inherit one of the preceding base classes,
which receives frames of the time-series. This inherited class encapsulates
knowledge of how the time-series was generated, including its parameterization.
It is good practice to give this the same class name as the corresponding
generator class (there is no namespace clash since client and server run
in different processes).

Each receptor is assumed to have the following attributes:

    __handle__ = a 'popular' name for the receptor which is shared
        with the time-series generator with which it is coordinated

    parmeters(parameter_dict) = a method which accepts a parameter dictionary
        containing (possibly) default values, replaces those values with its
        own choices, and returns that dictonary

    wrapup() = a method which is called after the entire time-series
        has been accumulated
'''

class CExpC(SingleTimeSeriesComplex):

    # class variables (same values for all instances)
    __handle__ = 'complex_exponential_with_complex_transport'

    def __init__(self):

        super().__init__()

    def parameters(self,t):
        # configure parameter values for this service choice
        # t = default set of parameters as starting point

        t['frame'] = 20
        t['num_samples'] = 55
        t['phase_increment'] = 0.01

        return t

    def wrapup(self):
        
        self.print(self.whole)
        self.plot(self.whole)
