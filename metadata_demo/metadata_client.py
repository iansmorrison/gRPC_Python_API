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

def query(message):
    return grpcMessage.QueryRequest(question = message)

def service(message):
    return grpcMessage.ServiceRequest(request = message)

def report(message):
    return grpcMessage.ClientStatus(report = message)
    
def run():
    _channel = grpc.insecure_channel(_net_connection)
    _stub = grpcServe.ServiceControlStub(_channel)
    _r1 = _stub.Query(query('Query: What can you do?'))
    print('Client received: ' + _r1.answer)
    _r2 = _stub.Service(service('Service: Do B please'))
    print('Client received: ' + _r2.report)
    _r3 = _stub.WrapUp(report('WrapUp: B completed as I was expecting'))
    print('Client received: ' + _r3.report)
    

if __name__ == '__main__':
  run()
