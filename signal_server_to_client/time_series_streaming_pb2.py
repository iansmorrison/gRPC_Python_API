# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: time_series_streaming.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='time_series_streaming.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x1btime_series_streaming.proto\"/\n\x06\x43onfig\x12\x11\n\toperation\x18\x01 \x01(\t\x12\x12\n\nparameters\x18\x02 \x01(\t\"\'\n\x04Info\x12\x10\n\x08response\x18\x01 \x01(\t\x12\r\n\x05\x61lert\x18\x02 \x01(\t\"\x1c\n\nRealSample\x12\x0e\n\x06sample\x18\x01 \x03(\x02\")\n\rComplexSample\x12\x18\n\x06sample\x18\x01 \x03(\x0b\x32\x08.Complex\"%\n\x07\x43omplex\x12\x0c\n\x04real\x18\x01 \x01(\x02\x12\x0c\n\x04imag\x18\x02 \x01(\x02\x32\x97\x01\n\x13TimeSeriesStreaming\x12&\n\x14MetaDataCoordination\x12\x07.Config\x1a\x05.Info\x12(\n\x0eRealTimeSeries\x12\x07.Config\x1a\x0b.RealSample0\x01\x12.\n\x11\x43omplexTimeSeries\x12\x07.Config\x1a\x0e.ComplexSample0\x01\x62\x06proto3')
)




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operation', full_name='Config.operation', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='Config.parameters', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=78,
)


_INFO = _descriptor.Descriptor(
  name='Info',
  full_name='Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='Info.response', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alert', full_name='Info.alert', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=119,
)


_REALSAMPLE = _descriptor.Descriptor(
  name='RealSample',
  full_name='RealSample',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sample', full_name='RealSample.sample', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=121,
  serialized_end=149,
)


_COMPLEXSAMPLE = _descriptor.Descriptor(
  name='ComplexSample',
  full_name='ComplexSample',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sample', full_name='ComplexSample.sample', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=151,
  serialized_end=192,
)


_COMPLEX = _descriptor.Descriptor(
  name='Complex',
  full_name='Complex',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='real', full_name='Complex.real', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='imag', full_name='Complex.imag', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=231,
)

_COMPLEXSAMPLE.fields_by_name['sample'].message_type = _COMPLEX
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
DESCRIPTOR.message_types_by_name['Info'] = _INFO
DESCRIPTOR.message_types_by_name['RealSample'] = _REALSAMPLE
DESCRIPTOR.message_types_by_name['ComplexSample'] = _COMPLEXSAMPLE
DESCRIPTOR.message_types_by_name['Complex'] = _COMPLEX
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), dict(
  DESCRIPTOR = _CONFIG,
  __module__ = 'time_series_streaming_pb2'
  # @@protoc_insertion_point(class_scope:Config)
  ))
_sym_db.RegisterMessage(Config)

Info = _reflection.GeneratedProtocolMessageType('Info', (_message.Message,), dict(
  DESCRIPTOR = _INFO,
  __module__ = 'time_series_streaming_pb2'
  # @@protoc_insertion_point(class_scope:Info)
  ))
_sym_db.RegisterMessage(Info)

RealSample = _reflection.GeneratedProtocolMessageType('RealSample', (_message.Message,), dict(
  DESCRIPTOR = _REALSAMPLE,
  __module__ = 'time_series_streaming_pb2'
  # @@protoc_insertion_point(class_scope:RealSample)
  ))
_sym_db.RegisterMessage(RealSample)

ComplexSample = _reflection.GeneratedProtocolMessageType('ComplexSample', (_message.Message,), dict(
  DESCRIPTOR = _COMPLEXSAMPLE,
  __module__ = 'time_series_streaming_pb2'
  # @@protoc_insertion_point(class_scope:ComplexSample)
  ))
_sym_db.RegisterMessage(ComplexSample)

Complex = _reflection.GeneratedProtocolMessageType('Complex', (_message.Message,), dict(
  DESCRIPTOR = _COMPLEX,
  __module__ = 'time_series_streaming_pb2'
  # @@protoc_insertion_point(class_scope:Complex)
  ))
_sym_db.RegisterMessage(Complex)



_TIMESERIESSTREAMING = _descriptor.ServiceDescriptor(
  name='TimeSeriesStreaming',
  full_name='TimeSeriesStreaming',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=234,
  serialized_end=385,
  methods=[
  _descriptor.MethodDescriptor(
    name='MetaDataCoordination',
    full_name='TimeSeriesStreaming.MetaDataCoordination',
    index=0,
    containing_service=None,
    input_type=_CONFIG,
    output_type=_INFO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RealTimeSeries',
    full_name='TimeSeriesStreaming.RealTimeSeries',
    index=1,
    containing_service=None,
    input_type=_CONFIG,
    output_type=_REALSAMPLE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ComplexTimeSeries',
    full_name='TimeSeriesStreaming.ComplexTimeSeries',
    index=2,
    containing_service=None,
    input_type=_CONFIG,
    output_type=_COMPLEXSAMPLE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TIMESERIESSTREAMING)

DESCRIPTOR.services_by_name['TimeSeriesStreaming'] = _TIMESERIESSTREAMING

# @@protoc_insertion_point(module_scope)
