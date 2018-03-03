"""
The Python implementation of a generic GRPC service stub
Progammer David G Messerschmitt
19 Feb 2018
"""

from concurrent import futures
import time
import importlib

# this file contains definitions of SERVICE_NAME,
# RPC_AND_MESSAGE_NAMES and MESSAGE_FIELDS
# these are shared between client and server
from PROTO_DEFINITIONS import *

# gRPC engine
import grpc

# Import gRPC-compiled modules, removing the .proto-specific naming                                  
grpcServe = importlib.import_module('{0}_pb2_grpc'.format(NAME_OF_PROTO_FILE))
grpcMessage = importlib.import_module('{0}_pb2'.format(NAME_OF_PROTO_FILE))

# Do the same for needed methods within the modules
grpcServicer = getattr(grpcServe,'{0}Servicer'.format(SERVICE_NAME))
grpcAddServicer = getattr(grpcServe,'add_{0}Servicer_to_server'.format(SERVICE_NAME))

# dynamically create class GenericServer that inherits from grpcServe
#   and adds methods specific to this rpc context
class GenericServer(grpcServicer):

  def __init__(self):
    
    self.going = True   # set False to force server termination at the next opportunity
    self.timeout = MAXIMUM_SERVICE_TIME_IN_MINUTES
    
    # copy of message fields which can be used to store messages and responses
    self.messageFields = MESSAGE_FIELDS.copy()
    
    super().__init__()

  def intercept(self,rpc,request):
    # intercepts incoming message via rpc, stores message on dictionary and
    #   calls server to read message and formulate reply, then sends reply to client via rpc

    # print request: a poor man's substitute for a proper log file
    print('Received message to server on RPC channel: ' + rpc)
    print(request)
    
    # access list of messages names for this rpc
    [recd,send] = RPC_AND_MESSAGE_NAMES[rpc]
    
    # for each field in receive message, store received value in message dictionary
    for field in self.messageFields[recd].keys():
      self.messageFields[recd][field] = getattr(request,field)
      
    # now call runtime method which formulates a response and store in messageFields[][]
    # normally server implementation will provide this method
    #   that responds to each possible received message recd
    self.response(rpc)

    # pull that response from the dictonary, assuming it has been stored there by the client
    r = self.messageFields[send]
    
    # at this point it would make sense to log received message and response
    #     in a format similar to report()

    # pass response message to gRPC to be sent to client
    sendMessage = getattr(grpcMessage,send) # appropriate gRPC method to handle this request
    return sendMessage(**r) # unpack message fields and hand over to gRPC
  
  def report(self):
    # capture final state of messageFields
    print('\n!!!!! Report of the gRPC sent and response messages !!!!')
    for rpc_name in RPC_AND_MESSAGE_NAMES.keys():
      print('\nRPC name: ' + rpc_name)
      for message_name in RPC_AND_MESSAGE_NAMES[rpc_name]:
        print('\tMessage name: ' + message_name)
        for field_name in self.messageFields[message_name].keys():
          field_value = self.messageFields[message_name][field_name]
          print('\t\t' + field_name + ' = ' + field_value)

  def run(self):

    # instantiate server
    self.s = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add server to pool
    grpcAddServicer(self,self.s)
    # open network port to server    
    self.s.add_insecure_port(NET_CONNECTION)

    # start server, stop when requested or following a timeout
    self.time_elapsed = 0 # elapsed time in minutes
    self.s.start()
    while self.going and self.time_elapsed < self.timeout:
      time.sleep(60) # sleep for one minute
      self.time_elapsed += 1
    self.s.stop(0)

'''
grpcServe is expecting a set of methods, one for each rcp stmt in the .proto file
   which intercept incoming messages on that rcp and send reply
 since names are context dependent, we create these methods dynamically
   and then add to GenericServer class using setattr()
 Note: I would love to replace the exec() ugliness, but I have tried and failed
'''
for rpc in RPC_AND_MESSAGE_NAMES.keys():
  exec(
'''
def h(self,request,context):   # h is a placeholder, immediately deleted
  return self.intercept("{0}",request)
'''.format(rpc)
       )
  setattr(GenericServer,rpc,h)
  del(h)

