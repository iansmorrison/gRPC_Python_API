"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long-duration signals) to return multiple complex samples

Programmer: David G Messerschmitt
18 March 2018
"""

# !!! IF PROTO FILE IS CHANGED, THIS FILE MUST BE EDITED TO ALIGN NAMES !!!

import json
import inspect
from pprint import pprint
import generic_client as gc

class ComplexSignalClient(gc.GenericClientStub):
    '''
    Retreives a generic complex-valued signal
    Particulars of WHAT signal is returned are left to an inherited class
    '''

    def __init__(self):
        super().__init__()

        #self.samples = 205 # number of samples to generate and stream

    #   !!! CONFIGURATION !!!

    def metadata_message_and_response(self,op,param):
        # inherited class can call this method to send an
        #   operation to the server
        #       op = string specifying desired operation
        #       param = dictonary containing parameters of that op
        # returns server's response

        # JSON string representation of param is actually sent
        p = {'operation':op,'parameters':json.dumps(param)}
        s = self.message.Config(**p)
        r = self.channel.MetaDataCoordination(s) # returns response message
        return [json.loads(r.response),r.alert]

    #   !!! RUN  !!!
 
    def get(self):
        # method is invoked in order to capture a signal
        # we assume server has already been configured
        
        s = self.message.Config(**{
                        'operation':'get',
                        'parameters':json.dumps('')
                        })
        r = self.channel.OneDimensionalSignal(s) # r = list of signal samples
        
        # r is a generator (to conserve memory) and thus can only be accessed once
        # lets use that one chance to merge streamed responses into two lists stored in memory


        for sc in r:
            num_samples = len(sc.sample)
            samples = [None] * num_samples # number of samples in one repeated field
            for i in range(num_samples):
                # convert to a complex data type and store in a list
                samples[i] = complex(sc.sample[i].real,sc.sample[i].imag)
            yield samples

