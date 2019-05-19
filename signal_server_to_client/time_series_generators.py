"""
The Python implementation of time-series generators
All specifications for time-series generation are contained in this file,
    so a new time-series type can easily be added by editing this file
    and only this file.
    
Progammer David G Messerschmitt
16 April 2018
"""

import os
import numpy as np
from scipy import signal
from pprint import pprint

import time_series_server as tss

'''
To add a new signal generator, simply add a new class implementing that
to this file. The name of this class matters not, except that it must be unique.

Each generator is expected to have a docstring, which is the description of
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
imag-parts of a complex value. The number of dimensions and the meaning of those
dimensions is a matter of convention established between coordinated generator
and client implementations and documented by the parameter dictionary (below).

Generally 'real_valued_streaming' is preferred because it is more general.
For example, it would be inefficient to represent time-values by dtype = complex values.
It is straightforward to represent complex values by a dimension containing the
real- and imag-parts of that value.

Each generator class must have two methods:

    parameters() is called exactly once and returns a dictionary
        containing all the parameters of the generator        
        and a description of their meaning and their default values.
        This dictionary is the sole documentation presented to the user,
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

    def parameters(self):
        # specify configuration parameters, including values (cannot be changed)
        #   and defaults (subject to change)
        # a default = None indicates that the client must specify a value
        # a value = something is a value that is chosen by the server
        #   and cannot be changed

        t = {}

        t['frame'] = {
            'description':'number of time-samples in each generated \
time-series frame',
            'default':10,
            'minimum':1
                        }
        
        t['time_duration'] = {
            'description':'total duration of time-series in samples',
            'default':None,
            'minimum':1
                          }
        
        t['phase_initial'] = {
            'description':'phase of first time-sample as fraction of 2*pi, \
            in the range +-0.5',
            'default':0.,
            'minimum':-0.5,
            'maximum':+0.5
                          }

        t['sampling_interval'] = {
            'description':'time interval between samples in seconds',
            'default':None,
            'minimum':0.
                        }

        t['frequency'] = {
            'description':'frequency in Hz',
            'default':None,
            'minimum':0.
                        }
        
        return t

    def initialize(self):
        # initializes time-series generator for a new run
        # returns the transport parameters chosen
        #   (which pay depend on the values in the generator parameters)

        # note: this object has already been equipped with a set of
        #   attributes storing parameter values chosen by the client;
        #   for example parameter 'frame' has been stored as attribute self.frame

        self._num_samples = int( self.time_duration / self.sampling_interval )       
        self._count = 0  # number of time-values generated so far

        # transport parameters returned to client for its configuration
        r = {
            
            'data_type' : 'real',  # must be 'real' or 'complex'
            
            # we will time-division multiplex three time-series:
            # [times, reals, imags]
            'array_shapes': [[self.frame]] * 3
            }
        
        return r
        
    def generate(self):
        # generate one frame of time-values and return
        #   a one-dimensional numpy array containing those values
        # these values have dtype=complex because we specified
        #   'data_type' to be complex

        # determine number of samples to generate this call
        total_remaining = self._num_samples - self._count
        start = self._count
        duration = min(total_remaining,self.frame)

        if duration > 0:

            # array of time's
            t = np.arange(start,start+duration,1) * self.sampling_interval

            # array of phases
            arg = 2 * np.pi * self.frequency * t

            # evaluate complex exponential
            vals = np.exp(1j * arg)
            
            self._count += duration

            # time-division multiplex three real-valued time-series
            return [ t, vals.real, vals.imag ]

        else: return []
        

class CExpC():
    '''
    Time-series generator for a complex-exponential that streams complex
    values. The time-values are not streamed, and must be inferred by the client.
    The streaming is divided into frames, whose size the client can control.
    '''

    __handle__ = 'complex_exponential_with_complex_transport'

    def parameters(self):
        # specify configuration parameters, includng values (cannot be changed)
        #   and defaults (subject to change)
        # a default = None indicates that the client must specify a value
        # a value = something is a value that is chosen by the server
        #   and cannot be changed

        t = {}
        
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
            'description':'phase of first time-sample as fraction of 2*pi, \
            in the range +-0.5',
            'default':0.,
            'minimum':-0.5,
            'maximum':+0.5
                          }
        
        t['phase_increment'] = {
            'description':'phase advance per time-sample as fraction \
of 2*pi;  by sampling theorem, it must be in the range +-0.5',
            'default':None,
            'minimum':-0.5,
            'maximum':+0.5
                        }
        return t

    def initialize(self):
        # initializes time-series generator for a new run
        # returns the transport parameters chosen
        #   (which pay depend on the values in the generator parameters)

        # note: this object has already been equipped with a set of
        #   attributes storing parameter values chosen by the client;
        #   for example parameter 'frame' has been stored as attribute self.frame
        
        self._count = 0  # number of time-values generated so far

        # transport parameters returned to client for its configuration
        r = {
            
            'data_type' : 'complex',  # must be 'real' or 'complex'
            
            # exactly one time-series [] is generated
            # 1-D ndarray of complex values with shape [self.frame]
            'array_shapes': [ [self.frame] ]
            }
        
        return r
        
    def generate(self):
        # generate one frame of time-values and return
        #   a one-dimensional numpy array containaing those values
        # these values have dtype=complex because we specified
        #   'data_type' to be 

        # determine number of samples to generate this call
        total_remaining = self.num_samples - self._count
        start = self._count
        duration = min(total_remaining,self.frame)

        if duration > 0:

            t = np.arange(start,start+duration,1)  # ndarray of time indexes
            arg = 1j * 2 * np.pi * self.phase_increment * t # ndarray of phases
            vals = np.exp(arg)
            self._count += duration
            
            # vals = numpy array to be returned
            # vals.shape must be consistent with 'array_shapes'

            # return a list with length = 1
            #   (since there is only one time-multiplexed signal)
            return [vals]

##        else: return np.array([])
        else: return []


class SigMFfileBrowser():
    '''
    This signal generator reads a range of complex values of a SigMF
    file containing a recorded signal. It streams the real and imaginary
    time series as two separate signals to the client.
    '''

    __handle__ = 'browse samples stored in a SigMF file'

    def parameters(self):
        # specify configuration parameters, including values (cannot be changed)
        #   and defaults (subject to change)
        # a default = None indicates that the client must specify a value
        # a value = something is a value that is chosen by the server
        #   and cannot be changed

        t = {}

        t['directory'] = {
            'description':'directory containing repository of SigMF files',
              'default':'data'
                      }

        t['file_name'] = {
            'description':'name of SigMF signal data file',
              'default':'rosetta-2010-06-04.sigmf-data'
                      }
          
        t['starting_sample'] = {
            'description':'index of starting sample',
            'default':0,
            'minimum':0
                        }
        
        t['total_sample_count'] = {
            'description':'total number of samples',
            'default':100,
            'minimum':1
                          }
        
        return t

    def initialize(self):
        # initializes time-series generator for a new run
        # returns the transport parameters chosen
        #   (which pay depend on the values in the generator parameters)

        # note: this object has already been equipped with a set of
        #   attributes storing parameter values chosen by the client;
        #   for example parameter 'frame' has been stored as attribute self.frame

        # we assume data files are stored in a subdirectory
        #   of the python code being executed
        # change current directory code directory
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        # file relative path to data file
        self.file_path = os.path.join(self.directory,self.file_name)
        
        # Map the file for easy access to the data  
        self.file_map = np.memmap(self.file_path,dtype=np.byte)

        # Useful for checking file indexes against file length
        self.total_file_length = self.file_map.size

        # Track number of calls
        self.call_count = 0

        # transport parameters returned to client for its configuration
        r = {
            
            'data_type' : 'real',  # must be 'real' or 'complex'
            
            # we will time-division multiplex two time-series:
            # [reals, imags]
            'array_shapes': [[self.total_sample_count]] * 2
            }
        
        return r
        
    def generate(self):
        # generate one frame of time-values and return
        #   a one-dimensional numpy array containing those values
        # these values have dtype=real because we specified
        #   'data_type' to be float

        if self.call_count < 1:
            
            # Odd values (starting with index one) are the real part
            self.datavals_real = \
                self.file_map[self.starting_sample:self.starting_sample+2*self.total_sample_count:2]
            # Repeat starting with index two to get the complex part
            self.datavals_imag = \
                self.file_map[self.starting_sample+1:self.starting_sample+2*self.total_sample_count][::2]
            
            self.call_count += 1

            # time-division multiplex real and imag time-series
            return [ self.datavals_real, self.datavals_imag ]

        else: return []

class SigMFfilePeriodogram():
    '''
    This signal generator reads a range of complex values of a SigMF
    file containing a recorded signal. It calculates a Welsh periodogram
    on the resuting range.
    '''

    __handle__ = 'generate a Welch periodogram on a SigMF file'

    def parameters(self):
        # specify configuration parameters, including values (cannot be changed)
        #   and defaults (subject to change)
        # a default = None indicates that the client must specify a value
        # a value = something is a value that is chosen by the server
        #   and cannot be changed

        t = {}

        # No attempt to make the path platform-independent
        t['directory'] = {
            'description':'directory containing the repository of SigMF files',
            'default':'data'
                      }

        t['file_name'] = {
            'description':'name of specific SigMF signal data file',
            'default':'rosetta-2010-06-04.sigmf-data'
                      }
          
        t['starting_sample'] = {
            'description':'index of starting sample',
            'default':0,
            'minimum':0
                        }
        
        t['total_sample_count'] = {
            'description':'total number of samples',
            'default':10000,
            'minimum':1
                          }
        
        return t

    def initialize(self):
        # initializes time-series generator for a new run
        # returns the transport parameters chosen
        #   (which pay depend on the values in the generator parameters)

        # note: this object has already been equipped with a set of
        #   attributes storing parameter values chosen by the client;
        #   for example parameter 'frame' has been stored as attribute self.frame

        # we assume data files are stored in a subdirectory
        #   of the python code being executed
        # change current directory code directory
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        # file relative path to data file
        self.file_path = os.path.join(self.directory,self.file_name)
        
        # Map the file for easy access to the data  
        self.file_map = np.memmap(self.file_path,dtype=np.byte)
        
        # Useful for checking file indexes against file length
        self.total_file_length = self.file_map.size

        # Track the number of calls
        self.call_count = 0

        # transport parameters returned to client for its configuration
        r = {
            
            'data_type' : 'real',  # must be 'real' or 'complex'
            
            # we will time-division multiplex two time-series:
            # [frequencies, spectrum]
            # 256 is default analysis window for signal.welch
            'array_shapes': [[256],[256]]
            }

        print('Transport charcteristic: ', r)
        
        return r
        
    def generate(self):
        # generate one frame of time-values and return
        #   a one-dimensional numpy array containing those values
        # these values have dtype=real because we specified
        #   'data_type' to be float

        if self.call_count < 1:
    
            # Odd values (starting with index one) are the real part
            self.datavals_real = \
                self.file_map[self.starting_sample:self.starting_sample+2*self.total_sample_count:2]
            # Repeat starting with index two to get the complex part
            self.datavals_imag = \
                self.file_map[self.starting_sample+1:self.starting_sample+2*self.total_sample_count][::2]

            # Do the periodogram
            self.f, self.PS = \
               signal.welch(self.datavals_real + 1j*self.datavals_imag,scaling='spectrum')

            print('Periodogram array sizes', self.f.size, self.PS.size)
            
            self.call_count += 1

            # time-division multiplex frequency and spectrum
            return [ self.f, self.PS ]

        else: return []
