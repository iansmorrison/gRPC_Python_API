"""
The Python implementation of time-series generators
All specifications for time-series generation are contained in this file,
    so a new time-series type can easily be added by editing this file
    and only this file.
    
Progammer David G Messerschmitt
16 April 2018
"""

import numpy as np
from pprint import pprint

'''
To add a new signal generator, simply add a new class implementing that
to this file. The name of this class matters not, except that it must be unique.

Each generator is expected to have a docstring, which is the descrption of
the generator conveyed to the client. It should give them sufficient information
to make an informed choice of that generator.

Each generator class is expected to have two configuration attributes:

    __handle__ is a 'popular' name for the generator which is
        friendly and descriptive to the user; this is the name displayed to the
        user and which the user specifies to invoke this generator
        
    __transport__ specifies whether this generator uses
        'real_valued_streaming' (each value has dtype = float)
        'complex_valued_streaming' (each value has dtype = complex)

One or a number of time-series can be streamed. Each such time-series can be
multi-dimensional numpy array containing scalar, vector, or matrix values.
For example, video would be a time-series of matrix values, each representing
one frame of the video. The array may or may not include a dimension containing
the times values, and it may or may not include a dimension containing the real- and
imag-parts of a complex value. The number of dimensions and the meanng of those
dimensions is a matter of convention established between coordinated generator
and client implementations and documented by the parameter dictionary (below).

Generally 'real_valued_streaming' is preferred because it is more general.
For example, it would be inefficient to represent time-values by dtype = complex values.
It is straightfoward to represent complex values by a dimension containing the
real- and imag-parts of that value.

Each generator class must have two methods:

    parameters() is called exactly once and returns a dictionary
        containing all the parameters of the generator        
        and a description of their meaning and their default values.
        This dictiionary is the sole documentation presented to the user,
        and is expected to have sufficient information and detail to allow
        the user to properly configure the generator.
        
    initialize(parameter_dict) is called once for each time-series generation cycle and
        allows the generator to initialize its internal state. Its sole argument
        is a dictionary of parameter values which has been specified by the user.
        
    generate() is called repeatedly, and returns a numpy.ndarray object
        representing one 'frame' of time-values. Generally this will not be the
        entire time-series, but rather just one frame of the time series.
        This ndarray object must have exactly one dimension so that it can
        be streamed serially over the network. If more than one such time-series
        is generated, the generator is responsible for their time-division
        multiplexing, generally by generating one frame of each such time-series
        in round-robin fashion.

The reason for putting responsibility for serialization and time-division
multiplexing on the generator is so that a compatible client can properly
interpret the stream of real- or complex-values it is streamed. Building all the
possible case into the server would be too limiting of the possibilities.
Fortunately this serialization and multiplexing is very straightforward with
available NumPy functions, as illustrated by the examples below.
'''

class CExpPlusTimeR():
    '''
    Time-series generator for a complex-exponential that streams real-values.
    The triplet [time,real,complex] contains both the time and the real-
    and imag-parts of the complex-exponential.
    '''

    __handle__ = 'complex_exponential_with_times_and_real_transport'

    # __transport__ specifies the gRPC service invoked by this generator
    __transport__ = 'real_valued_streaming'

    def __init__(self): pass


class CExpC():
    '''
    Time-series generator for a complex-exponential that streams complex
    values. The time-values are not streamed, and must be inferred by the client.
    '''
    
    # class variables (same values for all instances)
    __handle__ = 'complex_exponential_with_complex_transport'
    __transport__ = 'complex_valued_streaming'

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

    def initialize(self,parameter_dict):
        print('\nInitialization of time-series generator')
        print('\nTime-series generator will use the following parameters:')
        pprint(parameter_dict)
                  
        # store final set of parameters as variables for efficiency
        # for example, parameter 'frame' is stored in a variable self.frame
        for field in parameter_dict.keys():
            setattr(self,field,parameter_dict[field])

        self._count = 0  # number of time-values generated so far
        
    def generate(self):
        # generate one frame of time-values and return
        #   a one-dimensional numpy array continaing those values
        # these values have dtype = complex because we specified
        #   attribute __transport__ = 'complex_valued_streaming'

        # determine number of samples to generate this call
        total_remaining = self.num_samples - self._count
        start = self._count
        duration = min(total_remaining,self.frame)

        if duration > 0:

            t = np.arange(start,start+duration,1)  # ndarray of time indexes
            arg = 1j * 2 * np.pi * self.phase_increment * t # ndarray of phases
            vals = np.exp(arg)
            self._count += duration
            
            # vals is one-dimensional so no serialization required
            return vals

        else: return np.array([])

