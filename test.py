__author__ = 'gram'

from spels import SpellGame


SpellGame().test([
    [ 'get chain', 'You cannot get that.\n'],
    [ 'get egg', 'You cannot get that.\n' ],
    [ 'go west', '''You are in a beautiful garden - there is a well in front of you.
There is a door going east from here.
There is a gate going outside from here.
You see a frog on the floor.
You see a chain on the floor.
'''],
    [ 'unlock gate', 'Unlock gate how?\n'],
    [ 'unlock gate with key', 'You don\'t have the key.\n'],
    [ 'get chain', 'You are now carrying the chain.\n'],
    [ 'drop bucket', 'You don\'t have the bucket.\n'],
    [ 'drop chain', 'You dropped the chain in the garden.\n'],
    [ 'get chain', 'You are now carrying the chain.\n'],
    [ 'go east', '''You are in the bedroom of a wizards house - there is a wizard snoring loudly on the bed.
There is a door going west from here.
There is a stairway going upstairs from here.
You see a bucket on the floor.
You see a bottle on the floor.
'''],
    [ 'get bucket', 'You are now carrying the bucket.\n'],
    [ 'go upstairs', '''You are in the attic of the wizards house - there is a giant welding torch in the corner.
There is a stairway going downstairs from here.
'''],
    [ 'weld chain to bucket', 'The chain is now securely welded to the bucket.\n'],
    [ 'go downstairs', '''You are in the bedroom of a wizards house - there is a wizard snoring loudly on the bed.
There is a door going west from here.
There is a stairway going upstairs from here.
You see a bottle on the floor.
'''],
    [ 'go west', '''You are in a beautiful garden - there is a well in front of you.
There is a door going east from here.
There is a gate going outside from here.
You see a frog on the floor.
'''],
    [ 'dunk bucket in well', 'The bucket is now full of water.\n'],
    [ 'go east', '''You are in the bedroom of a wizards house - there is a wizard snoring loudly on the bed.
There is a door going west from here.
There is a stairway going upstairs from here.
You see a bottle on the floor.
'''],
    [ 'splash wizard with bucket', '''The wizard awakens from his slumber.
He greets you warmly and drops a key. But he is confused why you woke him. What now?
'''],
    [ 'splash wizard with bucket', 'You have already done that.\n' ],
    [ 'get key', 'You are now carrying the key.\n'],
    [ 'go west', '''You are in a beautiful garden - there is a well in front of you.
There is a door going east from here.
There is a gate going outside from here.
You see a frog on the floor.
'''],
    [ 'break gate', 'I don\'t know how to break gate.\n'],
    [ 'unlock gate', 'Unlock gate how?\n'],
    [ 'unlock gate with key', 'You unlock the gate! It\'s very dark outside...\n'],
    [ 'go outside', '''You are in the middle of the deep woods. only a few rays of sunlight reach the ground from here. The porch of the wizard\'s house is to your right.
There is a gate going inside from here.
You see a cake on the floor.
'''],
    [ 'go', 'Go what?\n'],
    [ 'get cake', '''You are now carrying the cake.

YES! CAKE! YOU WIN THE GAME 100000000 TIMES!!!
''']]
)

