''' 
The following dictionaries store file and service names,
    which must align with the .proto file
This allows us to replace .proto-specific names with generic ones
    and remove these names from the program files
'''

PROTO_FILE = 'signal_server_to_client'

##SERVICE = 'SignalServerToClient'
SERVICE = 'ServerToClientStreaming'

#Coordinate client and server ports
NET_CONNECTION = 'localhost:50057'
