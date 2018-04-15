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

        # import and generically rename gRPC code generated by the .proto compiler
        self.message = importlib.import_module('{0}_pb2'.format(PROTO_FILE))
        self.serve = importlib.import_module('{0}_pb2_grpc'.format(PROTO_FILE))
                                                 
        # a stub which allows client to interact with gRPC
        s = getattr(self.serve,'{0}Stub'.format(SERVICE))

        # establish a port where rpc requests can be received
        c = grpc.insecure_channel(NET_CONNECTION)

        # instantiate a client stub listening to this channel
        self.channel = s(c)



