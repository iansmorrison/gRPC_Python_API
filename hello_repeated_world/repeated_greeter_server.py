"""
The Python implementation of the GRPC helloworld.Greeter server
This version uses a repeated field to return multiple greetings
This version modified by David G Messerschmitt
27 Jan 2018
"""

from concurrent import futures
import time
import grpc
import hellorepeatedworld_pb2
import hellorepeatedworld_pb2_grpc

# Configuration
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_timeout = _ONE_DAY_IN_SECONDS # Elapsed time before giving up
_net_addr = 'localhost:50053' # Port to listen to for RPC requests

def compose_greeting(name,seq_num):
  # name = person to greet
  # seq_num = reveals to the user how many greetings have been sent
  return 'Response #{0}: Hello, {1}!'.format(seq_num,name)

def multiple_greetings(name,num):
  # num = number of greetings to send back as repetition
  for n in range(num):
    yield compose_greeting(name,n+1)
    
  
class MultiGreeter(hellorepeatedworld_pb2_grpc.MultiGreeterServicer):

  def SayHello(self,request,context):
    # Send multiple greetings, each with a sequence number
    #   as a repeated field, manifested by a list object
    return hellorepeatedworld_pb2.HelloReply(
        greeting = multiple_greetings(request.name,request.num_greetings)
          )

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  hellorepeatedworld_pb2_grpc.add_MultiGreeterServicer_to_server(MultiGreeter(),server)
  server.add_insecure_port(_net_addr)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
