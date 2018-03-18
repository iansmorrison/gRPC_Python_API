"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
  
Programmer: David G Messerschmitt
18 March 2018
"""
from numpy import round

import signal_client as csc

class ComplexExponentialClient(csc.ComplexSignalClient):
    # Client which retreives a complex exonential, making use of the
    # ComplexSignalClient (which retreives a generic complex signal)
    
    def __init__(self):
        super().__init__()

    # There are three phases: discovery, configuration, and run

    def discovery(self):
        # get information about service
        print('\nSend help query:')
        self.config_message_and_response('help',{})
        

    def configuration(self):
        # sets server configuration parameters

        # get list of parameters and their defaults from server
        print('\nSend default query:')
        [p,a] = self.config_message_and_response('default',{})

        # change defaults as desired
        p['numSamples'] = 205
        p['phaseIncrement'] = 0.1

        # configure the server parameters
        print('\nSend set config:')
        self.config_message_and_response('set',p)                                      

    def run(self):
        # run the client to return complex exponential with parameters()
        # super class provides get(), which receives a streamed complex signal
        [self.reals,self.imags] = self.get()

    def report(self, resolution=3):
        # print result to standard output with specified resolution
        print('\nReal part of complex exponential ({0} samples):\n'.format(len(self.reals)))
        print(round(self.reals,resolution))
        print('\nImag part of complex exponential ({0} samples):\n'.format(len(self.imags)))
        print(round(self.imags,resolution))
                  

if __name__ == '__main__':
 c = ComplexExponentialClient()
 c.discovery()
 c.configuration()
 c.run()
 c.report()
