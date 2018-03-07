"""
The Python implementation of a server that returns a complex-valued signal
It uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Progammer David G Messerschmitt
5 March 2018
"""
from math import *
import importlib
import generic_server as gs

from PROTO_DEFINITIONS import *

# ComplexSignalServer assumes:
#   the rpc channel is 'GetSignal'
#   received messsages have a field 'numSamples'
#   the return messages are 'stream Sample' with fields 'real' and 'imag'

grpcMessage = importlib.import_module('{0}_pb2'.format(NAME_OF_PROTO_FILE))
sendMessage = getattr(grpcMessage,'Sample')

# Adjust this parameter for efficiency
NUM_MESSAGES_PER_RESPONSE = 10

class ComplexSignalServer(gs.GenericServer):
  
  def __init__(self):
    super().__init__()

  # needs to be a method for each rpc channel that processes
  #   request and sends response as defined in .proto file
  # name of method == name of rpc channel
  
  def GetSignal(self,request,context):
    
    # first deal with the parameters of request
    # first strip off parameters needed by self
    self.ns = getattr(request,'numSamples')
    # remaining parameters not needed

    # second pass remaining parmaters to inherited class
    #   which uses them to generate the signal
    # note that we pass ALL the paramerters
    self.parameters(request)
    
    # Size of each response is NUM_MESSAGES_PER_RESPONSE
    # Number of responses in each repeated field
    self.nr = floor(self.ns/NUM_MESSAGES_PER_RESPONSE)
    # Size of last remaining repeated field
    self.nlo = self.ns % NUM_MESSAGES_PER_RESPONSE

    for j in range(self.nr): # iterate over signal chunks

      # send two repeated fields
      [real,imag] = self.signal(NUM_MESSAGES_PER_RESPONSE)
      r = {'real' : real,'imag' : imag}
      yield sendMessage(**r)

    # last remaining repeated field, which may 
    if self.nlo == 0: # not needed
      yield None
    else:
      [real,imag] = self.signal(self.nlo)
      r = {'real' : real,'imag' : imag}
      yield sendMessage(**r)
