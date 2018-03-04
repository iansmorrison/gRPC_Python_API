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

grpcMessage = importlib.import_module('{0}_pb2'.format(NAME_OF_PROTO_FILE))
sendMessage = getattr(grpcMessage,'Signal') # gRPC method for sends

class ComplexSignalServer(gs.GenericServer):

  number = 0  # keeps track of number of samples sent
  
  def __init__(self):

    # initialize messageFields[][]
    super().__init__()

    self.num = 0 # number of signal samples already streamed
    self.pb = 0.
    self.pi = .25
    self.ns = 10

    # (optional) defaults here

  def GetSignal(self,request,context):

    self.pb = request.phaseBegin
    self.pi = request.phaseIncrement
    self.ns = request.numSamples

    for i in range(self.ns):
      phase = request.phaseBegin + request.phaseIncrement * i
      r = {'real' : cos(2*pi*phase)}
      yield sendMessage(**r)
  
  def respond(self,rpc,recd,sent):

    if self.num == 0 and rpc == 'Request':

        print('Call to server with these parameters:')
        
        # extract requested signal parameters only once
        self.pb = self.messageFields['Request']['phaseBegin']
        self.pi = self.messageFields['Request']['phaseIncrement']
        self.ns = self.messageFields['Request']['numSamples']
        

    # generate one more sample with those parameters
    print(self.pb,self.pi,self.num,self.ns)
    phase = self.pb + self.pi * self.num
    self.messageFields['Signal']['real'] = cos(phase)
                                
    self.num = self.num + 1
    
    if self.num < self.ns:  return True   # more samples to be streamed                   
    else: return False  # we are done
    
if __name__ == '__main__':

  s = ComplexSignalServer()
  s.run()
  #s.report() # view final state of messageFields
