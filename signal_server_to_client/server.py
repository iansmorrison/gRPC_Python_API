"""
The Python implementation of a server that returns a
  complex exponential complex-valued signal
Progammer David G Messerschmitt
4 April 2018
"""
import cmath
import numpy as np

import signal_server as css
import parameters as param
import buffer as buf

class TimeSeriesServer:
    '''
    Implements a server which provides a one-dimensional
    stream of complex-valued samples
    The packet size is determined by network efficiency
        considerations
    Generates the actual signal sample values
        including the number of samples per call and the
        total number of samples
    Returns a list of samples, which is empty if the server
        is exhausted
    '''

    def __init__(self,p,t):
      # p = instance of Parameters class storing parameter metadata
      # t = parameter dictionary for this signal semantics
      self.param = p

      # add metadata relevant at this layer to that provided by
      #   and inherited class
      t['service_type'] = {
                      'description':'structure of the signal',
                      'default':'time_series'
                      }
      t['num_samples'] = {
                      'description':'total duration of signal in samples',
                      'default':None,
                      'minimum':1
                      }
      t['frame'] = {
                    'description':'number of samples in each generated \
signal frame',
                    'default':10,
                    'minimum':1
                    }
          
      # initialize Parameter with the parameter metadata
      self.param.set(t)
     
      # initialize state of signal generation
      self.initialize()

    def initialize(self):
      # signal generator may be run more than once, so
      #   define an initialization separate from object instantiation

      self._count = 0
      self.param_dict_to_var()
      
    def param_dict_to_var(self):
      
      # store final set of parameters as variables for efficiency
      # for example, parameter 'num_samples' becomes self.numSamples
      p = self.param.final()
      for field in p.keys():
        setattr(self,field,p[field])
      
    def get(self):
    
      # determine number of samples to generate
      total_remaining = self.num_samples - self._count
      generate_this_call = min(total_remaining,self.frame)

      if generate_this_call > 0:
        self._count += generate_this_call
        # method generate() must be provided by inherited class
        return self.generate(self._count,generate_this_call)
      else:
        return []
      

class ComplexExponentialServer(TimeSeriesServer):

  def __init__(self,p):
    # p = instance of Parameters storing parameter values

    # define the parameters, their bounds and their defaults
    # note: all numerical parameters must have a 'default' field
    #     (set to default=None if client is required to supply this parameter)

    t = {'semantics':'cexp'}
    t['description'] = 'service returns samples of a complex exponential \
cos(2*pi*phase) + i * sin(2*pi*phase)'
    t['phase_initial'] = {
                      'description':'phase of first sample as fraction of 2*pi; \
must be between -0.5 and +0.5',
                      'default':0.,
                      'minimum':-0.5,
                      'maximum':+0.5
                      }
    t['phase_increment'] = {
                    'description':'phase advance per sample as fraction of 2*pi; \
by sampling theorem, must be between -0.5 and +0.5',
                    'default':None,
                    'minimum':-0.5,
                    'maximum':+0.5
                    }

    super().__init__(p,t)

  def generate(self,start,duration):
    
##    # generate a list of samples indexed by start<=k<(start+duration-1)
##    vals = [None] * duration
##    for i in range(duration):
##        phase = self.phase_initial + (start+i)*self.phase_increment
##        vals[i] = cmath.exp(2.*cmath.pi*phase*1j)
##    return vals

    # generate a numpy array of samples indexed by start<=k<(start+duration-1)
    print(start,duration)
    t = np.arange(start,start+duration,1)
    print(t)
    arg = 1j * 2 * np.pi * self.phase_increment * t
    print(arg)
    vals = np.exp(arg)
    print(vals)
    return list(vals)
    

if __name__ == '__main__':

    p = param.Parameters() # parameter dictonary
    g = ComplexExponentialServer(p) # signal generator
    b = buf.TimeSeriesBuffer(g)   # streaming buffer
    s = css.StreamingServer(p,b,g)  # gRPC server
    s.run()
