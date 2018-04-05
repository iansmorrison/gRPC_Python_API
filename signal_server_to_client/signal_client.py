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
import buffer as buff

class StreamingClient(gc.GenericClientStub):
    '''
    Retreives a generic complex-valued signal
    Particulars of WHAT signal is returned are left to an inherited class
    '''

    def __init__(self):
        
        super().__init__()

    #   !!! CONFIGURATION !!!

    def connect(self,b):
        # b = buffer where client will send gRPC output and
        #   input lists of values at the semantic layer
        self.buff = b

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

    def stream(self):
        # method is invoked in order to capture signal stream from gRPC channel
        
        s = self.message.Config(**{
                        'operation':'get',
                        'parameters':json.dumps('')
                        })
        
        self.r = self.channel.OneDimensionalSignal(s)
        # r is a generator (to conserve memory) and thus can only be iterated once

    def get(self):
        # get next value from r, convert to complex values,
        #   store in list, and return
        
        rnext = next(self.r,None)
        if rnext == None: return []
        size = len(rnext.sample)
        vals = [None] * size
        for i in range(size):
            vals[i] = complex(rnext.sample[i].real,rnext.sample[i].imag)
        return vals
