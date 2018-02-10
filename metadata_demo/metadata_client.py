"""
The Python implementation of the GRPC helloworld.Greeter client.
This version modified by David G Messerschmitt
27 Jan 2018
"""

import grpc
import metadata_demo_pb2
import metadata_demo_pb2_grpc

# Configuration
_net_connection = 'localhost:50055'

def query(message):
    return metadata_demo_pb2.QueryRequest(question = message)

def service(message):
    return metadata_demo_pb2.ServiceRequest(request = message)

def report(message):
    return metadata_demo_pb2.ClientStatus(report = message)
    
def run():
    _channel = grpc.insecure_channel(_net_connection)
    _stub = metadata_demo_pb2_grpc.ServiceControlStub(_channel)
    _r1 = _stub.Query(query('Query: What can you do?'))
    print('Client received: ' + _r1.answer)
    _r2 = _stub.Service(service('Service: Do B please'))
    print('Client received: ' + _r2.report)
    _r3 = _stub.WrapUp(report('WrapUp: B completed as I was expecting'))
    print('Client received: ' + _r3.report)
    

if __name__ == '__main__':
  run()
