"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
  
Programmer: David G Messerschmitt
18 March 2018
"""
from numpy import round
from pprint import pprint

import signal_client as csc

class ComplexExponentialClient(csc.ComplexSignalClient):
    # Client which retreives a complex exonential, making use of the
    # ComplexSignalClient (which retreives a generic complex signal)
    
    def __init__(self):
        super().__init__()

    # There are three phases: discovery, configuration, and run

    def discovery(self):
        # get information about service
        [r,a] = self.metadata_message_and_response('help',{})
        print('\nParameters supported by server:\n')
        pprint(r)
        

    def configuration(self):
        # sets server configuration parameters

        # from server, get list of parameters and their defaults
        [p,a] = self.metadata_message_and_response('default',{})
        print('\nDefault values of parameters:\n')
        pprint(p)

        # change defaults as desired
        p = {'num_samples':55,'frame':20,'phase_increment':0.1}

        # configure the server parameters
        print('\nChosen parameters sent to server:\n')
        pprint(p)
        [p,a] = self.metadata_message_and_response('set',p)
        if a != '':
            print('\nAlert from server: ',a)

    def run(self):
        # run the client to return complex exponential with parameters()
        # super class provides get(), which receives a streamed complex signal
        # get() returns a generator, so it can be interated only once
        # to access it later, have to store in a list

        for samples in self.get():
            print('\nPacket:\n',samples)
                  

if __name__ == '__main__':
 c = ComplexExponentialClient()
 c.discovery()
 c.configuration()
 c.run()
## c.report()
