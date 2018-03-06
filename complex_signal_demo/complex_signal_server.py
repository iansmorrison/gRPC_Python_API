"""
The Python implementation of a complex signal server
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Progammer David G Messerschmitt
2 March 2018
"""
from math import *
import importlib
import generic_server as gs

from PROTO_DEFINITIONS import *

# Use repeated message fields to group messages in single packet
# Number of messages is chosen for efficiency
NUM_MESSAGES_PER_RESPONSE = 10
# Too small results in more packets than necessary
# Too large results in packet fragmentation and more packets

grpcMessage = importlib.import_module('{0}_pb2'.format(NAME_OF_PROTO_FILE))
sendMessage = getattr(grpcMessage,'Sample') # gRPC method for sends

class ComplexSignalServer(gs.GenericServer):

  number = 0  # keeps track of number of samples sent
  
  def __init__(self):

    # initialize messageFields[][]
    super().__init__()

    # (optional) defaults here

  # needs to be a method like this for each rpc channel that processes
  # request and sends response
  # name of method == name of rpc channel
  def GetSignal(self,request,context):

    self.pb = request.phaseBegin
    self.pi = request.phaseIncrement
    self.ns = request.numSamples
    # Size of each response is NUM_MESSAGES_PER_RESPONSE
    # Number of responses
    self.nr = floor(self.ns/NUM_MESSAGES_PER_RESPONSE)
    # Size of last response
    self.nlo = self.ns % NUM_MESSAGES_PER_RESPONSE
    # Allocate memory for response
    sample_array_real = [None] * NUM_MESSAGES_PER_RESPONSE
    sample_array_imag = [None] * NUM_MESSAGES_PER_RESPONSE
    sample_array_last_real = [None] * self.nlo
    sample_array_last_imag = [None] * self.nlo

    # generate nr 
    for j in range(self.nr):
      for i in range(NUM_MESSAGES_PER_RESPONSE):
        phase = request.phaseBegin + request.phaseIncrement * (i+j*NUM_MESSAGES_PER_RESPONSE)
        sample_array_real[i] = cos(2*pi*phase)
        sample_array_imag[i] = sin(2*pi*phase)
      r = {'real' : sample_array_real,'imag' : sample_array_imag}
      yield sendMessage(**r)

    for i in range(self.nlo):
      phase = request.phaseBegin + request.phaseIncrement * (i+self.nr*NUM_MESSAGES_PER_RESPONSE)
      sample_array_last_real[i] = cos(2*pi*phase)
      sample_array_last_imag[i] = sin(2*pi*phase)
    r = {'real' : sample_array_last_real,'imag' : sample_array_last_imag}
    yield sendMessage(**r)
      
    
if __name__ == '__main__':

  s = ComplexSignalServer()
  s.run()
  #s.report() # view final state of messageFields
