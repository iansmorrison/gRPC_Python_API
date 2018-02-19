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

# metadata is represented by a dictionary on both send and receive
# initialize metadata dictionary
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

def _message(message_name):
    # message_name = string identifying type of message
    cmd='grpcMessage.{0}(**_messageFields["{0}"])'.format(message_name)
    print(cmd)
    return eval(cmd)

def _grpcRequest(rpc_name,message_name):
    # rpc_name = string with name of service
    # message_name = string identifying type of message
    cmd = 'grpcMessage.{0}(**_messageFields["{0}"])'.format(message_name)
    cmd = '_stub.{0}({1})'.format(rpc_name,cmd)
    print(cmd)
    return eval(cmd)

  
def run():
    _channel = grpc.insecure_channel(_net_connection)
    cmd = 'grpcServe.{0}Stub(_channel)'.format(_serviceName)
    _stub = eval(cmd)

    # example query of the server
    _messageFields['QueryRequest']['question'] = 'What can you do?'
    _r1 = _stub.Query(_message('QueryRequest'))
    #_r1 = _grpcRequest('Query','QueryRequest')
    _messageFields['QueryReply']['answer'] = _r1.answer

    # example service request
    _messageFields['ServiceRequest']['request'] = 'Do B please'
    _r2 = _stub.Service(_message('ServiceRequest'))
    _messageFields['ServiceStatus']['report'] = _r2.report

    # example wrapup request
    _messageFields['ClientStatus']['report'] = 'B completed as I was expecting'
    _r3 = _stub.WrapUp(_message('ClientStatus'))
    _messageFields['WrapUpReport']['report'] = _r3.report

    # print messages back from server
    print(_messageFields['QueryReply'])
    print(_messageFields['ServiceStatus'])
    print(_messageFields['WrapUpReport'])
    

if __name__ == '__main__':
  run()
