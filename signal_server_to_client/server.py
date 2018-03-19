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
    
    # generate parameter dictionaries for this signal semantics
    self.parameters = self.param_define()
    self.defaults = self.param_default(self.parameters)

    # if an error occurs, setting this variable to False will
    #   stop further actions
    self.abort = False

    # internal state preserved from one call to the next
    self.samples_sent = 0  # number of signal samples already sent
    self.last_size = -1  # size of last repeated field sent

  #   !!! CONFIGURATION  !!!

  def param_define(self):
    # defines the parameters for this signal, their bounds and their defaults
    # returns a dictonary containing this information
    # Note: all numerical parameters must have a 'default' field
    #     (set to None if client is required to supply this parameter)

    param = {'semantics':'cexp'}
    param['description'] = 'service returns samples of a complex exponential \
cos(2*pi*phase) + i * sin(2*pi*phase)'
    param['numSamples'] = {
                      'description':'total duration of signal',
                      'default':None,
                      'minimum':1
                      }
    param['phaseInitial'] = {
                      'description':'phase of first sample as fraction of 2*pi; \
must be between -0.5 and +0.5',
                      'default':0.,
                      'minimum':-0.5,
                      'maximum':+0.5
                      }
    param['phaseIncrement'] = {
                    'description':'phase advance per sample as fraction of 2*pi; \
by sampling theorem, must be between -0.5 and +0.5',
                    'default':None,
                    'minimum':-0.5,
                    'maximum':+0.5
                    }

    return param

  def param_default(self,param):
    # param = dictionary of parameters
    # returns dictionary populated with parameter default values
    #   using information derived from param
    # this is an authoritative list of parameters that must
    #   be specified by either client or by default
    
    defaults = {}   
    for field in param.keys():
      if 'default' in param[field]:
        defaults[field] = param[field]['default']       
    return defaults
      
  def dispatch(self,op,param):
    # method required by OneDimensionalSignalServer
    #   op = string from client specifying operation
    #   param = dictonary from client specifying parameters
    # returns [response,alert] to be transmitted to client
    #   response = dictonary storing requested info
    #   alert = string containing info not specifically requested

    if op == 'help':
      return [self.parameters,'']

    elif op == 'default':
      return [self.defaults,'']

    elif op == 'set':
      # check availability of all parameters and enforced bounds
      # avoid Python exceptions since client platform may not support this

      # keep going until abort = True
      self.abort = False

      # override default values (where client has specified them)
      p = self.defaults.copy()
      p.update(param)

      # make sure all parameters have been specified
      for field in p.keys():
        if p[field] == None:
          self.abort = True
          return [{},"Error: parameter '{0}' must be specified".format(field)]

      # confirm that all parameters fall within bounds
      if not self.abort:
        for fields in self.parameters.keys():
          if 'minimum' in self.parameters[field]:
            if p[field] < self.parameters[field]['minimum']:
              self.abort = True
              return [{},'Error: parameter {} below minimum'.format(field)]
          if 'maximum' in self.parameters[field]:
            if p[field] > self.parameters[field]['maximum']:
              self.abort = True
              return [{},'Error: parameter {} above maximum'.format(field)]

      # at this point all parameters in p are specified and consistent
      # store them in the object state
      # copy parameters to variables for computational efficiency
      # Example: p['numSamples'] is copied as self.numSamples
      if not self.abort:
        for param in p.keys():
          setattr(self,param,p[param])
        
      return [p,'']


   #   !!! SIGNAL GENERATION UPON REQUEST  !!!
         
  def generate_signal(self,size):
    
    # required method of ComplexSignalServer
    # returns a repeated field of samples as a pair of lists
    # size = number of samples requested
    # this method will be called repeatedly for streaming, and
    #   so must maintain an internal state between calls
    
    if size is not self.last_size:  # Allocate new memory for samples
      self.real = [None] * size; self.imag = [None] * size
    
    for i in range(size):
 
      phase = self.phaseInitial+self.phaseIncrement*(self.samples_sent+i)
      self.real[i] = cos(2*pi*phase)
      self.imag[i] = sin(2*pi*phase)
        
    self.samples_sent += size
    self.last_size = size
    
    return [self.real,self.imag]


if __name__ == '__main__':

  s = ComplexExponentialServer()
  s.run()
