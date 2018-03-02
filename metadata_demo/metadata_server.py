"""
The Python implementation of a metadata demonstration service stub
Progammer David G Messerschmitt
19 Feb 2018
"""

import generic_server as gs

class MetadataServer(gs.GenericServer):

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
  # view final state of messageFields
  # note that what we would prefer is a log file that captures all the
  #   intermediate actions; that will be added later
  s.report()
