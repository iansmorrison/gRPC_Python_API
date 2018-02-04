"""
The Python implementation of the GRPC helloworld.MultiGreeter client
Programmed by David G Messerschmitt
27 Jan 2018
"""

import grpc
import hellorepeatedworld_pb2
import hellorepeatedworld_pb2_grpc

# Configuration
_user_name = 'Dave'
_number = 20 # number of streaming responses
_net_addr = 'localhost:50053'

def invoke_service(user_name,num):
    return hellorepeatedworld_pb2.HelloRequest(
        name = user_name,
        num_greetings = num
        )
    
def run():
  channel = grpc.insecure_channel(_net_addr)
  stub = hellorepeatedworld_pb2_grpc.MultiGreeterStub(channel)
  response = stub.SayHello(invoke_service(_user_name,_number))
  for greet in response.greeting:
      print(greet)

if __name__ == '__main__':
  run()
