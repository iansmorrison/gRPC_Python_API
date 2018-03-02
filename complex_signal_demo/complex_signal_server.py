"""
The Python implementation of a complex signal server
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Progammer David G Messerschmitt
2 March 2018
"""

import generic_server as gs

class ComplexSignalServer(gs.GenericServer):

  def __init__(self):

    # initialize messageFields[][]
    super().__init__()

    # defaults
    self.messageFields['Signal']['phaseIncrement'] = 0.25
    self.messageFields['Signal']['numSamples'] = 10
    

  def response(self,message):

    if message == 'Request':

        # extract requested signal parameters
        phaseIncrement = self.messageFields['Request']['phaseIncrement']
        numSamples = self.messageFields['Request']['numSamples']

        # generate requested signal with those parameters
        self.messageFields['Signal']['phaseIncrement'] = phaseIncrement
        self.messageFields['Signal']['numSamples'] = numSamples
        self.messageFields['Signal']['real'] = 1.0
    
if __name__ == '__main__':

  s = ComplexSignalServer()
  s.run()
  s.report() # view final state of messageFields
