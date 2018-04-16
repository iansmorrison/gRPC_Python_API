''' 
The following dictionaries store file and service names,
    which must align with the .proto file
This allows us to replace .proto-specific names with generic ones
    and remove these names from the program files
'''

PROTO_FILE = 'time_series_streaming'

SERVICE = 'TimeSeriesStreaming'

#Coordinate client and server ports
NET_CONNECTION = 'localhost:50057'
