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

import buffer
import generic_server as gs

from PROTO_DEFINITIONS import *

# number of gRPC repeated fields, which affects network throughput
# too small and there are a lot of small packets; too large and
#   the network has to fragment the packets
REPEATED_FIELD_COUNT = 10


class StreamingSignalServer(gs.GenericServer):
  
  def __init__(self,p,b,g):
    # p = instance of Parameters class
    # b = instance of ListBuffer class
    # g = instance of signal generation class
    
    super().__init__()

    # instantiate object managing parameters
    self.param = p
    self.buffer = b
    self.generator = g

  def dispatch(self,op,p):
    #   op = string from client specifying operation
    #   p = dictonary from client specifying parameters
    #   returns [response,alert] to be transmitted to client
    #     response = dictonary storing requested info
    #     alert = string containing info not specifically requested

    if op == 'help':
      return [self.param.parameters(),'']

    elif op == 'default':
      return [self.param.defaults(),'']

    elif op == 'set':
      # check availability of all parameters and enforced bounds
      # avoid Python exceptions since client platform may not support this

      # abort = True means further actions are skipped
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

      # initialize signal generator
      self.generator.initialize()
      self.buffer.initialize()
        
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

    # do nothing if something has gone awry previously
    if self.abort: return

    while True:
      
      vals = self.buffer.get(REPEATED_FIELD_COUNT)
      if vals == []: break
      
      # convert to an array of Complex messages
      for i in range(len(vals)):
        r = {'real':vals[i].real,'imag':vals[i].imag}
        vals[i] = self.message.Complex(**r)
      r = {'alert':'','sample' : vals}
      yield self.message.ComplexSample(**r)

