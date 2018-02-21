"""
The Python implementation of a generic gRPC client stub
Programmer David G Messerschmitt
19 Feb 2018
"""

import grpc
import metadata_demo_pb2 as grpcMessage
import metadata_demo_pb2_grpc as grpcServe

class GenericClientStub():
    '''
    Establish channel and satisfy rpc requests
    Class not specific to any protocol buffer definition, but encapsulates
        all the grpc mechanics and hides them from the user
    This class does not require modification if the .proto file is changed
    '''

    def __init__(self):
        self.channel = grpc.insecure_channel(_NET_CONNECTION)
        cmd = 'grpcServe.{0}Stub(self.channel)'.format(self.serviceName)
        self.stub = eval(cmd)
        
    def rpcRequest(self,rpc_name):
        # request to invoke rpc requires name of rcp channel
        # rpc_name = string with name of service

        # look up name of client message
        client_message_name = self.rcpAndMessageNames[rpc_name][0]
        # Example:
        # self.client_message_name = 'QueryRequest'

        # formulate gRPC command in two stages
        cmd = 'grpcMessage.{0}(**self.messageFields["{0}"])'.format(client_message_name)
        # Example:
        # cmd = 'grpcMessage.QueryRequest(**_messageFields["QueryRequest"])'
        
        cmd = 'self.stub.{0}({1})'.format(rpc_name,cmd)
        # Example:
        # cmd = 'self.stub.Query(cmd)'

        # execute message transmission
        r = eval(cmd)
    
        # look up name of server response message
        server_message_name = self.rcpAndMessageNames[rpc_name][1]
        # Example:
        # server_message_name = 'QueryReply'
        
        # populate the dictionary message fields based on response r
        server_message_keys = self.messageFields[server_message_name]
        for key in server_message_keys:
            self.messageFields[server_message_name][key] = eval('r.{0}'.format(key))

    def report(self):
        print('\n!!!!! Report of the gRPC sent and response messages !!!!')
        for rpc_name in self.rcpAndMessageNames.keys():
             print('\nRPC name: ' + rpc_name)
             for message_name in self.rcpAndMessageNames[rpc_name]:
                 print('\tMessage name: ' + message_name)
                 for field_name in self.messageFields[message_name].keys():
                     field_value = self.messageFields[message_name][field_name]
                     print('\t\t' + field_name + ' = ' + field_value)

# Configuration
_NET_CONNECTION = 'localhost:50055'

class MetadataClient(GenericClientStub):
    '''
    This is the user-programmed class specific to a particular .proto file
    All message fields are stored in a dictionary messageFields
    Interactions with gRPC is thru setting and reading values in this dictionary
        and calling methods of super() = GenericClientStub()
    '''

    def __init__(self):

        # drawn from .proto file
        self.serviceName = 'ServiceControl'

        # dictionaries of rpc and message names must align with .proto file
        self.rcpAndMessageNames = {
                                    'Query' :      ['QueryRequest',    'QueryReply'    ],
                                    'Service' :    ['ServiceRequest',  'ServiceStatus' ],
                                    'WrapUp':      ['ClientStatus',    'WrapUpReport'  ]
                                  }

        # any desired default values can be introduced here in place of None
        # any message fields not defaulted or set here will default to gRPC-defined values
        self.messageFields =    {
                                'QueryRequest':     {'question' : None  },
                                'ServiceRequest' :  {'request'  : None  },
                                'ClientStatus' :    {'report'   : None  },
                                'QueryReply':       {'answer'   : None  },
                                'ServiceStatus':    {'report'   : None  },
                                'WrapUpReport':     {'report'   : None  }
                                }

        super().__init__()

    def run(self):
        # the natural ordering of rpc requests is Query, Service, WrapUP
        
        # first a Query
        self.messageFields['QueryRequest']['question'] = 'What services do you offer?'
        self.rpcRequest('Query')

        # next Service
        self.messageFields['ServiceRequest']['request'] = 'Provide B please'
        self.rpcRequest('Service')

        # finally WrapUP
        self.messageFields['ClientStatus']['report'] = 'Service B completed as I was expecting'
        self.rpcRequest('WrapUp')

    

if __name__ == '__main__':
 c = MetadataClient()
 c.run()
 c.report()
