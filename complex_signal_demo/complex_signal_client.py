"""
The Python implementation of the ComplexSignalClient
This version uses a both a repeated field (for efficiency)
  and streaming (for long-duration signals) to return multiple complex samples
Programmer: David G Messerschmitt
6 March 2018
"""

# !!! IF PROTO FILE IS CHANGED, THIS FILE NEEDS TO BE EDITED TO ALIGN NAMES !!!

import generic_client as gc

class ComplexSignalClient(gc.GenericClientStub):
    '''
    Retreives a generic complex-valued signal
    Particulars of WHAT signal is returned are left to an inherited class
    '''

    def __init__(self):
        super().__init__()

        self.samples = 205 # number of samples to generate and stream

    #   !!! DISCOVERY !!!

    def ask_question(self,p):
        # inherited class can call this method to query the server

        s = self.message.Question(**p)
        r = self.channel.Query(s) # returns response message

        print('\nQuery response:')
        # response is a generator (type of iterator)
        for name in r.signal_name:
            print(name)
        
    #   !!! CONFIGURATION !!!

    def set_parameters(self,p):
        # inherited class can call this method to set parameters of the server

        s = self.message.Param(**p)
        r = self.channel.SetConfig(s) # returns response message

        print('\nSetConfig response:')
        if not r.okay:  # server not satisfied with parameters
            print('Warning! ',r.narrative)
        else:
            print('Configuration available:',r.narrative)

        #   !!! RUN  !!!
 
    def get(self):
        # method is invoked in order to capture a signal
        
        s = self.message.Request(**{'numSamples':self.samples})
        r = self.channel.GetSignal(s) # server response is a signal
        
        # r is a generator (to save memory) and thus can only be accessed once
        # use that one chance to merge streamed responses into two lists stored in memory
        reals = []; imags = []
        for sc in r:
            reals.extend(sc.real); imags.extend(sc.imag)
        return [reals,imags]
