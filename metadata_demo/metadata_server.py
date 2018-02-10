"""
The Python implementation of the GRPC helloworld.Greeter client.
This version modified by David G Messerschmitt
27 Jan 2018
"""

from concurrent import futures
import time
import grpc
import metadata_demo_pb2
import metadata_demo_pb2_grpc

# Configuration
_MAXIMUM_SERVICE_TIME_IN_MINUTES = 2
_net_connection = 'localhost:50055' # Port to listen to for RPC requests


class ServiceControl(metadata_demo_pb2_grpc.ServiceControlServicer):

  def __init__(self):
    super().__init__()
    self.going = True

  def Query(self, request, context):
    print('Server received: ' + request.question)
    return metadata_demo_pb2.QueryReply(answer = 'QueryReply: ' + 'A or B or C')
  
  def Service(self, request, context):
    print('Server received: ' + request.request)        
    return metadata_demo_pb2.ServiceStatus(report = 'ServiceStatus: ' + 'B accomplished')

  def WrapUp(self, request, context):
    print('Server receive: ' + request.report)
    self.going = False  # stop server after response is sent
    return metadata_demo_pb2.WrapUpReport(report = 'WrapUpReport: ' + 'Waiting for another request')


def serve():
  _timeout = _MAXIMUM_SERVICE_TIME_IN_MINUTES
  s = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  c = ServiceControl()
  metadata_demo_pb2_grpc.add_ServiceControlServicer_to_server(c,s)
  s.add_insecure_port(_net_connection)
  _time_elapsed = 0 # elapsed time in minutes
  s.start()
  while c.going and _time_elapsed < _timeout:
    time.sleep(60) # sleep for one minute
    _time_elapsed += 1
  s.stop(0)


if __name__ == '__main__':
  serve()
