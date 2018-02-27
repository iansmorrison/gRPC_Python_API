"""
The Python implementation of a generic GRPC service stub
Progammer David G Messerschmitt
19 Feb 2018
"""

import generic_server

class MetadataServer(generic_server.GenericServer):

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

  s = MetadataServer()
  s.run()
  s.report() # view final state of messageFields
