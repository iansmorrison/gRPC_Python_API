"""
The Python implementation of the ComplexSignal server
This version uses a both a repeated field (for efficiency)
  and streaming (for long responses) to return multiple complex samples
  
Programmer: David G Messerschmitt
5 Feb 2018
"""

from concurrent import futures
import time
import math
import grpc
import complex_signal_pb2
import complex_signal_pb2_grpc

# Configuration
_NUM_MESSAGES_PER_RESPONSE = 10 # Set this for efficiency
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_timeout = _ONE_DAY_IN_SECONDS # Elapsed time before giving up
_net_addr = 'localhost:50056' # Port to listen to for RPC requests

def samples_real(num,start_seq_num):
  # num = total number of samples to send back as repetition
  # start_seq_num = starting number in the sequence
  for n in range(num):
    yield float(start_seq_num + n +0.2)

def samples_imag(num,start_seq_num):
  for n in range(num):
    yield float(start_seq_num + n +0.7)
  
class ComplexSignal(complex_signal_pb2_grpc.ComplexSignalServicer):

  def Signal(self,request,context):
    # Total greetings
    _num = request.num_samples
    # Greetings per response
    _num_responses = math.floor(_num/_NUM_MESSAGES_PER_RESPONSE)
    # Greetings in the last response
    _num_left_over = _num % _NUM_MESSAGES_PER_RESPONSE
    # stream lists of greetings
    for n in range(_num_responses):
      # response single list of greetings
      yield complex_signal_pb2.Signal(
        real = samples_real(
          _NUM_GREETINGS_PER_RESPONSE,
          n * _NUM_GREETINGS_PER_RESPONSE
          ),
        imag = samples_imag(
          _NUM_GREETINGS_PER_RESPONSE,
          n * _NUM_GREETINGS_PER_RESPONSE)
          )
    # Last response with a list of greetings left over
    yield complex_signal_pb2.Signal(
        real = samples_real(
          _num_left_over,
          _num_responses * _NUM_GREETINGS_PER_RESPONSE
          ),
        imag = samples_imag(
          _NUM_GREETINGS_PER_RESPONSE,
          n * _NUM_GREETINGS_PER_RESPONSE
          )
          )

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  complex_signal_pb2_grpc.add_ComplexSignalServicer_to_server(
    ComplexSignal(),
    server
    )
  server.add_insecure_port(_net_addr)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
