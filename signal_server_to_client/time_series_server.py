"""
The Python implementation of a server that returns a
  complex exponential complex-valued signal
Progammer David G Messerschmitt
4 April 2018
"""

import inspect
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

        # create a dictionary of all available generators
        #   which are assumed to be implemented as classes in module tsg
        self.generators = {}
        for name, obj in inspect.getmembers(tsg,inspect.isclass):
            self.generators[name] = obj

        # create a dictonary with documentation for each generator
        self.generators_desc = {}
        for name in self.generators.keys():
            # __handle__ is the 'popular' name for a time-series
            #       generator, suitable for presenting to user
            # __handle__ must be specified by the generator class
            #       as a class variable
            handle = self.generators[name].__handle__
            docstring = inspect.getdoc(self.generators[name])
            self.generators_desc[handle] = docstring
                   
        # a place to store and manipulate parameter metadata
        self.param = param.Parameters()
	 
        super().__init__()

    def handle_to_gen(self,handle):
        # look up the generator class associated with a given handle
        # returns an instance of that class
        
        for name in self.generators.keys():
            if self.generators[name].__handle__ == handle:
                return self.generators[name]()
    
    def dispatch(self,op,p):
        # implement operation requested by client
        #   op = string from client specifying operation
        #   p = dictonary from client specifying parameters
        #   returns [response,alert] to be transmitted to client
        #     response = dictonary containing requested info
        #     alert = string containing info not specifically requested

        if op == 'service_types?':

            r = { 'service_type' : self.generators_desc }
            return [r, '']
            
        if op == 'service_choice':

            c = p['service_choice']           
            if c not in self.generators_desc.keys():
                return [{},'Time-series generator {} not available'.format(c)]
            print('\nClient has chosen time-series generator ', c)

            # instantiate the chosen signal generator class
            self.gen = self.handle_to_gen(c)
            
            # get parameter dictionary for this service
            t = self.gen.parameters()
            # add handle and docstrings as an aid to the client
            t['handle'] = self.gen.__handle__
            t['description'] = self.gen.__doc__

            # store parameter dictionary for future use and manipulation
            self.param.set(t)
            
            # send parameter dictionary to client in answer message
            return [t,'']

        elif op == 'set':
            # configuration of server and client for this service
            #   with parameters provided by client

            print('\nParameter values chosen by client:')
            pprint(p)
            self.param.update(p)
            print('\nFull set of parameter values including client changes:')
            pprint(self.param.final())
            
            # check availability of all parameters and enforced bounds

            # abort = True => further actions are skipped
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

            # store parameters as variables in time-series generator object
            self.param_dict_to_var(self.gen, self.param.final())
            
            # initialize signal generator for a new run
            # returns s = set of transport-layer parameters which will
            #   be returned to the client for compatible configuation
            s = self.gen.initialize()           
            print('\nNew time-series generator run with transport configuration:')
            pprint(s)

            # capture the shapes for later consistency checks
            self.shapes = s['array_shapes']

            # initialize the time-division multiplexing state
            self.sent = 0

            # initialize buffer for a new run
            self.buff.initialize()

            return [s,'']

    def param_dict_to_var(self,obj,p):
        # stores a set of parameters as variables for efficiency
        # obj = object whose attributes are set
        #   (typically a time-series generator)
        # p = a dictonary of parameter values
        # for example, value of a parameter named 'frame' becomes
        #   a variable self.frame in object obj

        for field in p.keys():
            setattr(obj,field,p[field])       
      
    def get(self):
        # called repeatedly by buffer instance to feed it new
        #   frames of time-series values
        # in turn it calls the time-series generate() function to return
        #   a list of numpy array's assumed to contain time-series values
        #   which are to be time-division multiplexed

        if self.sent == 0:
            # all time-division muliplexed time-series have been sent, so
            #   call generate() to replenish a new list of time-series array's
            self.vals_list = self.gen.generate()
            
            if not isinstance(self.vals_list, list):
                print("\nError: Time series generator output is not a list of time-series array's")
                return []
            elif len(self.vals_list) == 0:
                print('\nGenerator run completed')
                return []
            elif not len(self.vals_list) == len(self.shapes):
                print('\nError: Time series generator returned list of time-series with wrong length')
                return []
        
        vals = self.vals_list[self.sent]
        self.sent += 1
        if self.sent == len(self.vals_list):
            self.sent = 0
        
        if not isinstance(vals, np.ndarray):
            print('\nError: Time-series generator failed to return a numpy array')
            print('\nValues returned:\n',vals)
            return []
        
        # flatten the numpy array and convert to a 1-D list
        # this serializes the values for transport over RPC
        return list(np.ravel(vals))
    

if __name__ == '__main__':

    s = TimeSeriesServer()
    s.run()
