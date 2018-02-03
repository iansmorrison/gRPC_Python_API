"""
The Python implementation of the GRPC helloworld.Greeter server
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple greetings
This version modified by David G Messerschmitt
3 Feb 2018
"""

from concurrent import futures
import time
import math
import grpc
import hellorepeatedworld_pb2
import hellorepeatedworld_pb2_grpc

# Configuration
_NUM_GREETINGS_PER_RESPONSE = 10 # Set this for efficiency
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_timeout = _ONE_DAY_IN_SECONDS # Elapsed time before giving up
_net_addr = 'localhost:50054' # Port to listen to for RPC requests

def compose_greeting(name,seq_num):
  # name = person to greet
  # seq_num = reveals to the user how many greetings have been sent
  return 'Response #{0}: Hello, {1}!'.format(seq_num,name)

def multiple_greetings(name,num,start_seq_num):
  # generate a list of greetings to be returned as a repeated greeting
  # num = total number of greetings to send back as repetition
  # start_seq_num = starting number in the sequence
  for n in range(num):
    yield compose_greeting(name,start_seq_num+n+1)
    
  
class MultiGreeter(hellorepeatedworld_pb2_grpc.MultiGreeterServicer):

  def SayHello(self,request,context):
    _name = request.name
    # Total greetings
    _num = request.num_greetings
    # Greetings per response
    _num_responses = math.floor(_num/_NUM_GREETINGS_PER_RESPONSE)
    # Greetings in the last response
    _num_left_over = _num % _NUM_GREETINGS_PER_RESPONSE
    # stream lists of greetings
    for n in range(_num_responses):
      # response single list of greetings
      yield hellorepeatedworld_pb2.HelloReply(
        greeting = multiple_greetings(
          _name,
          _NUM_GREETINGS_PER_RESPONSE,
          n * _NUM_GREETINGS_PER_RESPONSE
          )
          )
    # Last response with a list of greetings left over
    yield hellorepeatedworld_pb2.HelloReply(
        greeting = multiple_greetings(
          _name,
          _num_left_over,
          _num_responses * _NUM_GREETINGS_PER_RESPONSE
          )
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
