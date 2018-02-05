
"""
Runs protoc with the gRPC plugin to generate messages and gRPC stubs
"""

from grpc_tools import protoc

file_name = 'metadata_demo'

outcome = protoc.main(
    (
	'',
	'--proto_path=.',
	'--python_out=.',
	'--grpc_python_out=.',
	'./' + file_name + '.proto',
    )
)

print(outcome)
