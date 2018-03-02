
'''
The client implementation of a metadata demo
Programmer David G Messerschmitt
22 Feb 2018
'''

import generic_client

class MetadataClient(generic_client.GenericClientStub):
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

        # This would be the place to define any desired default values
        #   for messageField[][]
        # any message fields not defaulted or set here will default to gRPC-defined values

        # this will instantiate a client stub and connection to server
        super().__init__()

    def run(self):
        '''
        This method is invoked in order to run the client, which interacts with the rpc client stub
        Its purpose is to generate rpc messages, interpret the responses from
            the server, and generate new rpc messages
            
        This is an implementation of a metadata demo
        '''

        # the natural ordering of rpc requests is Query, Service, WrapUP
        
        # first send a Query
        self.messageFields['QueryRequest']['question'] = 'What services do you offer?'
        self.rpcSend('Query')

        # next invoke a Service
        self.messageFields['ServiceRequest']['request'] = 'Provide B please'
        self.rpcSend('Service')

        # finally WrapUP
        self.messageFields['ClientStatus']['report'] = 'Service B completed as I was expecting'
        self.rpcSend('WrapUp')


if __name__ == '__main__':
 c = MetadataClient()
 c.run()
 c.report() # view final state of messageFields
