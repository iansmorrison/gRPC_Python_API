"""
The Python implementation of a server that returns a
  complex exponential complex-valued signal
Progammer David G Messerschmitt
4 April 2018
"""
import numpy as np
from pprint import pprint

import parameters as param
import message_server as ms
import time_series_generators as tsg

class TimeSeriesServer(ms.StreamingServer):
    '''
    Implements a server which provides a one-dimensional
    stream of complex-valued samples
    The packet size is determined by network efficiency
        considerations
    Generates the actual signal sample values
        including the number of samples per call and the
        total number of samples
    Returns a list of samples, which is empty if the server
        is exhausted
    '''

    def __init__(self):

        # support discovery of different time-series generator types
        self.generators = tsg.Chooser()
        
        # store and manipulate parameter metadata
        self.param = param.Parameters()
	 
        super().__init__()

    def dispatch(self,op,p):
        # implement operation requested by client
        #   op = string from client specifying operation
        #   p = dictonary from client specifying parameters
        #   returns [response,alert] to be transmitted to client
        #     response = dictonary containing requested info
        #     alert = string containing info not specifically requested

        if op == 'service_types?':
            r = {'service_type': self.generators.alternatives()}
            return [r, '']

        if op == 'describe':
            c = p['service_type']
            print('\nClient is asking about service ', c)

            g = self.generators.choice(c)
            r = {c : g.parameters()['description']}
            return [r, '']
            
        if op == 'service_choice':

            c = p['service_choice']
            print('\nClient has chosen service ', c)

            self.gen = self.generators.choice(c)
            if self.gen == None:
                return [{},'Service choice {} not available'.format(c)]

            # get parameters for this service
            t = self.gen.parameters()
            # store for future use and manipulation
            self.param.set(t)
            # send parameters to client in answer message
            return [t,'']

        elif op == 'set':

            print('\nParameter values chosen by client:')
            pprint(p)
            self.param.update(p)
            print('\nFull set of parameter values including client changes:')
            pprint(self.param.final())
            
            # check availability of all parameters and enforced bounds

            # abort = True means further actions are skipped
            self.abort = False

            # make sure all parameters have been specified
            field = self.param.complete()
            if field:
                self.abort = True
                print('\nAborting because a parameter left unspecified')
                return [{},"Error: parameter '{0}' must be specified".format(field)]

            # confirm that all parameters fall within bounds
            field = self.param.bounds()
            if field:
                self.abort = True
                print('\nAborting because a parameter is out of bounds')
                return [{},'Error: parameter {} out of bounds'.format(field)] 

            # initialize signal generator and buffer for a new run
            self.initialize_generator()
            self.buff.initialize()

            return [{},'']

        
    def initialize_generator(self):
        # signal generator may be run more than once, so
        #   define an initialization separate from object instantiation

        self.gen.initialize(self.param.final())
        print('\nNew time-series generator run')
      
    def get(self):
        # called repeatedly by buffer instance to feed it new
        #   frames of time-series values

        vals = self.gen.generate()
        if len(vals) == 0:
            print('Generator run completed')

        return vals
    

if __name__ == '__main__':

    s = TimeSeriesServer()
    s.run()
