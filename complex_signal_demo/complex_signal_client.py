"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long-duration signals) to return multiple complex samples
Programmer: David G Messerschmitt
2 March 2018

    !!! IT SHOULD NOT BE NECESSARY TO EDIT THIS FILE !!!
"""

import generic_client as gc

class ComplexSignalClient(gc.GenericClientStub):
    '''
    Retreives a generic complex-valued signal
    Particulars of WHAT signal is retreived are left to an inherited class
    '''

    def __init__(self):
        super().__init__()       

    def get(self):
        '''
        This method is invoked in order to run the client, which interacts with the rpc client stub
        Its purpose is to generate rpc messages, interpret the responses from
            the server, and generate new rpc messages
        This is an implementation of a complex signal demo
        '''

        # send request for a complex signal
        
        # inherited class must implement request(), which returns the name
        #   of the request message aligned with the .proto file definition
        self.sendMessage = getattr(self.grpcMessage,self.request())
        
        # inherited class must implement paramters(), which returns a dictionary
        #   with set of parameters aligned with .proto file definitions
        send = self.sendMessage(**self.parameters())
        
        # inherited class must implement rpc(), which returns the name
        #   of the rpc channel aligned with the .proto file definition
        stub = getattr(self.stub,self.rpc())

        # access the complex signal in response by invoking the client stub
        r = stub(send)
        # r is a generator (to save memory) and thus can only be accessed once
        
        # merge streamed responses into two lists stored in memory
        reals = []; imags = []
        for sc in r:
            reals.extend(sc.real); imags.extend(sc.imag)

        return [reals,imags]
