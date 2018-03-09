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

# Configuration
# Adjust this parameter for efficiency
NUM_MESSAGES_PER_RESPONSE = 10

class ComplexSignalServer(gs.GenericServer):
  
  def __init__(self):

    super().__init__()

##    # a method must be provided for each message which returns response to client
##    self.returnBack = getattr(self.grpcMessage,'Back')
##    self.returnConfirm = getattr(self.grpcMessage,'Confirm')
##    self.returnSample = getattr(self.grpcMessage,'Sample')

  # a method must be provided for each rpc channel that processes
  #   request and sends response as defined in .proto file
  # name of method == name of rpc channel

  def Test(self,request,context):

    print('Test message received: ',request.dave)
    r = {'dody' : 'Test message received okay'}
    return self.grpcMessage.Back(**r)

  def SetConfig(self,request,context):

    # pass Param to inherited class, returns message to send back
    r = self.config(request)
    return self.grpcMessage.Confirm(**r)
  
  def GetSignal(self,request,context):

    self.ns = getattr(request,'numSamples')
    
    # Size of each response is NUM_MESSAGES_PER_RESPONSE
    # Number of responses in each repeated field
    self.nr = floor(self.ns/NUM_MESSAGES_PER_RESPONSE)
    # Size of last remaining repeated field
    self.nlo = self.ns % NUM_MESSAGES_PER_RESPONSE

    for j in range(self.nr): # iterate over signal chunks

      # send two repeated fields
      [real,imag] = self.generate_signal(NUM_MESSAGES_PER_RESPONSE)
      r = {'real' : real,'imag' : imag}
      #yield self.returnSample(**r)
      yield self.grpcMessage.Sample(**r)

    # last remaining repeated field, which may 
    if self.nlo == 0: # not needed
      yield None
    else:
      [real,imag] = self.generate_signal(self.nlo)
      r = {'real' : real,'imag' : imag}
      #yield self.returnSample(**r)
      yield self.grpcMessage.Sample(**r)
