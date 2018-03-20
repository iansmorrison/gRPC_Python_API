"""
The Python implementation of a server that returns a
  complex exponential complex-valued signal
Progammer David G Messerschmitt
18 March 2018
"""
from math import pi,sin,cos

import signal_server as css

class ComplexExponentialServer(css.OneDimensionalSignalServer):
  
  def __init__(self):
    
    super().__init__()
  
    # add names for lists containing repeated fields
    self.real = []; self.imag = []

  def param_define(self):
    # defines the parameters for this signal, their bounds and their defaults
    # returns a dictonary containing this information
    # Note: all numerical parameters must have a 'default' field
    #     (set to None if client is required to supply this parameter)

    p = {'semantics':'cexp'}
    p['description'] = 'service returns samples of a complex exponential \
cos(2*pi*phase) + i * sin(2*pi*phase)'
    p['num_samples'] = {
                      'description':'total duration of signal',
                      'default':None,
                      'minimum':1
                      }
    p['phase_initial'] = {
                      'description':'phase of first sample as fraction of 2*pi; \
must be between -0.5 and +0.5',
                      'default':0.,
                      'minimum':-0.5,
                      'maximum':+0.5
                      }
    p['phase_increment'] = {
                    'description':'phase advance per sample as fraction of 2*pi; \
by sampling theorem, must be between -0.5 and +0.5',
                    'default':None,
                    'minimum':-0.5,
                    'maximum':+0.5
                    }

    return p
      
         
  def signal_gen(self,start,size):
    
    # required method of ComplexSignalServer
    # returns a repeated field of samples as a pair of lists
    # size = number of samples requested
    # this method will be called repeatedly for streaming, and
    #   so must maintain an internal state between calls

    # Allocate new memory for samples (unless already allocated)
    if len(self.real) != size:
      self.real = [None] * size; self.imag = [None] * size
    
    for i in range(size):
      phase = self.phase_initial+self.phase_increment*(start+i)
      self.real[i] = cos(2*pi*phase)
      self.imag[i] = sin(2*pi*phase)
            
    return [self.real,self.imag]


if __name__ == '__main__':

  s = ComplexExponentialServer()
  s.run()
