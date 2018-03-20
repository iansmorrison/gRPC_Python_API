"""
The Python implementation of a server that returns a complex-valued signal
It uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Progammer David G Messerschmitt
18 March 2018
"""
import importlib
import json
from math import floor

import generic_server as gs

from PROTO_DEFINITIONS import *

# Configuration
NUM_MESSAGES_PER_RESPONSE = 10  # Adjust for efficiency

class OneDimensionalSignalServer(gs.GenericServer):
  
  def __init__(self):
    super().__init__()

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
    self.nr = floor(self.numSamples/NUM_MESSAGES_PER_RESPONSE)
    # Size of last remaining repeated field
    self.nlo = self.numSamples % NUM_MESSAGES_PER_RESPONSE
    size = NUM_MESSAGES_PER_RESPONSE
    
    for j in range(self.nr): # iterate over repeated fields

      # send real and imag repeated fields
      start = NUM_MESSAGES_PER_RESPONSE*j
      [real,imag] = self.generate_signal(start,size)
      r = {'alert':'','real' : real,'imag' : imag}
      yield self.message.ComplexSample(**r)

    # last remaining repeated field
    if self.nlo == 0: # we are done
      yield None
    else:
      start = NUM_MESSAGES_PER_RESPONSE*self.nr
      size = self.nlo
      [real,imag] = self.generate_signal(start,size)
      r = {'alert':'','real' : real,'imag' : imag}
      yield self.message.ComplexSample(**r)

class Parameters:
  # To make implementation of server easier, class
  #   provides some useful functions to store and manage parameters

  def __init__(self,p):
    
    # Argument p = provided parameter dictionary
    self.p = p

    # Extract and a dictionary with only default values
    self.d = {}   
    for field in self.p.keys():
      if 'default' in self.p[field]:
        self.d[field] = self.p[field]['default']

  def parameters(self):
    return self.p
  
  def defaults(self):
    return self.d

  def override_defaults(self,p):
    # p = dictionary of values
    # returns self.d overridden by p
    t = self.d.copy()
    t.update(p)
    return t
  
