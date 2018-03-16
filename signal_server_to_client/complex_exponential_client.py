"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Programmer: David G Messerschmitt
2 March 2018
"""
from numpy import round

import complex_signal_client as csc

class ComplexExponentialClient(csc.ComplexSignalClient):
    # Client which retreives a complex exonential, making use of the
    # ComplexSignalClient (which retreives a generic complex signal)
    
    def __init__(self):
        super().__init__()

    # There are three phases: discovery, configuration, and run

    def discovery(self):
        # implements a discovery prototol
        self.ask_question(
                            {
                            'what_signal' : True
                            }
                        )

    def configuration(self):
        # sets server configuration parameters
        self.set_parameters(
                                {
                                'signal_name' : 'cexp',
                                'phaseBegin' : 0.,
                                'phaseIncrement' : 0.1
                                }
                            )

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
