"""
The Python implementation of a generic GRPC service stub
Progammer David G Messerschmitt
19 Feb 2018
"""

from concurrent import futures
import time
import importlib

from PROTO_DEFINITIONS import *

# gRPC engine
import grpc

# Import gRPC-compiled modules with generic renaming                                  
grpcServe = importlib.import_module('{0}_pb2_grpc'.format(NAME_OF_PROTO_FILE))
grpcServicer = getattr(grpcServe,'{0}Servicer'.format(SERVICE_NAME))
grpcAddServicer = getattr(grpcServe,'add_{0}Servicer_to_server'.format(SERVICE_NAME))

# Configuration
MAXIMUM_SERVICE_TIME_IN_MINUTES = 60

class GenericServer(grpcServicer):
  # initiate and run a server

  def __init__(self):

    # set False to force server termination at the next timeout opportunity
    self.going = True
    
    super().__init__()

  def run(self):

    # instantiate server
    s = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add server to pool
    grpcAddServicer(self,s)
    # open network port to server    
    s.add_insecure_port(NET_CONNECTION)

    # start server, stop when requested or following a timeout
    elapsed = 0 # elapsed time in minutes
    s.start()
    while self.going and elapsed < MAXIMUM_SERVICE_TIME_IN_MINUTES:
      time.sleep(60) # sleep for one minute
      elapsed += 1
    s.stop(0)


