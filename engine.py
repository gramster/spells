
debug = False
objects = []
locations = {}
non_debug_locations = {}
game_map = {}
location = ''
game_over = False
winning_object = ''
winning_message = ''

def set_goal(object, message):
    global winning_message, winning_object
    winning_message = message
    winning_object = object

def set_debug(v):
    global debug
    debug = v
    set_debug_locations()

def place_objects(v):
    global locations
    global non_debug_locations
    global objects
    locations = {}
    objects = []
    non_debug_locations = {}
    for object in v.iterkeys():
        objects.append(object)
        non_debug_locations[object] = locations[object] = v[object]

    set_debug_locations()

def add_object(name, location):
    global objects, locations, non_debug_locations
    if location not in game_map:
        print 'Unknown location %s' % location
        return
    objects.append(name)
    locations[name] = non_debug_locations[name] = location

def set_debug_locations():
    global locations, non_debug_locations, objects
    for object in objects:
        if debug:
            locations[object] = 'body'
        else:
            locations[object] = non_debug_locations[object]

def add_location(name, description):
    """
    Add a location to map with the name 'name'. 'description' is what
    you see if you look in the location.
    """
    global game_map
    game_map[name] = [ description, []]

def add_route(start, direction, type, destination, enabled):
    """
    Add a connection between start and destination, which you get to
    by going via direction. 'type' describes the portal.
    """
    global game_map
    if not start in game_map:
        print '%s is not a valid location' % start
    elif not destination in game_map:
        print '%s is not a valid location' % destination
    else:
        game_map[start][1].append([direction, type, destination, enabled])

def enable_route(start, direction):
    global game_map
    if not start in game_map:
        print '%s is not a valid location' % start
    else:
        routes = game_map[start][1]
        for route in routes:
            if route[0] == direction:
                route[3] = True
                break

def set_location(v):
    """
    Set the player's current location.
    """
    global location
    location = v

def describe_location(location, game_map):
    print game_map[location][0]

def describe_path(path):
    print 'There is a ', path[1], ' going ', path[0], ' from here.'

def describe_paths(location, game_map):
    for path in game_map[location][1]:
        describe_path(path)

def is_at(object, location, object_locations):
    return object in object_locations and object_locations[object] == location

def describe_floor(location, objects, object_locations):
    for object in objects:
        if is_at(object, location, object_locations):
            print 'You see a ', object, ' on the floor.'

def look(args):
    describe_location(location, game_map)
    describe_paths(location, game_map)
    describe_floor(location, objects, locations)

def walk(args):
    global location
    direction = args[0]
    for path in game_map[location][1]:
        if path[0] == direction:
            if not path[3]:
                print 'That way is blocked'
                return
            location = path[2]
            look([])
            return
    print 'You cannot go that way.'

def pickup(args):
    for object in args:
        #print 'Try get ', object, ' locations ', locations, 'current', location
        if is_at(object, location, locations):
            locations[object] = 'body'
            print 'You are now carrying the ', object
        else:
            print 'You cannot get that.'

def drop(args):
    for object in args:
        if is_at(object, 'body', locations):
            locations[object] = location
            print 'You dropped the ', object, ' in the ', location
        else:
            print 'You don\'t have the ', object

def have(object):
    return is_at(object, 'body', locations)


def inventory(args):
    for object in objects:
        if have(object):
            print object


def conditional_game_action(command, subject, object, place, need_subject, flag, \
                            condition, success_message, fail_message, args):
    if len(args) < 2:
        print 'How?'
        return False

    if args[0] != object or args[1] != subject:
        print 'You cannot do that'
        return False

    if flag:
        print 'You have already done that'
        return True
    if not have(object):
        print 'You don\'t have the ', object
        return False
    if need_subject and not have(subject):
        print 'You don\'t have the ', subject
        return False

    if place != 'any' and location != place:
        print 'You cannot do that here.'
        return False

    if condition:
        print success_message
        return True
    else:
        print fail_message
        return False

def game_action(command, subject, object, place, need_subject, flag, \
                success_message, args):
    return conditional_game_action(command, subject, object, place, need_subject, \
                                   flag, True, success_message, '', args)

commands = {
    'inventory': inventory,
    'get': pickup,
    'take': pickup,
    'drop': drop,
    'walk': walk,
    'go': walk,
    'run': walk,
    'look': look,
}

def add_commands(c):
    global commands
    commands.update(c)

def end_game():
    global game_over
    game_over = True


def execute(line):
    tokens = line.split(' ')

    # remove and save the first token; it is the verb.
    verb = tokens[0]
    tokens.pop(0)
    # Try to decide whether subject comes before object.
    # E.g.:
    # drop <object>
    # verb <object> on/in/to <subject>
    # verb <subject> with <object>

    # remove tokens that are just fluff, like 'around', 'to'

    tokens = [word for word in tokens if not word in ['around', 'to', 'on', 'in', 'the', 'a']]
    if 'with' in tokens:
        # Remove the 'with' and reverse subject/object
        tokens = reversed([word for word in tokens if not word in ['with']])

        tokens = [word for word in tokens if not word in ['with']]
    if verb in commands:
        commands[verb](tokens)
        if winning_object != '' and have(winning_object):
            print winning_message
            end_game()
    else:
        print 'I didn\'t understand that'


def run_game():
    look([])

    while not game_over:
        line = raw_input()
        execute(line)

def replay(actions):
    for action in actions:
        print action
        execute(action)



