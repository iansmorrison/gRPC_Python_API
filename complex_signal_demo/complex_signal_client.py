"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long-duration signals) to return multiple complex samples
Programmer: David G Messerschmitt
6 March 2018
"""

#   !!! IF PROTO FILE IS CHANGED, THIS FILE NEEDS TO BE EDITED TO ALIGN NAMES !!!


import generic_client as gc

class ComplexSignalClient(gc.GenericClientStub):
    '''
    Retreives a generic complex-valued signal
    Particulars of WHAT signal is returned are left to an inherited class
    '''

    def __init__(self):

        super().__init__()
        
        # methods for send messages
        # there must be one for each rpc channel
        #self.sendTest = getattr(self.grpcMessage,'Go')
        self.sendConfig = getattr(self.grpcMessage,'Param')
        self.sendRequest = getattr(self.grpcMessage,'Request')

        # methods for response messages
        # there must be one for each rpc channel
        #self.stubTest = getattr(self.stub,'Test')
        self.stubConfig = getattr(self.stub,'SetConfig')
        self.stubSignal = getattr(self.stub,'GetSignal')       

    def get(self):
        # method is invoked in order to run the client
      
        # configuration of server
        # inherited class must implement paramters(), which returns a dictionary
        #   with set of parameters aligned with .proto file definitions
        p = self.parameters()
        print('Param message sent: ',p)
        s = self.sendConfig(**p)
        r = self.stubConfig(s)
        print('Confirm response received: ',r)
        
        # request and process signal
        #s = self.sendRequest(**{'numSamples':105})
        s = self.grpcMessage.Request(**{'numSamples':105})
        #r = self.stubSignal(s)
        r = self.stub.GetSignal(s)
        # r is a generator (to save memory) and thus can only be accessed once
        # merge streamed responses into two lists stored in memory
        reals = []; imags = []
        for sc in r:
            reals.extend(sc.real); imags.extend(sc.imag)
        return [reals,imags]
