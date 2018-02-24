"""
The Python implementation of a generic gRPC client stub
Programmer David G Messerschmitt
19 Feb 2018
"""

# ENCAPSULATION OF RELEVANT .proto NAME DEFINTIONS
# This file contains definitions of SERVICE_NAME,
# RPC_AND_MESSAGE_NAMES and MESSAGE_FIELDS
# This file is shared between client and server
from PROTO_DEFINITIONS import *

# gRPC engine
import grpc

# files compiled from the .proto file by gRPC
cmd = 'import {0}_pb2 as grpcMessage'.format(NAME_OF_PROTO_FILE)
# Example:
# cmd = 'import metadata_demo_pb2 as grpcMessage'

exec(cmd)
cmd = 'import {0}_pb2_grpc as grpcServe'.format(NAME_OF_PROTO_FILE)
# Example:
# cnd = 'import metadata_demo_pb2_grpc as grpcServe'
exec(cmd)

class GenericClientStub():
    '''

    Establish channel and satisfy rpc requests
    Class not specific to any protocol buffer definition, but encapsulates
        all the grpc mechanics and hides them from the user
    This class does not require modification if the .proto file is changed

    !!! IT SHOULD NOT BE NECESARY TO EDIT THIS FILE !!!
    
    '''

    def __init__(self):

        # create a working copy of MESSAGE_FIELDS whose content can be dynamically changed
        self.messageFields = MESSAGE_FIELDS.copy()

        # establish a port where rpc requests can be received
        self.channel = grpc.insecure_channel(NET_CONNECTION)

        # instantiate a server instance listening to this channel
        exp = 'grpcServe.{0}Stub(self.channel)'.format(SERVICE_NAME)
        # Example:
        # exp = 'grpcServe.ServiceControlStub(self.channel)'
        self.stub = eval(exp)
        
    def rpcSend(self,rpc_name):
        # request to invoke rpc requires name of rcp channel
        # rpc_name = name of rpc channel as a string

        # look up name of client and server messages corresponding to this rcp channel
        [c_name,s_name] = RPC_AND_MESSAGE_NAMES[rpc_name]
        # Example:
        # c_name = 'QueryRequest' and s_name = 'QueryReply'

        # formulate gRPC command in two stages
        exp = 'grpcMessage.{0}(**self.messageFields["{0}"])'.format(c_name)
        # Example:
        # cmd = 'grpcMessage.QueryRequest(**self.messageFields["QueryRequest"])'

        # execute message transmission; note that this is a blocking transaction
        exp = 'self.stub.{0}({1})'.format(rpc_name,exp)
        # Example:
        # cmd = 'self.stub.Query(cmd)'
        r = eval(exp)
        
        # populate the dictionary message fields based on response r
        for key in self.messageFields[s_name].keys():
            self.messageFields[s_name][key] = eval('r.{0}'.format(key))

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
    '''

    def __init__(self):

        # create a copy of MESSAGE_FIELDS so its content can be dynamically changed
        # any desired default values can be introduced here in place of None
        # any message fields not defaulted or set here will default to gRPC-defined values
        self.messageFields = MESSAGE_FIELDS.copy()

        super().__init__()

    def run(self):
        '''
        This method is invoked in order to run the client
        Its purpose is to generate rpc messages, interpret the responses from
            the server, and generate new rpc messages
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
