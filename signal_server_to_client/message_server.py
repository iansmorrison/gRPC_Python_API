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

import buffer as buff
import generic_server as gs

from PROTO_DEFINITIONS import *

# number of gRPC repeated fields, which affects network throughput
# too small and there are a lot of small packets; too large and
#   the network has to fragment the packets
REPEATED_FIELD_COUNT = 10


class StreamingServer(gs.GenericServer):
  
  def __init__(self):
    
    super().__init__()

    # a buffer to store signal values as they are generated
    self.buff = buff.TimeSeriesBuffer(self)
##    self.generator = g

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

  def RealTimeSeries(self,request,context):

    # responds to request for streamng of real values
    # manages the splitting of signal into repeated fields

    # do nothing if something has gone awry previously
    if self.abort: return

    while True:
      
      # get a list of floating values to pass to gRPC
      vals = self.buff.get(REPEATED_FIELD_COUNT)
      if vals == []: break  # no more values to transmit
      
      # convert to an list of messages
      #   which will be transmitted as a repeated field
      r = {'sample' : vals}
      yield self.message.RealSample(**r)
      
  def ComplexTimeSeries(self,request,context):

    # responds to request for streamng of complex signal
    # manages the splitting of signal into repeated fields

    # do nothing if something has gone awry previously
    if self.abort: return

    while True:
      
      vals = self.buff.get(REPEATED_FIELD_COUNT)
      if vals == []: break
      
      # convert to an array of Complex messages
      for i in range(len(vals)):
        r = {'real':vals[i].real,'imag':vals[i].imag}
        vals[i] = self.message.Complex(**r)
      r = {'sample' : vals}
      yield self.message.ComplexSample(**r)

