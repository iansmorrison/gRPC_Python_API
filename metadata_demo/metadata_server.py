"""
The Python implementation of the GRPC helloworld.Greeter client.
This version modified by David G Messerschmitt
27 Jan 2018
"""

from concurrent import futures
import time
import grpc
import metadata_demo_pb2 as grpcMessage
import metadata_demo_pb2_grpc as grpcServe

# Configuration
_MAXIMUM_SERVICE_TIME_IN_MINUTES = 15
_net_connection = 'localhost:50055'


class ServiceControl(grpcServe.ServiceControlServicer):

  def __init__(self):
    super().__init__()
    self.going = True

  def Query(self, request, context):
    print('Server received: ' + request.question)
    return grpcMessage.QueryReply(answer = 'QueryReply: ' + 'A or B or C')
  
  def Service(self, request, context):
    print('Server received: ' + request.request)        
    return grpcMessage.ServiceStatus(report = 'ServiceStatus: ' + 'B accomplished')

  def WrapUp(self, request, context):
    print('Server receive: ' + request.report)
    #self.going = False  # stop server after response is sent
    return grpcMessage.WrapUpReport(report = 'WrapUpReport: ' + 'Waiting for another request')

def serve():
  _timeout = _MAXIMUM_SERVICE_TIME_IN_MINUTES
  s = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  c = ServiceControl()
  grpcServe.add_ServiceControlServicer_to_server(c,s)
  s.add_insecure_port(_net_connection)
  _time_elapsed = 0 # elapsed time in minutes
  s.start()
  while c.going and _time_elapsed < _timeout:
     time.sleep(60) # sleep for one minute
     _time_elapsed += 1
  s.stop(0)

if __name__ == '__main__':
  serve()
