"""
The Python implementation of a complex signal server
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Progammer David G Messerschmitt
2 March 2018
"""
import math
import generic_server as gs

class ComplexSignalServer(gs.GenericServer):

  def __init__(self):

    # initialize messageFields[][]
    super().__init__()

    # defaults here
    
  def response(self,message):

    if message == 'Request':

        # extract requested signal parameters
        phaseIncrement = self.messageFields['Request']['phaseIncrement']
        numSamples = self.messageFields['Request']['numSamples']

        # generate requested signal with those parameters       
        vals = [None] * numSamples
        for i in range(numSamples):
          vals[i] = math.cos(2*math.pi*phaseIncrement*i)
          
        self.messageFields['Signal']['real'] = vals
    
if __name__ == '__main__':

  s = ComplexSignalServer()
  s.run()
  s.report() # view final state of messageFields
