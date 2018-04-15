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
from pprint import pprint
import matplotlib.pyplot as plt

import parameters as param
import generic_client as gc
import buffer as buff

class TimeSeriesClient(gc.GenericClientStub):
        '''
        Retreives a generic complex-valued time series
        Particulars of semantics (WHAT signal is represented)
                are left to an inherited class
        '''

        def __init__(self,p,t):
                # p = instance of Parameters storing parameter values
                # t = parameter values set by inherited class

                self.t = t

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
                return [json.loads(r.response),r.alert]

        def discovery(self):
                # get information about server

                [r,a] = self.metadata_message_and_response('help',{})
                print('\nParameters supported by server:\n')
                pprint(r)

        def configuration(self):
                # sets server configuration parameters

		# from server, get list of parameter default values
                [p,a] = self.metadata_message_and_response('default',{})
                print('\nDefault values of parameters:\n')
                pprint(p)

		# change defaults as desired
		# only parameters relevant at this time-series layer
                self.t['service_type'] = 'time_series'
                self.t['num_samples'] = 55

		# configure the server parameters
                print('\nChosen parameters sent to server:\n')
                pprint(self.t)
                self.param_dict_to_var()
                [p,a] = self.metadata_message_and_response('set',self.t)
                if a != '':
                        print('\nAlert from server: ',a)

        def param_dict_to_var(self):

                # store final set of parameters as variables for efficiency
                # for example, parameter 'frame' becomes self.numSamples
                for field in self.t.keys():
                        setattr(self,field,self.t[field])
                
	#   *****************  runtime streaming ******************

        def stream(self):
		# method is invoked to capture signal stream from gRPC channel

		# send op = 'get' to server to ask for a time series to be streamed
                s = self.message.Config(**{
						'operation':'get',
						'parameters':json.dumps('')
						})

		# capture resulting time series
##                self.r = self.channel.OneDimensionalSignal(s)
                self.r = self.channel.ComplexTimeSeries(s)

		# r is a generator (to conserve memory) and thus
		#   can only be iterated once by repeated calls to
		#   the get() method

        def get(self):
		# get next value from r, convert to complex values,
		#   store in list, and return
		# this method will be called repeatedly by an instance
		#   of a TimeSeriesBuffer

                rnext = next(self.r,None)
                if rnext == None: return [] # signals end of streaming

		# each rnext.sample is a repeated field, represented as list
                size = len(rnext.sample) # number of samples

		# convert to array of complex numbers
                vals = [None] * size
                for i in range(size):
                        vals[i] = complex(rnext.sample[i].real,rnext.sample[i].imag)
                return vals
                
        def run(self):
                # run the client to return complex exponential with parameters()
                # buff.get() provides a streamed complex time series

                self.stream()   # access time-series from gRPC channel

                while True:
                        vals = self.buff.get(self.frame)
                        if len(vals) == 0: break
                        self.display_frame(vals[:]) 

        def display_frame(self,vals):

                # print 
                # round for purposes of display
                for i in range(len(vals)):
                        vals[i] = complex(
                                round(vals[i].real,2),
                                round(vals[i].imag,2)
                                )
                print('\nOne frame of size = ',len(vals),'\n',vals)

##                # plot
##                plt.plot(t,s.real,t,s.imag)
##                plt.axis([0,numSamples*T,-1,+1])
##                plt.title('Magnitude of exp(x)')
##                plt.show()
