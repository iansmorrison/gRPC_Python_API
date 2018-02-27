"""
The Python implementation of a generic gRPC client stub
Programmer David G Messerschmitt
19 Feb 2018
"""

import importlib

# ENCAPSULATION OF RELEVANT .proto NAME DEFINTIONS
# This file contains definitions of SERVICE_NAME, RPC_AND_MESSAGE_NAMES and MESSAGE_FIELDS
# This file is shared between client and server
from PROTO_DEFINITIONS import *

# gRPC engine
import grpc

# Import gRPC-compiled modules, removing the .proto-specific naming
grpcMessage = importlib.import_module('{0}_pb2'.format(NAME_OF_PROTO_FILE),'SUB')
grpcServe = importlib.import_module('{0}_pb2_grpc'.format(NAME_OF_PROTO_FILE),'SUB')

# Do the same for needed functions within the modules
grpcServeStub = getattr(grpcServe,'{0}Stub'.format(SERVICE_NAME))

class GenericClientStub():
    '''

    Establish channel and satisfy rpc requests
    Class not specific to any protocol buffer definition, but encapsulates
        all the grpc mechanics and hides them from the user
    This class does not require modification if the .proto file is changed,
        as it automatically makes use of the PROTO_DEFINITIONS dictonaries to customize

    !!! IT SHOULD NOT BE NECESARY TO EDIT THIS FILE !!!
    
    '''

    def __init__(self):

        # create a working copy of MESSAGE_FIELDS whose content can be dynamically changed
        self.messageFields = MESSAGE_FIELDS.copy()

        # establish a port where rpc requests can be received
        self.channel = grpc.insecure_channel(NET_CONNECTION)

        # instantiate a client stub listening to this channel
        self.stub = grpcServeStub(self.channel)
        
    def rpcSend(self,rpc_name):
        # request to invoke rpc requires name of rcp channel
        # rpc_name = name of rpc channel as a string

        # look up name of client and server messages corresponding to this rcp channel
        [c_name,s_name] = RPC_AND_MESSAGE_NAMES[rpc_name]
        # Example:
        # c_name = 'QueryRequest' and s_name = 'QueryReply'

        # formulate gRPC command in two stages
        sendMessage = getattr(grpcMessage,c_name)(**self.messageFields[c_name])
        # execute message transmission; note that this is a blocking transaction
        r = getattr(self.stub,rpc_name)(sendMessage)
       
        # populate the dictionary message fields based on response r from server
        for key in self.messageFields[s_name].keys():
            self.messageFields[s_name][key] = getattr(r,key)

        # we are finished; the client can now retreive the received message
        #   from messageFields[][]

        # at this point it would make sense to log this send and response
        #   in a format similar to report()

    def report(self):
        print('\n!!!!! Report of the gRPC sent and response messages !!!!')
        for rpc_name in RPC_AND_MESSAGE_NAMES.keys():
             print('\nRPC name: ' + rpc_name)
             for message_name in RPC_AND_MESSAGE_NAMES[rpc_name]:
                 print('\tMessage name: ' + message_name)
                 for field_name in self.messageFields[message_name].keys():
                     field_value = self.messageFields[message_name][field_name]
                     print('\t\t' + field_name + ' = ' + field_value)

'''
The client implementation of a metadata demo
Programmer David G Messerschmitt
22 Feb 2018
'''

class MetadataClient(GenericClientStub):
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
    Note that this class may implement the communication portion of an application, deferring the
        remainder of the application logic to an inherited class.

            !!! THIS IMPLEMENTATION IS SPECIFIC TO THE .proto DEFINITIONS !!!

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
