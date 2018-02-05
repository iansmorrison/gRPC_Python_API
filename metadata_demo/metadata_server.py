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
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_timeout = _ONE_DAY_IN_SECONDS # Elapsed time before giving up
_net_connection = 'localhost:50055' # Port to listen to for RPC requests


class ServiceControl(metadata_demo_pb2_grpc.ServiceControlServicer):

  def Query(self, request, context):
    print('Query received: ' + request.question)
    return metadata_demo_pb2.QueryReply(answer = 'QueryReply: ' + 'A or B or C')
  
  def Service(self, request, context):
    print('Service request received: ' + request.request)        
    return metadata_demo_pb2.ServiceStatus(report = 'ServiceStatus: ' + 'B accomplished')

  def WrapUp(self, request, context):
    print('Client status received: ' + request.report) 
    return metadata_demo_pb2.WrapUpReport(report = 'WrapUpReport: ' + 'Waiting for another request')


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  metadata_demo_pb2_grpc.add_ServiceControlServicer_to_server(ServiceControl(),server)
  server.add_insecure_port(_net_connection)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()
