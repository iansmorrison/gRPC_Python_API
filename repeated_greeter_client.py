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
_number = 25 # number of streaming responses
_net_addr = 'localhost:50054'

def invoke_service(user_name,num):
    return hellorepeatedworld_pb2.HelloRequest(
        name = user_name,
        num_greetings = num
        )
    
def run():
  channel = grpc.insecure_channel(_net_addr)
  stub = hellorepeatedworld_pb2_grpc.MultiGreeterStub(channel)
  responses = stub.SayHello(invoke_service(_user_name,_number))
  for response in responses:
      for greeting in response.greeting:
          print(greeting)

if __name__ == '__main__':
  run()
