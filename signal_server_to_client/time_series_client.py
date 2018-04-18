"""
The Python implementation of a time-series streaming clinet
This version uses a both a repeated field (for efficiency)
  and streaming (for long-duration signals) to return multiple complex samples
It includes support for both real- and complex-valued samples

Programmer: David G Messerschmitt
14 April 2018
"""

# !!! IF .PROTO FILE IS CHANGED, THIS FILE MUST BE EDITED TO ALIGN NAMES !!!

import json
import numpy as np
import inspect
from pprint import pprint

import parameters as param
import generic_client as gc
import buffer as buff
import time_series_receptors as cr

class TimeSeriesClient(gc.GenericClientStub):
        '''
        Retreives a generic time-series from a client stub
        This class handles discovery and configuration, but
                not run-time
        Different inherited class can handle different
                structures of the time-series, like real or complex
        Supports either real-valued or complex-valued time-series
        Connection topology:
            run() calls buffer which calls get() which
                accesses stream() which calls gRPC
            get() has to be supplied by an inherited class
        Current implementation uses a real-valued time-series, but
            this implementation is retained for possible future use
        '''

        def __init__(self):

                # create a dictionary of all available time-series receptors
                #   which are assumed to be implemented as classes in module cr
                self.receptors = {}
                for name, obj in inspect.getmembers(cr,inspect.isclass):
                    self.receptors[name] = obj
            
                # object to store and manipulate parameters
                self.param = param.Parameters()

                # instantiate a buffer and point it to self
                # used for conversion of repeated fields to time-series frames
                self.buff = buff.TimeSeriesBuffer(self)

                self.abort = False # a fatal error has occured?

                super().__init__()
                
        def handle_to_rec(self,handle):
            # look up the receptor class associated with a given handle
            # returns an instance of that class

            for name in self.receptors.keys():
                if self.receptors[name].__handle__ == handle:
                    return self.receptors[name]()
            
	#   ********** metadata and configuration *************

        def metadata_message_and_response(self,op,p):
		# send an operation to the server
		#       op = string specifying desired operation
		#       param = dictonary containing parameters of that op
		# returns server's response in two parts:
		#   response = parameter dictonary
		#   alert = alert string with any information not requesed

		# JSON string representation of param is actually sent
                t = {'operation':op,'parameters':json.dumps(p)}
                s = self.message.Config(**t)
                r = self.channel.MetaDataCoordination(s) # returns response message

		# JSON response message converted to dictonary 
                return [json.loads(r.response), r.alert]

        def discover_and_choose(self):
                # get information about services available, and choose one

                self.abort = False

                # what are the time-series generators available from this server?
                [r,a] = self.metadata_message_and_response('service_types?', {})

                print('\nList of time-series generators available:')
                for name in r['service_type'].keys():
                    print('\nService: {}:'.format(name))
                    print(r['service_type'][name])

                # choose a service and find out its parameterization
                #   (in the future this will probably be obtained from user)
                choice = 'complex_exponential_with_complex_transport'
                
                if choice not in r['service_type'].keys():
                    self.abort = True
                    print('\nChosen service type not available')
                    return
                
                print('\nTime-series generator chosen: ', choice)
                p = {'service_choice' : choice}
                [r,a] = self.metadata_message_and_response('service_choice', p)
                print('\nParameters supported by this generator:\n')
                pprint(r)

                # instantiate a client for this service type
                self.rec = self.handle_to_rec(choice)

                # store parameters for future use and manipulation
                self.param.set(r)

        def configuration(self):
                # sets server configuration parameters

                p = self.param.defaults()
                print('\nDefault values of parameters:\n')
                pprint(p)

		# ask the service layer for parameter values
                p = self.rec.parameters(p)
                self.param.update(p)
                
		# configure the server parameters
                print('\nChosen parameters sent to server:\n')
                pprint(self.param.final())
                # store parameter values in variables
                self.param_dict_to_var()

                # inform server of parameters chosen
                # server returns configuration information for the gRPC transport
                [p,a] = self.metadata_message_and_response('set', self.param.final())
                if a != '':
                        print('\nAlert from server: ', a)
                self.transport = p['transport']
                print('\nTransport request: ',self.transport)

	#   ********** runtime operations *************

        def stream(self):
		# method is invoked to capture signal stream from gRPC channel

		# send op = 'get' to server to ask for a time series to be streamed
                s = self.message.Config(**{
						'operation':'get',
						'parameters':json.dumps('')
						})

                # capture resulting time series
                if self.transport == 'real_valued_streaming':
                    self.r = self.channel.RealTimeSeries(s)
                elif self.transport == 'complex_valued_streaming':
                    self.r = self.channel.ComplexTimeSeries(s)
                else:
                    print(
            '\nUnknown gRPC service {} requested'.format(self.transport)
                        )

		# r is a generator (to conserve memory) and thus
		#   can only be iterated once by repeated calls to
		#   the get() method

                # retrive time-series frames from buffer
                # buffer in turn will repeatedly call self.get() to
                #   retreive streamed values from gRPC
                while True:
                    
                        vals_list = self.buff.get(self.frame)
                        # convert to a numpy array object
                        vals_array = np.array(vals_list)
                        
                        # push each array to the application layer
                        #   which receive()'s them
                        self.rec.receive(vals_array)

                        if vals_array.size == 0: break

        def run(self):
                # orchestrate stages of operation
                
                if not self.abort: self.discover_and_choose()
                if not self.abort: self.configuration()
                if not self.abort: self.stream()
                        
        def param_dict_to_var(self):

                # store final set of parameters as variables for efficiency
                # for example, value of a parameter named 'frame' becomes
                #   variable self.frame
                p = self.param.final()
                for field in p.keys():
                        setattr(self,field,p[field])
                

class ComplexTimeSeriesClient(TimeSeriesClient):
        '''
        Handle the runtime stream of a complex-valued time-series
        Particulars of semantics (WHAT signal is represented)
                are left to an inherited class
        '''

        def __init__(self):

                super().__init__()


        def get(self):
		# get next value from r, convert to complex values,
		#   store in list, and return
		# this method will be called repeatedly by an instance
		#   of a TimeSeriesBuffer, which will store it in a
		#   buffer for access by the application layer in
		#   time series frames

                rnext = next(self.r, None) # None = default if no more data
                if rnext == None: return [] # signals end of streaming

		# each rnext.sample is a repeated field, represented as list
                size = len(rnext.sample) # number of samples

		# convert to array of complex numbers
                vals = [None] * size
                for i in range(size):
                        vals[i] = complex(rnext.sample[i].real,rnext.sample[i].imag)
                return vals
               

if __name__ == '__main__':

    s = ComplexTimeSeriesClient()
    s.run()
