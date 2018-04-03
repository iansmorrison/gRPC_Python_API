"""
The Python implementation of a server that returns a complex-valued signal
It uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Progammer David G Messerschmitt
18 March 2018
"""
import importlib
import json
import cmath
from math import floor
from pprint import pprint

import generic_server as gs

from PROTO_DEFINITIONS import *

# Configuration
NUM_MESSAGES_PER_RESPONSE = 10  # Adjust for efficiency

class OneDimensionalSignalServer(gs.GenericServer):
  
  def __init__(self):
    super().__init__()

    # instantiate object managing parameters
    # param_define() returns the parameter dictionary
    self.param = Parameters(self.param_define())

  def dispatch(self,op,p):
    #   op = string from client specifying operation
    #   p = dictonary from client specifying parameters
    # returns [response,alert] to be transmitted to client
    #   response = dictonary storing requested info
    #   alert = string containing info not specifically requested

    if op == 'help':
      return [self.param.parameters(),'']

    elif op == 'default':
      return [self.param.defaults(),'']

    elif op == 'set':
      # check availability of all parameters and enforced bounds
      # avoid Python exceptions since client platform may not support this

      # abort = True further actions are skipped
      self.abort = False

      # override default values (where client has specified them)
      self.param.update(p)

      # make sure all parameters have been specified
      field = self.param.complete()
      if field:
        self.abort = True
        return [{},"Error: parameter '{0}' must be specified".format(field)]

      # confirm that all parameters fall within bounds
      field = self.param.bounds()
      if field:
        self.abort = True
        return [{},'Error: parameter {} out of bounds'.format(field)]
      
      # copy parameters to variables for computational efficiency
      # Example: p['numSamples'] is copied as self.numSamples
      if not self.abort:
        p = self.param.final()
        for field in p.keys():
          setattr(self,field,p[field])
        
      return [self.param.final(),'']

  # a method must be provided for each rpc channel that processes
  #   request and sends response as defined in .proto file
  # name of method == name of rpc channel

  def MetaDataCoordination(self,request,context):
    # pass request to inherited class, which returns message to send back
    # messages are signal-specific, so we simply pass-thru
    #   messages are 

    # request.operation = string denoting desired action or information
    # request.parameters = JSON-serialized string representing
    #   parameter dictionary

    # pass operation and parameters to inherited class to interpret
    # returns list containing
    #   response = dictonary containing response
    #   alert = string with any alert message
    [response,alert] = self.dispatch(
                          request.operation,
                          json.loads(request.parameters)
                          )
    
    # transmit to client
    # store in a dictionary, with 'response' as a JSON-encoded string
    r = {
      'response':json.dumps(response),
      'alert':alert
      }
    return self.message.Info(**r)
  
  def OneDimensionalSignal(self,request,context):
    # responds to request for streamng of complex signal
    # manages the splitting of signal into repeated fields

    # do nothing if something has gone wrong previously
    if self.abort: return
    
    # Number of responses in each repeated field
    self.nr = floor(self.num_samples/NUM_MESSAGES_PER_RESPONSE)
    # Size of last remaining repeated field
    self.nlo = self.num_samples % NUM_MESSAGES_PER_RESPONSE
    size = NUM_MESSAGES_PER_RESPONSE
    
    for j in range(self.nr): # iterate over repeated fields

      # send real and imag repeated fields
      start = NUM_MESSAGES_PER_RESPONSE*j
##      [real,imag] = self.generate(start,size)
##      r = {'alert':'','real' : real,'imag' : imag}
##      yield self.message.ComplexSample(**r)
      
      sample = self.generate(start,size)
      # convert to an array of Complex messages
      for i in range(len(sample)):
        r = {'real':sample[i].real,'imag':sample[i].imag}
        sample[i] = self.message.Complex(**r)
      r = {'alert':'','sample' : sample}
      yield self.message.ComplexSample(**r)
      

    # last remaining repeated field
    if self.nlo == 0: # we are done
      yield None
    else:
      start = NUM_MESSAGES_PER_RESPONSE*self.nr
      size = self.nlo
##      [real,imag] = self.generate(start,size)
##      r = {'alert':'','real' : real,'imag' : imag}
##      yield self.message.ComplexSample(**r)

      sample = self.generate(start,size)
      # convert to an array of Complex messages
      for i in range(len(sample)):
        r = {'real':sample[i].real,'imag':sample[i].imag}
        sample[i] = self.message.Complex(**r)
      r = {'alert':'','sample' : sample}
      yield self.message.ComplexSample(**r)

class Parameters:
  # class to store and manage parameter dictionaries

  def __init__(self,p):
    
    # argument p = provided parameter dictionary
    self.p = p
    
    # extract a smaller dictionary d with only default values
    self.d = {}   
    for field in self.p.keys():
      if 'default' in self.p[field]:
        self.d[field] = self.p[field]['default']

    # store a dictonary t with default values overridden by
    #   client-specified values
    self.t = {}

  def parameters(self):
    return self.p
  
  def defaults(self):
    return self.d

  def update(self,c):
    # c = dictionary of values that are to override the current values
    # returns self.d overridden by c
    self.t = self.d.copy()
    self.t.update(c)
    return

  def complete(self):
    # checks final parameters r to make sure there are no missing values
    # returns either None or the name of the first encountered missing parameter
    for field in self.t.keys():
        if self.t[field] == None:
          return field
    return None

  def bounds(self):
    # checks final parameters r to make sure there are no
    #   value below minimum or above maximum
    # returns either None or the name of the first encountered problematic value
    for field in self.p.keys():
      if 'minimum' in self.p[field]:
        if self.t[field] < self.p[field]['minimum']:
          return field
      if 'maximum' in self.p[field]:
        if self.t[field] > self.p[field]['maximum']:
          return field
    return None

  def final(self):
    # return final set of parameters for signal generation
    return self.t
