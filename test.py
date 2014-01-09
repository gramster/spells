__author__ = 'gram'

from engine import replay
import spels

# TODO - now that we have commands returning strings instead of printing them,
# write expectations for each command.

replay([
    'get chain',
    'get egg',
    'go west',
    'unlock gate',
    'unlock gate with key',
    'get chain',
    'drop bucket',
    'drop chain',
    'get chain',
    'go east',
    'get bucket',
    'go upstairs',
    'weld chain to bucket',
    'go downstairs',
    'go west',
    'dunk bucket in well',
    'go east',
    'splash wizard with bucket',
    'get key',
    'go west',
    'break gate',
    'unlock gate',
    'unlock gate with key',
    'go outside',
    'get crowbar',
    'kill beast with crowbar',
    'go',
    'get cake'
])