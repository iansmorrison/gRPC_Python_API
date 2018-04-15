"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long-duration signals) to return multiple complex samples

Programmer: David G Messerschmitt
18 March 2018
"""

# !!! IF .PROTO FILE IS CHANGED, THIS FILE MUST BE EDITED TO ALIGN NAMES !!!

import json
import inspect
import numpy as np
from pprint import pprint

import parameters as param
import generic_client as gc
import buffer as buff

class TimeSeriesClient(gc.GenericClientStub):
        '''
        Retreives a generic time series
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

        def __init__(self,p,t):
                # p = instance of Parameters storing parameter values
                # t = parameter values set by inherited class

                self.t = t

                # instantiate a buffer, which is used
                #   for conversion of repeated fields to time-series frames
                self.buff = buff.TimeSeriesBuffer(self)

                super().__init__()
	
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

        def discovery(self):
                # get information about server

                [r,a] = self.metadata_message_and_response('help', {})
                print('\nParameters supported by server:\n')
                pprint(r)

        def configuration(self):
                # sets server configuration parameters

		# from server, get list of parameter default values
                [p,a] = self.metadata_message_and_response('default', {})
                print('\nDefault values of parameters:\n')
                pprint(p)

		# change defaults as desired
		# only parameters relevant at this time-series layer
                self.t['service_type'] = 'time_series'
                self.t['num_samples'] = 55

		# configure the server parameters
                print('\nChosen parameters sent to server:\n')
                pprint(self.t)
                self.param_dict_to_var() # store parameter values as variables

                # inform server of what parameter values have been chosen
                [p,a] = self.metadata_message_and_response('set', self.t)
                if a != '':
                        print('\nAlert from server: ', a)

	#   ********** runtime operations *************

        def stream(self):
		# method is invoked to capture signal stream from gRPC channel

		# send op = 'get' to server to ask for a time series to be streamed
                s = self.message.Config(**{
						'operation':'get',
						'parameters':json.dumps('')
						})

		# capture resulting time series
                self.r = self.channel.ComplexTimeSeries(s)

		# r is a generator (to conserve memory) and thus
		#   can only be iterated once by repeated calls to
		#   the get() method

        def frames(self):
                # run the client to return complex exponential with parameters()
                # buff.get() provides a streamed complex time series with
                #   desired self.frame length

                self.stream()   # access time-series from gRPC channel

                # we retrive time-series frames from buffer
                # buffer in turn will repeatedly call self.get() to
                #   retreive streamed values from gRPC
                while True:
                        vals_list = self.buff.get(self.frame)
                        
                        if len(vals_list) == 0: # end of generated time-series
                            self.receive(np.array([]))
                            break

                        # convert to a numpy array object
                        vals_array = np.array(vals_list)
                        
                        # push each list of values to the application layer
                        #   which receive()'s them
                        self.receive(vals_array)

        def run(self):
                # orchestrate stages of operation
                
                self.discovery()
                self.configuration()
                self.frames()
                        
        def param_dict_to_var(self):

                # store final set of parameters as variables for efficiency
                # for example, value of a parameter named 'frame' becomes
                #   variable self.frame
                for field in self.t.keys():
                        setattr(self,field,self.t[field])
                

class ComplexTimeSeriesClient(TimeSeriesClient):
        '''
        Handle the runtime stream of a complex-valued time-series
        Particulars of semantics (WHAT signal is represented)
                are left to an inherited class
        '''

        def __init__(self,p,t):
                # p = instance of Parameters storing parameter values
                # t = parameter values are set by inherited class

                self.t = t

                super().__init__(p,t)


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
               

