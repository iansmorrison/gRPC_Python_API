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

class GenericServer(grpcServe.ServiceControlServicer):

  def __init__(self):

    super().__init__()
    self.going = True

  def Query(self, request, context):
    self.messageFields['QueryRequest']['question'] = request.question
    self.messageFields['QueryReply']['answer'] = 'A or B or C'
    r = self.messageFields['QueryReply']
    return grpcMessage.QueryReply(**r)
  
  def Service(self, request, context):
    self.messageFields['ServiceRequest']['request'] = request.request
    self.messageFields['ServiceStatus']['report'] = 'B accomplished'
    r = self.messageFields['ServiceStatus']
    return grpcMessage.ServiceStatus(**r)

  def WrapUp(self, request, context):
    self.messageFields['ClientStatus']['report'] = request.report
    self.going = False  # stop server after response is sent
    self.messageFields['WrapUpReport']['report'] = 'Waiting for another request'
    r = self.messageFields['WrapUpReport']
    return grpcMessage.WrapUpReport(**r)

  def report(self):
    print('\n!!!!! Report of the gRPC sent and response messages !!!!')
    for rpc_name in self.rcpAndMessageNames.keys():
      print('\nRPC name: ' + rpc_name)
      for message_name in self.rcpAndMessageNames[rpc_name]:
        print('\tMessage name: ' + message_name)
        for field_name in self.messageFields[message_name].keys():
          field_value = self.messageFields[message_name][field_name]
          print('\t\t' + field_name + ' = ' + field_value)

class MetadataServer(GenericServer):

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
    
  def run(self):
    _timeout = _MAXIMUM_SERVICE_TIME_IN_MINUTES
    self.s = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    #self.c = self.ServiceControlServicer()
    grpcServe.add_ServiceControlServicer_to_server(self,self.s)
    self.s.add_insecure_port(_net_connection)
    _time_elapsed = 0 # elapsed time in minutes
    self.s.start()
    while self.going and _time_elapsed < _timeout:
      time.sleep(60) # sleep for one minute
      _time_elapsed += 1
    self.s.stop(0)

if __name__ == '__main__':
  s = MetadataServer()
  s.run()
  s.report()
