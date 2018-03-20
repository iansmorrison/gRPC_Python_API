"""
The Python implementation of a server that returns a
  complex exponential complex-valued signal
Progammer David G Messerschmitt
18 March 2018
"""
from math import pi,sin,cos
from pprint import pprint

import signal_server as css

class ComplexExponentialServer(css.OneDimensionalSignalServer):
  
  def __init__(self):
    
    super().__init__()

    self.param = css.Parameters(self.param_define())
    print('\nParameters:\n')
    pprint(self.param.parameters())
    print('\nDefaults:\n')
    pprint(self.param.defaults())

    self.parameters = self.param.parameters()
    self.defaults = self.param.defaults()
    
##    # generate parameter dictionaries for this signal semantics
##    self.parameters = self.param_define()
##    self.defaults = self.param_default(self.parameters)

    # establish name for lists containing repeated fields
    self.real = []; self.imag = []

    # if an error occurs, setting this variable to False will
    #   stop further actions
    self.abort = False

  #   !!! CONFIGURATION  !!!

  def param_define(self):
    # defines the parameters for this signal, their bounds and their defaults
    # returns a dictonary containing this information
    # Note: all numerical parameters must have a 'default' field
    #     (set to None if client is required to supply this parameter)

    p = {'semantics':'cexp'}
    p['description'] = 'service returns samples of a complex exponential \
cos(2*pi*phase) + i * sin(2*pi*phase)'
    p['numSamples'] = {
                      'description':'total duration of signal',
                      'default':None,
                      'minimum':1
                      }
    p['phaseInitial'] = {
                      'description':'phase of first sample as fraction of 2*pi; \
must be between -0.5 and +0.5',
                      'default':0.,
                      'minimum':-0.5,
                      'maximum':+0.5
                      }
    p['phaseIncrement'] = {
                    'description':'phase advance per sample as fraction of 2*pi; \
by sampling theorem, must be between -0.5 and +0.5',
                    'default':None,
                    'minimum':-0.5,
                    'maximum':+0.5
                    }

    return p

##  def param_default(self,param):
##    # param = dictionary of parameters
##    # returns dictionary populated with parameter default values
##    #   using information derived from param
##    # this is an authoritative list of parameters that must
##    #   be specified by either client or by default
##    
##    defaults = {}   
##    for field in param.keys():
##      if 'default' in param[field]:
##        defaults[field] = param[field]['default']       
##    return defaults
      
  def dispatch(self,op,p):
    # method required by OneDimensionalSignalServer
    #   op = string from client specifying operation
    #   p = dictonary from client specifying parameters
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
##      p = self.defaults.copy()
##      p.update(param)
      po = self.param.override_defaults(p)

      # make sure all parameters have been specified
      for field in po.keys():
        if po[field] == None:
          self.abort = True
          return [{},"Error: parameter '{0}' must be specified".format(field)]

      # confirm that all parameters fall within bounds
      if not self.abort:
        for fields in self.parameters.keys():
          if 'minimum' in self.parameters[field]:
            if po[field] < self.parameters[field]['minimum']:
              self.abort = True
              return [{},'Error: parameter {} below minimum'.format(field)]
          if 'maximum' in self.parameters[field]:
            if po[field] > self.parameters[field]['maximum']:
              self.abort = True
              return [{},'Error: parameter {} above maximum'.format(field)]

      # at this point all parameters in p are specified and consistent
      # store them in the object state
      # copy parameters to variables for computational efficiency
      # Example: p['numSamples'] is copied as self.numSamples
      if not self.abort:
        for name in po.keys():
          setattr(self,name,po[name])
        
      return [po,'']

   #   !!! SIGNAL GENERATION UPON REQUEST  !!!
         
  def generate_signal(self,start,size):
    
    # required method of ComplexSignalServer
    # returns a repeated field of samples as a pair of lists
    # size = number of samples requested
    # this method will be called repeatedly for streaming, and
    #   so must maintain an internal state between calls

    # Allocate new memory for samples (unless already allocated)
    if len(self.real) != size:
      self.real = [None] * size; self.imag = [None] * size
    
    for i in range(size):
      phase = self.phaseInitial+self.phaseIncrement*(start+i)
      self.real[i] = cos(2*pi*phase)
      self.imag[i] = sin(2*pi*phase)
            
    return [self.real,self.imag]


if __name__ == '__main__':

  s = ComplexExponentialServer()
  s.run()
