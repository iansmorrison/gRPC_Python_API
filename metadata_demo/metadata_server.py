"""
The Python implementation of a generic GRPC service stub
Progammer David G Messerschmitt
19 Feb 2018
"""

from concurrent import futures
import time
import grpc
import metadata_demo_pb2 as grpcMessage
import metadata_demo_pb2_grpc as grpcServe

# Configuration
_MAXIMUM_SERVICE_TIME_IN_MINUTES = 15
_net_connection = 'localhost:50055'
service_name = 'ServiceControl'

class ServiceControl(grpcServe.ServiceControlServicer):

  def __init__(self):

    # drawn from .proto file
    self.serviceName = 'ServiceControl'

    # dictionaries of rpc and message names must align with .proto file
    self.rcpAndMessageNames = {
                                'Query' :      ['QueryRequest',    'QueryReply'    ],
                                'Service' :    ['ServiceRequest',  'ServiceStatus' ],
                                'WrapUp':      ['ClientStatus',    'WrapUpReport'  ]
                              }

    # any desired default values can be introduced here in place of None
    # any message fields not defaulted or set here will default to gRPC-defined values
    self.messageFields =    {
                              'QueryRequest':     {'question' : None  },
                              'ServiceRequest' :  {'request'  : None  },
                              'ClientStatus' :    {'report'   : None  },
                              'QueryReply':       {'answer'   : None  },
                              'ServiceStatus':    {'report'   : None  },
                              'WrapUpReport':     {'report'   : None  }
                            }

    super().__init__()
    self.going = True

  def Query(self, request, context):
    self.messageFields['QueryReply']['answer'] = 'A or B or C'
    r = self.messageFields['QueryReply']
    return grpcMessage.QueryReply(**r)
  
  def Service(self, request, context):
    self.messageFields['ServiceStatus']['report'] = 'B accomplished'
    r = self.messageFields['ServiceStatus']
    return grpcMessage.ServiceStatus(**r)

  def WrapUp(self, request, context):
    #self.going = False  # stop server after response is sent
    self.messageFields['WrapUpReport']['report'] = 'Waiting for another request'
    r = self.messageFields['WrapUpReport']
    return grpcMessage.WrapUpReport(**r)

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
