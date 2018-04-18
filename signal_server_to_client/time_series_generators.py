"""
The Python implementation of time-series generators
All specifications for new signal content are contained in this file,
    so a new time-series type can be added here
Progammer David G Messerschmitt
16 April 2018
"""

# make use of NumPy to simplify array processing
import numpy as np

# to add a new signal generator, simple add a new class
#   implementing that signal generato


class ComplexExponentialGenerator1():
    '''
    Time-series generator for a complex-exponential that employs
    real-valued streaming over the RPC layer, and conveys time-values
    as well as real- and imag-values.
    '''
    # the preceding doc string is the documentation for this generator
    #   that is displayed to the user
    
    # two required class variables are __handle__ and __transport__
    
    # __handle__ = a 'popular' name for the generator which is
    #   friendly and descriptive t the user
    __handle__ = 'cexp1'

    # __transport__ specifies the gRPC service invoked by this generator
    __transport__ = 'real-valued_streaming'

    def __init__(self): pass


class ComplexExponentialGenerator():
    '''
    Time-series generator for a complex-exponential that uses the
    complex-valued streaming over the RPC layer.
    '''
    # the preceding doc string is the documentation for this generator
    #   that is displayed to the user
    
    # two required class variables are __handle__ and __transport__
    
    # __handle__ = a 'popular' name for the generator which is
    #   friendly and descriptive t the user
    __handle__ = 'cexp'

    # __transport__ specifies the gRPC service invoked by this generator
    __transport__ = 'real-valued_streaming'

    def __init__(self): pass

    def parameters(self):
        # specify configuration parameters, includng values (cannot be changed)
        #   and defaults (subject to change)
        # a default = None indicates that the client must specify a value

        t = {'service_type':'cexp'}
        t['description'] = 'generator returns samples of a complex exponential \
exp(j * 2*pi * phase(t) * t) where t = time'
        t['num_samples'] = {
                          'description':'total duration of time-series in samples',
                          'default':None,
                          'minimum':1
                          }
        t['frame'] = {
                        'description':'number of time-samples in each generated \
time-series frame',
                        'default':10,
                        'minimum':1
                        }
        t['phase_initial'] = {
                          'description':'phase of first time-sample \
as fraction of 2*pi, in the range +-0.5',
                          'default':0.,
                          'minimum':-0.5,
                          'maximum':+0.5
                          }
        t['phase_increment'] = {
                        'description':'phase advance per time-sample as fraction \
of 2*pi;  by sampling theorem, must be in the range +-0.5',
                        'default':None,
                        'minimum':-0.5,
                        'maximum':+0.5
                        }
        return t

    def initialize(self,t):
        # initialize the time-series generator
        # t = dictionary of final parameter values
                  
        # store final set of parameters as variables for efficiency
        # for example, parameter 'frame' becomes self.frame
        for field in t.keys():
            setattr(self,field,t[field])

        self._count = 0  # number of time-values generated in total
        
    def generate(self):
        # generates one frame of time-samples and returns as a list

        # determine number of samples to generate this call
        total_remaining = self.num_samples - self._count
        start = self._count
        duration = min(total_remaining,self.frame)

        if duration > 0:

            t = np.arange(start,start+duration,1)  # array of time indexes
            arg = 1j * 2 * np.pi * self.phase_increment * t
            vals = np.exp(arg)
            self._count += duration
            
            return list(vals)

        else: return []

