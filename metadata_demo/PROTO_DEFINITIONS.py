'''
The following dictionaries store service, rpc, and message names,
which must align with the .proto file
Basically this is an equivalent representation of the .proto file

'''

NAME_OF_PROTO_FILE = 'metadata_demo'

SERVICE_NAME = 'ServiceControl'

RPC_AND_MESSAGE_NAMES = {
                          'Query' :      ['QueryRequest',    'QueryReply'    ],
                          'Service' :    ['ServiceRequest',  'ServiceStatus' ],
                          'WrapUp':      ['ClientStatus',    'WrapUpReport'  ]
                          }

MESSAGE_FIELDS =    {
                      'QueryRequest':     {'question' : None  },
                      'ServiceRequest' :  {'request'  : None  },
                      'ClientStatus' :    {'report'   : None  },
                      'QueryReply':       {'answer'   : None  },
                      'ServiceStatus':    {'report'   : None  },
                      'WrapUpReport':     {'report'   : None  }
                      }

'''
Also define configuration parameters
'''

MAXIMUM_SERVICE_TIME_IN_MINUTES = 15
NET_CONNECTION = 'localhost:50055'
