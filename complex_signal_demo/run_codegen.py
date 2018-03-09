
"""
Runs protoc with the gRPC plugin to generate messages and gRPC stubs
"""

from grpc_tools import protoc
    
# this file contains definitions of SERVICE_NAME,
# RPC_AND_MESSAGE_NAMES and MESSAGE_FIELDS
# these are shared between client and server
from PROTO_DEFINITIONS import *

subDirectory = '.'

outcome = protoc.main(
    (
	'',
	'--proto_path=.',
	'--python_out=' + subDirectory,
	'--grpc_python_out=' + subDirectory,
	'./' + PROTO_FILE + '.proto',
    )
)

print(outcome)
