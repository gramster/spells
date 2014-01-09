__author__ = 'gram'

debug = False
objects = []
locations = {}
non_debug_locations = {}
game_map = {}
location = ''
game_over = False
post_handler = None


def set_post_command_handler(h):
    global post_handler
    post_handler = h


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
    return game_map[location][0] + '\n'

def describe_path(path):
    return 'There is a %s going %s from here.\n' % (path[1], path[0])

def describe_paths(location, game_map):
    result = ''
    for path in game_map[location][1]:
        result = result + describe_path(path)
    return result

def is_at(object, location, object_locations):
    return object in object_locations and object_locations[object] == location

def describe_floor(location, objects, object_locations):
    result = ''
    for object in objects:
        if is_at(object, location, object_locations):
            result = result + ('You see a %s on the floor.\n' % object)
    return result

def look():
    return describe_location(location, game_map) + \
        describe_paths(location, game_map) + \
        describe_floor(location, objects, locations)

def walk(direction):
    global location
    for path in game_map[location][1]:
        if path[0] == direction:
            if not path[3]:
                return 'That way is blocked.\n'
            location = path[2]
            return look()
    return 'You cannot go that way.\n'

def pickup(object):
    #print 'Try get ', object, ' locations ', locations, 'current', location
    if is_at(object, location, locations):
        locations[object] = 'body'
        return 'You are now carrying the %s\n' % object
    else:
        return 'You cannot get that.\n'

def drop(object):
    if is_at(object, 'body', locations):
        locations[object] = location
        return 'You dropped the %s in the %s\n' % (object, location)
    else:
        return 'You don\'t have the %s\n' % object


def have(object):
    return is_at(object, 'body', locations)


def inventory():
    for object in objects:
        if have(object):
            print object


def conditional_game_action(command, subject, object, place, need_subject, flag,
                            condition, success_message, fail_message, s, o):
    if o != object or s != subject:
        return False, 'You cannot do that.\n'

    if flag:
        return True, 'You have already done that.\n'

    if not have(object):
        return False, ('You don\'t have the %s\n' % object)

    if need_subject and not have(subject):
        return False, ('You don\'t have the %s\n' % subject)

    if place != 'any' and location != place:
        return False, 'You cannot do that here.\n'

    if condition:
        return True, success_message
    else:
        return False, fail_message


def game_action(command, subject, object, place, need_subject, flag,
                success_message, s, o):
    return conditional_game_action(command, subject, object, place, need_subject,
                                   flag, True, success_message, '', s, o)

commands0 = {
    'inventory': inventory,
    'look': look,
}

commands1 = {
    'get': pickup,
    'take': pickup,
    'drop': drop,
    'walk': walk,
    'go': walk,
    'run': walk,
    }

commands2 = {}

def add_commands(c):
    global commands
    commands.update(c)

def add_command(name, handler, num_args):
    """
    Register a command handler. name can be a string or list of strings.
    """
    global commands0, commands1, commands2
    if type(name) is list:
        names = name
    else:
        names = [name]
    for verb in names:
        if num_args == 0:
            commands0[verb] = handler
        elif num_args == 1:
            commands1[verb] = handler
        elif num_args == 2:
            commands2[verb] = handler
        else:
            print 'num_args must be 0, 1 or 2'
            break

def end_game():
    global game_over
    game_over = True


def execute(line):
    result = ''
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

    if len(tokens) == 0:
        if verb in commands0:
            result = commands0[verb]()
        elif verb in commands1 or verb in commands2:
            return "%s what?\n" % verb
        else:
            return 'I don\'t know how to %s\n' % line
    elif len(tokens) == 1:
        if verb in commands1:
            result = commands1[verb](tokens[0])
        elif verb in commands2:
            return '%s %s how?\n' % (verb, tokens[0])
        elif verb in commands0:
            return 'I\'m not sure what you mean'
        else:
            return 'I don\'t know how to %s\n' % line
    elif len(tokens) == 2:
        if verb in commands2:
            result = commands2[verb](tokens[1], tokens[0])
        elif verb in commands0 or verb in commands1:
            return 'I\'m not sure what you mean.\n'
        else:
            return 'I don\'t know how to %s\n' % line

    if post_handler:
        result = result + post_handler()
    return result


def run_game():
    look()

    while not game_over:
        line = raw_input()
        print execute(line)

def replay(actions):
    for action in actions:
        print action
        print execute(action)



