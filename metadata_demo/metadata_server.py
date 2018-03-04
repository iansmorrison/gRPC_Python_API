"""
The Python implementation of a generic GRPC service stub
Progammer David G Messerschmitt
19 Feb 2018
"""

import generic_server

class MetadataServer(generic_server.GenericServer):

  def __init__(self):
    super().__init__()

  def respond(self,rpc,recd,send):
    # arguments are rpc channel, and names of receive and send
    #   messages on that rpc
    # return value is False if there are no more responses, and
    #   True if there are more responses (please call respond() again)

    if rpc == 'Query':
      self.messageFields['QueryReply']['answer'] = 'A or B or C'
      
      # Only one response necessary (not streaming rpc)
      return False
      
    elif rpc == 'Service':
      self.messageFields['ServiceStatus']['report'] = 'B accomplished'
      return False
      
    elif rpc == 'WrapUp':
      self.messageFields['WrapUpReport']['report'] = 'Waiting for another request'
      return False


if __name__ == '__main__':

  s = MetadataServer()
  s.run()
  s.report() # view final state of messageFields
