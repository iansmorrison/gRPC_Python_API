'''
The following dictionaries store service, rpc, and message names,
    which must align with the .proto file
This allows us to replace .proto-specific names with generic ones
    and remove these names from the base class program files
'''

NAME_OF_PROTO_FILE = 'complex_signal'

SERVICE_NAME = 'ComplexSignal'

RPC_AND_MESSAGE_NAMES = {
                          'GetSignal' : ['Request', 'Signal']
                          }

#Coordinate client and server ports to they can communicate
NET_CONNECTION = 'localhost:50056'
