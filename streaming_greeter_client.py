"""
The Python implementation of the GRPC helloworld.MultiGreeter client
Programmed by David G Messerschmitt
27 Jan 2018
"""

import grpc
import hellostreamingworld_pb2
import hellostreamingworld_pb2_grpc

# Configuration
_user_name = 'Dave'
_number = 20 # number of streaming responses
_net_addr = 'localhost:50052'

def invoke(user_name,number):
    return hellostreamingworld_pb2.HelloRequest(
        name=user_name,
        num_greetings=number
        )
    
def run():
  channel = grpc.insecure_channel(_net_addr)
  stub = hellostreamingworld_pb2_grpc.MultiGreeterStub(channel)
  responses = stub.SayHello(
      invoke(_user_name,_number)
      )
  for response in responses:
      print(response.greeting)

if __name__ == '__main__':
  run()
