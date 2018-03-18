'''
The following dictionaries store service, rpc, and message names,
    which must align with the .proto file
This allows us to replace .proto-specific names with generic ones
    and remove these names from the base class program files
'''

PROTO_FILE = 'signal_server_to_client'

SERVICE = 'SignalServerToClient'

# this can be used for exception checking
RPC_AND_MESSAGE_NAMES = {
                            'MetaDataCoordination' : ['Config', 'Info'],
                            'OneDimensionalSignal' : ['Config', 'ComplexSample'],
                            'TwoDimensionalSignal' : ['Config', 'ComplexArray']
                          }

#Coordinate client and server ports to they can communicate
NET_CONNECTION = 'localhost:50057'
