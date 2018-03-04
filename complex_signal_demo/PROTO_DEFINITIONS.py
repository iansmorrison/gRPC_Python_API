'''
The following dictionaries store service, rpc, and message names,
which must align with the .proto file
Basically this is an equivalent representation of the .proto file

'''

NAME_OF_PROTO_FILE = 'complex_signal'

SERVICE_NAME = 'ComplexSignal'

RPC_AND_MESSAGE_NAMES = {
                          'GetSignal' : ['Request', 'Signal']
                          }

MESSAGE_FIELDS =    {
                      'Request':
                          {
                            'phaseBegin' : None,
                            'phaseIncrement' : None,
                            'numSamples': None
                           },
                      'Signal':
                          {
                           'real' : None
                           }
                      }

'''
Also define server configuration parameters
'''

MAXIMUM_SERVICE_TIME_IN_MINUTES = 15
NET_CONNECTION = 'localhost:50056'
