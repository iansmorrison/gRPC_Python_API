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
_meta =  {
        'QueryRequest': {'question':''},
        'ServiceRequest' : {'request':''},
        'ClientStatus' : {'report':''},
        'QueryReply': {'answer':''},
        'ServiceStatus': {'report':''},
        'WrapUpReport': {'report':''}
        }
# note to future: would be nice to generate
#   _meta skeleton automatically from .proto file

def _message(message_type):
    # message_type = string identifying type of message
    return eval(
        "grpcMessage." + message_type +
        "(**_meta[" + "message_type" + "])"
        )
    
def run():
    _channel = grpc.insecure_channel(_net_connection)
    _stub = grpcServe.ServiceControlStub(_channel)

    # example query of the server
    _meta['QueryRequest']['question'] = 'What can you do?'
    _r1 = _stub.Query(_message('QueryRequest'))
    _meta['QueryReply']['answer'] = _r1.answer

    # example service request
    _meta['ServiceRequest']['request'] = 'Do B please'
    _r2 = _stub.Service(_message('ServiceRequest'))
    _meta['ServiceStatus']['report'] = _r2.report

    # example wrapup request
    _meta['ClientStatus']['report'] = 'B completed as I was expecting'
    _r3 = _stub.WrapUp(_message('ClientStatus'))
    _meta['WrapUpReport']['report'] = _r3.report

    # print messages back from server
    print(_meta['QueryReply'])
    print(_meta['ServiceStatus'])
    print(_meta['WrapUpReport'])
    

if __name__ == '__main__':
  run()
