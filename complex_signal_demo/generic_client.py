"""
The Python implementation of a generic gRPC client stub
Programmer David G Messerschmitt
19 Feb 2018

    !!! IT SHOULD NOT BE NECESARY TO EDIT THIS FILE !!!
"""

import importlib
import grpc

from PROTO_DEFINITIONS import *

class GenericClientStub():
    '''

    Establish channel and satisfy rpc requests
    Class not specific to any protocol buffer definition, but encapsulates
        all the grpc mechanics and hides them from the user
    This class does not require modification if the .proto file is changed,
        as it automatically makes use of the PROTO_DEFINITIONS dictonaries to customize    
    '''

    def __init__(self):

        # import and generically rename gRPC code generatd by the .proto compiler
        # inherited class must provide method proto() which provides name of .proto file
        self.grpcMessage = importlib.import_module('{0}_pb2'.format(NAME_OF_PROTO_FILE))
        self.grpcServe = importlib.import_module('{0}_pb2_grpc'.format(NAME_OF_PROTO_FILE))
                                                 
        # inherited class must provide method service() which provides name of service
        self.grpcServeStub = getattr(self.grpcServe,'{0}Stub'.format(SERVICE_NAME))

        # establish a port where rpc requests can be received
        # inherited class much provide method net() which provides port information
        self.channel = grpc.insecure_channel(NET_CONNECTION)

        # instantiate a client stub listening to this channel
        self.stub = self.grpcServeStub(self.channel)

        super().__init__()
        


