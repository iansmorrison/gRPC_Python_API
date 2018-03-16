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
NUM_MESSAGES_PER_RESPONSE = 10  # Adjust for efficiency

class ComplexSignalServer(gs.GenericServer):
  
  def __init__(self):
    super().__init__()

  # a method must be provided for each rpc channel that processes
  #   request and sends response as defined in .proto file
  # name of method == name of rpc channel

  def Query(self,request,context):
    # pass request to inherited class, which returns message to send back
    # messages are signal-specific, so we do not process content here
    
    signals = self.discovery(request)
    r = {'signal_name' : signals}
    return self.message.Answer(**r)

  def SetConfig(self,request,context):
    # pass request to inherited class, which returns message to send back
    # messages are signal-specific, so we do not process content here
    
    r = self.configuration(request)
    return self.message.Confirm(**r)
  
  def GetSignal(self,request,context):

    self.ns = getattr(request,'numSamples')
    
    # Number of responses in each repeated field
    self.nr = floor(self.ns/NUM_MESSAGES_PER_RESPONSE)
    # Size of last remaining repeated field
    self.nlo = self.ns % NUM_MESSAGES_PER_RESPONSE

    for j in range(self.nr): # iterate over signal chunks

      # send two repeated fields
      [real,imag] = self.generate_signal(NUM_MESSAGES_PER_RESPONSE)
      r = {'real' : real,'imag' : imag}
      yield self.message.Sample(**r)

    # last remaining repeated field
    if self.nlo == 0: # not needed
      yield None
    else:
      [real,imag] = self.generate_signal(self.nlo)
      r = {'real' : real,'imag' : imag}
      yield self.message.Sample(**r)
