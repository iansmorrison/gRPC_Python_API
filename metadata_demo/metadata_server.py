"""
The Python implementation of a generic GRPC service stub
Progammer David G Messerschmitt
19 Feb 2018
"""

from concurrent import futures
import time

# this file contains definitions of SERVICE_NAME,
# RPC_AND_MESSAGE_NAMES and MESSAGE_FIELDS
# these are shared between client and server
from PROTO_DEFINITIONS import *

# gRPC engine
import grpc

# files compiled from the .proto file
cmd = 'import {0}_pb2 as grpcMessage'.format(NAME_OF_PROTO_FILE)
# Example:
# import metadata_demo_pb2 as grpcMessage
exec(cmd)
cmd = 'import {0}_pb2_grpc as grpcServe'.format(NAME_OF_PROTO_FILE)
# Example:
# import metadata_demo_pb2_grpc as grpcServe
exec(cmd)


# dynamically create class GenericServer that inherits from grpcServe
#   and adds methods specific to this rpc context
exp = 'grpcServe.{0}Servicer'.format(SERVICE_NAME)
class GenericServer(eval(exp)):

  def __init__(self):
    self.going = True
    self.timeout = MAXIMUM_SERVICE_TIME_IN_MINUTES
    # copy of message fields which can be used to store messages and responses
    self.messageFields = MESSAGE_FIELDS.copy()
    super().__init__()

  def intercept(self,rpc,request):
    # intercepts incoming message on rpc, stores message on dictionary and
    #   calls server to read message and formulate reply, which is then sent
  
    # access list of messages names for this rpc_name
    [recd,reply] = RPC_AND_MESSAGE_NAMES[rpc]
    
    # for each field in receive message, store received value in message dictionary
    for field in self.messageFields[recd].keys():
      self.messageFields[recd][field] = eval('request.{0}'.format(field))
      
    # now call runtime method so it can formulate a response and store in message dictonary
    self.response(recd)

    # pull that response from the dictonary, assuming it has been stored there by the client
    r = self.messageFields[reply]
    
    # at this point it would make sense to log received message and response
    #     in a format similar to report()

    # pass response message to gRPC to be sent to client
    exp = 'grpcMessage.{0}(**r)'.format(reply)
    return eval(exp)
  
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
    cmd = 'grpcServe.add_{0}Servicer_to_server(self,self.s)'.format(SERVICE_NAME)
    eval(cmd)

    # open network port to server    
    self.s.add_insecure_port(NET_CONNECTION)

    # start server, stop when requested or timeout
    self.time_elapsed = 0 # elapsed time in minutes
    self.s.start()
    while self.going and self.time_elapsed < self.timeout:
      time.sleep(60) # sleep for one minute
      self.time_elapsed += 1
    self.s.stop(0)


# grpcServe is expecting a set of methods, one for each rcp stmt in the .proto file
#   which intercept incoming messages and send reply
# since names are context dependent, we create these methods dynamically
#   and then add to GenericServer class using setattr()
for rpc in RPC_AND_MESSAGE_NAMES.keys():
  exec('''
def h(self,request,context):
  return self.intercept("{0}",request)
  '''.format(rpc))
  setattr(GenericServer,rpc,h)
  

class MetadataServer(GenericServer):

  def __init__(self):
    super().__init__()

  def response(self,message):

    if message == 'QueryRequest':
      self.messageFields['QueryReply']['answer'] = 'A or B or C'
    elif message == 'ServiceRequest':
      self.messageFields['ServiceStatus']['report'] = 'B accomplished'
    elif message == 'ClientStatus':
      self.messageFields['WrapUpReport']['report'] = 'Waiting for another request'
  

if __name__ == '__main__':
  dir(GenericServer)
  dir(MetadataServer)
  s = MetadataServer()
  s.run()
  s.report() # view final state of messageFields
