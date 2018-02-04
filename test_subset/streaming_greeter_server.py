"""
The Python implementation of the GRPC helloworld.Greeter server
This version modified by David G Messerschmitt
27 Jan 2018
"""

from concurrent import futures
import time
import grpc
import hellostreamingworld_pb2
import hellostreamingworld_pb2_grpc

# Configuration
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_timeout = _ONE_DAY_IN_SECONDS # Elapsed time before giving up
_net_addr = 'localhost:50052' # Port to listen to for RPC requests

def compose_greeting(name,seq_num):
  # name = person to greet
  # seq_num = reveals to the user how many greetings have been sent
  return 'Response #{0}: Hello, {1}!'.format(seq_num,name)

class MultiGreeter(hellostreamingworld_pb2_grpc.MultiGreeterServicer):

  def SayHello(self,request,context):
    # Send multiple greetings, each with a sequence number
    # Calling HelloReply multiple times creates a stream of responses
    for n in range(request.num_greetings):
      yield hellostreamingworld_pb2.HelloReply(
        greeting = compose_greeting(request.name,n+1)
          )
      

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  hellostreamingworld_pb2_grpc.add_MultiGreeterServicer_to_server(MultiGreeter(),server)
  server.add_insecure_port(_net_addr)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()
