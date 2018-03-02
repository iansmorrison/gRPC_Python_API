"""
The Python implementation of the ComplexSignal client
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
Programmer: David G Messerschmitt
2 March 2018
"""


import generic_client as gs

print('RPC and message names:')
print(gs.RPC_AND_MESSAGE_NAMES)
print('Message names and fields:')
print(gs.MESSAGE_FIELDS)
print(gs.RPC_AND_MESSAGE_NAMES['GetSignal'])

class ComplexSignalClient(gs.GenericClientStub):
    '''
    This is the user-programmed class specific to a particular .proto file.
    All message fields are stored in a dictionary self.messageFields[][].
    Interactions with gRPC is thru:
        * To send a message, first set the desired fields in self.messageFields[][].
        * Then call self.rpcSend[] to initiate the transmission of that message. This will block
            until a response from the client is received and stored back in self.messageField[][].
        * Following completion of rpcSend, the resulting response can be read from self.messageFields[][].
    Generally this client will implement a protocol consisting of a sequence of self.rpcSend[] transmssions,
        reading responses, and acting accordingly.

    The available calls provided by GenericClientStub are:
        self.messageFields[message_name][field_name] indexes the message dictonary, where
            message_name = the name of an rpc channel (like 'QueryRequest')
            field_name = the name of a field within the message (like "question")
        self.rpcSend(rpc_channel_name) initiates a transmission, where
            rpc_channel_name = the name of an rpc channel (like 'Query')
        self.report() = gives a printed report of the entire message dictionary, good for debuggng.
    Note that this class may implement the communication portion of a client, deferring the
        remainder of the application logic to an inherited class.
    '''

    def __init__(self):

        # instantiate a client stub and connection to server
        # also initialize messageFields
        super().__init__()
        
        # Defaults
        self.messageFields['Request']['phaseIncrement'] = 0.25
        self.messageFields['Request']['numSamples'] = 10
        

    def run(self):
        '''
        This method is invoked in order to run the client, which interacts with the rpc client stub
        Its purpose is to generate rpc messages, interpret the responses from
            the server, and generate new rpc messages
        This is an implementation of a complex signal demo
        '''
        
        # send a Request
        # rely on defaults for now
        self.rpcSend('GetSignal')
        sample = self.messageFields['Signal']['real']
        print(sample)


if __name__ == '__main__':
 c = ComplexSignalClient()
 c.run()
 c.report() # view final state of messageFields
