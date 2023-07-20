__author__ = 'gram'


from engine import (
    set_debug, 
    place_objects, 
    add_location, 
    add_route, 
    set_location, 
    add_object, 
    set_goal,
    test
)

from engine import (
    game_action, 
    conditional_game_action, 
    have, 
    add_command, 
    run_game, 
    end_game, 
    enable_route
)

#from engine import post_handler

debug = False # Set to true to skip having to get the bucket and chain etc

chain_welded = debug
bucket_filled = debug
gate_unlocked = debug
key_dropped = False
wizard_splashed = False

set_debug(debug)

add_location('bedroom',
    'You are in the bedroom of a wizards house - there is a wizard snoring loudly on the bed.')

add_location('garden',
    'You are in a beautiful garden - there is a well in front of you.')

add_location('attic',
    'You are in the attic of the wizards house - there is a giant welding torch in the corner.')

add_location('forest',
             'You are in the middle of the deep woods. only a few rays of sunlight reach the ground from here. The porch of the wizard\'s house is to your right.')

add_route('bedroom', 'west', 'door', 'garden', True)
add_route('bedroom', 'upstairs', 'stairway', 'attic', True)
add_route('garden', 'east', 'door', 'bedroom', True)
add_route('attic', 'downstairs', 'stairway', 'bedroom', True)
add_route('garden', 'outside', 'gate', 'forest', False)
add_route('forest', 'inside', 'gate', 'garden', True)

# Locations of the objects.
place_objects({ 'bottle': 'bedroom', 
               'bucket' : 'bedroom', 
               'chain' : 'garden', 
               'frog' : 'garden', 
               'cake': 'forest' 
               })

set_location('bedroom')


def weld(subject, object):
    global chain_welded
    chain_welded, msg = game_action('weld', 'bucket', 'chain', 'attic', True,
                               chain_welded,
                               'The chain is now securely welded to the bucket.\n',
                               subject, object)
    return msg


def dunk(subject, object):
    global bucket_filled
    bucket_filled, msg = conditional_game_action('dunk', 'well', 'bucket', 'garden',
                                            False,
                                            bucket_filled, chain_welded,
                                            'The bucket is now full of water.\n',
                                            'The water is too low to reach.\n',
                                            subject, object)
    return msg


def splash(subject, object):
    global wizard_splashed
    ok, msg = conditional_game_action('splash', 'wizard', 'bucket', 'bedroom',
                                False, wizard_splashed, bucket_filled,
                                'The wizard awakens from his slumber.\n',
                                'You don\'t have a bucket of water.\n',
                               subject, object)
    if ok and not wizard_splashed:
        wizard_splashed = True
        if have('frog'):
            msg = msg + 'He see you that you stole his frog. He is so upset he banishes you to the netherworld. You lose!\n'
            end_game()
        else:
            msg = msg + 'He greets you warmly and drops a key. But he is confused why you woke him. What now?\n'
            add_object('key', 'bedroom')
    return msg


def hit(subject, object):
    ok, msg = game_action('hit', 'wizard', 'bucket' , 'bedroom', False, False,
                   'The wizard awakens angrily and turns you into a toad. You lose.\n',
                   subject, object)
    if ok:
        end_game()
    return msg


def unlock(subject, object):
    global gate_unlocked
    gate_unlocked, msg = \
        conditional_game_action('unlock', 'gate', 'key', 'garden',
                                False, gate_unlocked, True,
                               'You unlock the gate! It\'s very dark outside...\n',
                               'The gate is locked! You need a key to get in!\n',
                               subject, object)
    if gate_unlocked:
        enable_route('garden', 'outside')
    return msg


add_command(['splash', 'pour', 'empty'], splash, 2)
add_command(['dunk', 'fill', 'lower'], dunk, 2)
add_command(['weld', 'join', 'attach'], weld, 2)
add_command(['hit', 'strike', 'attack'], hit, 2)
add_command(['unlock', 'unlatch', 'open'], unlock, 2)

set_goal('cake', 'YES! CAKE! YOU WIN THE GAME 100000000 TIMES!!!\n')

if __name__ == "__main__":
    run_game()

