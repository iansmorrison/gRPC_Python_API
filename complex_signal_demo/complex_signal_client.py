"""
The Python implementation of the ComplexSignal client
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
  
Programmer: David G Messerschmitt
5 Feb 2018
"""

import grpc
import complex_signal_pb2
import complex_signal_pb2_grpc

# Configuration
_number_samples = 25 # number of samples
_net_addr = 'localhost:50056'

def invoke_service(num):
    return complex_signal_pb2.SignalRequest(
        num_samples = num
        )
    
def run():
  channel = grpc.insecure_channel(_net_addr)
  stub = complex_signal_pb2_grpc.ComplexSignalStub(channel)
  responses = stub.AccessSignal(invoke_service(_number_samples))
  for response in responses:
    print(response.real)
    print(response.imag)

if __name__ == '__main__':
  run()
