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
import matplotlib.pyplot as plt

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

		# ask the receptor for changes to parameter values
                p = self.rec.parameters()
                self.param.update(p)
                
		# configure the server parameters
                print('\nChosen parameters sent to server:\n')
                pprint(self.param.final())
                # store parameter values in variables for efficiency
                self.param_dict_to_var()

                # inform server of parameters chosen
                # server returns generator configuration information
                [p,a] = self.metadata_message_and_response('set', self.param.final())
                if a != '':
                        print('\nAlert from server: ', a)

                # in p = the configuration information returned, we are expecting
                #   'data_type' = 'real' or 'complex'
                #   'array_shapes' = list of numpy ndarray shapes for the time-series
                #       each such array shape is a list

                # 'data_type' determines which RPC channel we invoke
                self.rpc = p['data_type']
                print('\nData type to be used: ',self.rpc)

                # 'array_shapes' specifies the shapes of the numby arrays
                #   so that they can be recovered from the serialized versions
                self.shapes = p['array_shapes'] # list of shapes
                self.num = len(self.shapes) # number of multiplexed time-series
                # sizes of the respective serialized arrays
                self.sizes = [None] * self.num
                for i in range(self.num):
                    self.sizes[i] = np.prod(self.shapes[i])
                
                # configure the receptor
                self.rec.shapes(self.shapes)
                
                print('\nShapes of the generated arrays:')
                for i in range(len(self.shapes)):
                    print('Time-series {}: '.format(i+1),self.shapes[i])

	#   ********** runtime operations *************

        def stream(self):
		# method is invoked to capture signal stream from gRPC channel

		# send op = 'get' to server to ask for a time series to be streamed
                s = self.message.Config(**{
						'operation':'get',
						'parameters':json.dumps('')
						})

                # invoke the appropriate RCP channel for 'data_type"
                #   chosen by the time-series generator
                # capture resulting time series
                if self.rpc == 'real':
                    self.r = self.channel.RealTimeSeries(s)
                elif self.rpc == 'complex':
                    self.r = self.channel.ComplexTimeSeries(s)
                else:
                    self.abort = True
                    print(
            '\nUnknown RPC channel {} requested by server'.format(self.rpc)
                        )

		# r = a generator (to conserve memory) and thus
		#   can only be iterated once by repeated calls to
		#   the get() method

        def get(self):
		# get next repeated field from r and return that list
		# this method will be called repeatedly by a buffer
		#   which stores the list for later access by the signal receptor

                rnext = next(self.r, None) # None = default if no more data
                if rnext == None: return [] # signals end of streaming

		# each rnext.sample is a repeated field, represented as list
                if self.rpc == 'real':
                    return rnext.sample
                else: # must be 'complex'
                    size = len(rnext.sample)
                    vals = [None] * size
                    for i in range(size):
                            vals[i] = complex(
                                rnext.sample[i].real,
                                rnext.sample[i].imag
                                )
                    return vals

        def retrieve(self):
            # fetch a stream of lists with 'real' or 'complex'values from
            #   buffer, convert to numpy array's, reshape, and push to
            #   the time-series receptor
            # returns a list of numpy arrays,
            #   one for each time-multiplexed series

            while True:

                # time-series of different shapes are time-division multiplexed
                # round robin through these time-series

                vals = [None] * self.num
                
                for i in range(self.num):

                    size = self.sizes[i]
                    shape = self.shapes[i]
                    actual_shape = shape
                    
                    # retreive appropriate number of values from buffer
                    vl = self.buff.get(size)
##                    print('\nSeries # = :',i,'Values:\n',vl)

                    # a complication is that the final vl may have
                    #   a smaller size
                    actual_size = len(vl)

                    if actual_size == 0:
                        vals[i] = []
                        self.rec.receive([])
                        break
                    elif actual_size == size: pass
                    else:
                        # the time dimension [0] is smaller in proportion
                        actual_shape[0] = int(shape[0] * actual_size / size)
                    
                    # convert to a numpy array object and reshape
                    vals[i] = np.array(vl).reshape(actual_shape,order='C')
                    
                # push list of array's to the time-series receptor
                self.rec.receive(vals)
           
        def run(self):
                # orchestrate stages of operation
                
                if not self.abort: self.discover_and_choose()
                if not self.abort: self.configuration()
                if not self.abort: self.stream()
                if not self.abort: self.retrieve()
                        
        def param_dict_to_var(self):
                # stores final set of parameters as variables for efficiency
                # for example, value of a parameter named 'frame' becomes
                #   variable self.frame
                
                p = self.param.final()
                for field in p.keys():
                        setattr(self,field,p[field])
               
'''
For the convenience of the different receptors, we implement some
base classes that capture common functionality.
Time-series receptor classes can inherit these classes at their option.
'''

class MultiplexedTimeSeries():
    '''
    Time-series receptor for any generator that time-division multiplexes
    time-series.
    Each time-value can be a numby array, and they must all have the same shape.
    This base class has no knowledge of how the time-series was generated,
    or whether the values are real or complex.
    '''
    
    # a set of time-division multiplexed time-series is received
    #   round-robin fashion
    
    # self.shapes = list of np.ndarray shapes, one for each time-series
    # shapes[i] = ndarray.shape for multiplexed time-series i

    def shapes(self,s):
        # store shapes, which is a list of numby shapes for the
        #   time-multiplexed time-series

        self.shapes = s

        # allocate list of numby arrays to capture whole signals
        self.whole = [np.array([])] * len(self.shapes)
        
    def accumulate(self,vals):
        # service provided at the option of the inherited class
        # accumulates stream of frames into whole time-series,
        #   thus abandoning the frame structure
        # inherited class may need to deal with frames directly
        #   (as in a feedback situation)
        #   in which case it doesn't need to call this method

        if len(vals) == 0: # we have reached end of time-series
            self.wrapup()
            return

        for i in range(len(self.shapes)):

            if self.whole[i].size == 0:
                self.whole[i] = vals[i]
            else:
                self.whole[i] = np.append(self.whole[i],vals[i])


class MultiplexedComplexTimeSeries(MultiplexedTimeSeries):
    '''
    Class provides some common facilities for time-division multiplexed
    time-series which have complex-values.
    '''

    def print(self,vals):
        # print out the real- and imag-parts of a time series
        # vals = numpy.ndarray with dtype = complex

            print(
                '\nTotal received time-series of length = ',
                  vals.size, ':'
                )
            print('\nReal-part\n', np.around(vals.real, 3))
            print('\nImag-part\n', np.around(vals.imag, 3))

    def plot(self,vals):
        # make a plot of the real- and imag-parts of a time-series
        # vals = numpy.ndarray with dtype = complex

            plt.plot(vals.real)
            plt.plot(vals.imag)
##            plt.axis([0, self.whole.size * T, -1, +1])
            plt.title('Complex exponential')
            plt.show()
            
if __name__ == '__main__':

    s = TimeSeriesClient()
    s.run()
