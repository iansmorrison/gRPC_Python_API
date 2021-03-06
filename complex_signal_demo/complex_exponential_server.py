"""
The Python implementation of a server that returns a
  complex exponential complex-valued signal
Progammer David G Messerschmitt
6 March 2018
"""
from math import pi,sin,cos

import complex_signal_server as css

class ComplexExponentialServer(css.ComplexSignalServer):
  
  def __init__(self):
    
    super().__init__()
    
    self.samples_sent = 0  # number of signal samples already sent
    self.last_size = -1  # size of last repeated field sent

  #   !!! DISCOVERY  !!!

  def discovery(self,request):
    # method required by ComplexSignalServer
    # argument is request message from client
    # returns response message stored in a dictionary

    if request.what_signal:
      return [
        'cexp: complex exponential',
        'file: signal stored in file (not yet implemented)'
        ]

  #   !!! CONFIGURATION  !!!

  def configuration(self,request):
    # method required by ComplexSignalServer
    # argument is request message from client
    # returns response message stored in a dictionary

    self.signal_name = request.signal_name
    self.pB = request.phaseBegin
    self.pI = request.phaseIncrement

    if self.signal_name != 'cexp':
      return {
        'okay' : False,
        'narrative' : 'Signal description not recognized'
        }
    elif not -0.5 < self.pI < 0.5:
      return {
        'okay':False,
        'narrative':'Phase increment violates sampling theorem'
        }
    else: return {
        'okay':True,
        'narrative':'Signal will be provided as requested'
        }

   #   !!! RUN  !!!
         
  def generate_signal(self,size):
    
    # required method of ComplexSignalServer
    # returns a repeated field of samples as a pair of lists
    # size = number of samples requested
    # this method will be called repeatedly for streaming, and
    #   so must maintain an internal state between calls
    
    if size is not self.last_size:  # Allocate new memory for samples
      self.real = [None] * size; self.imag = [None] * size
    
    for i in range(size):
 
      phase = self.pB + self.pI * (self.samples_sent + i)
      self.real[i] = cos(2*pi*phase)
      self.imag[i] = sin(2*pi*phase)
        
    self.samples_sent += size
    self.last_size = size
    
    return [self.real,self.imag]
         
    
if __name__ == '__main__':

  s = ComplexExponentialServer()
  s.run()
