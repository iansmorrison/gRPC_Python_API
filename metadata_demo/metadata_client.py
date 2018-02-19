"""
The Python implementation of the GRPC helloworld.Greeter client.
This version modified by David G Messerschmitt
27 Jan 2018
"""

import grpc
import metadata_demo_pb2 as grpcMessage
import metadata_demo_pb2_grpc as grpcServe

# Configuration
_net_connection = 'localhost:50055'

# messages are represented by a dictionary on both send and receive
# initialize that dictionary
_serviceName = 'ServiceControl'
_rcpNames = ['Query','Service','WrapUp']
_messageFields =  {
        'QueryRequest':     {'question' : None},
        'ServiceRequest' :  {'request' : None},
        'ClientStatus' :    {'report' : None},
        'QueryReply':       {'answer' : None},
        'ServiceStatus':    {'report' : None},
        'WrapUpReport':     {'report' : None}
        }
# note to future: would be nice to generate
#   _meta skeleton automatically from .proto file

class GenericClientStub():
    '''
    Establish channel and satisfy rpc requests
    Class not specific to any protocol buffer definition, but encapsulates
        all the grpc mechanics
    Change .proto file and this class does not require modification
    '''

    def __init__(self):
        self.channel = grpc.insecure_channel(_net_connection)
        cmd = 'grpcServe.{0}Stub(self.channel)'.format(_serviceName)
        self.stub = eval(cmd)
        
    def rpcRequest(self,rpc_name,message_name):
        # request to invoke rpc requires name of rcp channel and message name
        # rpc_name = string with name of service
        # message_name = string identifying type of message
        cmd = 'grpcMessage.{0}(**_messageFields["{0}"])'.format(message_name)
        # Example:
        # cmd = 'grpcMessage.QueryRequest(**_messageFields["QueryRequest"])'
        cmd = 'self.stub.{0}({1})'.format(rpc_name,cmd)
        # Example:
        # cmd = 'self.stub.Query(cmd)'
        return eval(cmd)

class MetadataClient(GenericClientStub):

    def __init__(self):
        super().__init__()

    def run(self):

        # example query of the server
        _messageFields['QueryRequest']['question'] = 'What can you do?'
        r = self.rpcRequest('Query','QueryRequest')
        _messageFields['QueryReply']['answer'] = r.answer

        # example service request
        _messageFields['ServiceRequest']['request'] = 'Do B please'
        r = self.rpcRequest('Service','ServiceRequest')
        _messageFields['ServiceStatus']['report'] = r.report

        # example wrapup request
        _messageFields['ClientStatus']['report'] = 'B completed as I was expecting'
        r = self.rpcRequest('WrapUp','ClientStatus')
        _messageFields['WrapUpReport']['report'] = r.report

        # print messages back from server
        print(_messageFields['QueryReply'])
        print(_messageFields['ServiceStatus'])
        print(_messageFields['WrapUpReport'])
    

if __name__ == '__main__':
  MetadataClient().run()
