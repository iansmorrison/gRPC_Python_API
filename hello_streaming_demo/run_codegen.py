
"""
Runs protoc with the gRPC plugin to generate messages and gRPC stubs
"""

from grpc_tools import protoc

protoc.main(
    (
	'',
	'--proto_path=.',
	'--python_out=.',
	'--grpc_python_out=.',
	'./hellostreamingworld.proto',
    )
)
