__author__ = 'gram'


class Game:
    def __init__(self):
        self.debug = False
        self.objects = []
        self.locations = {}
        self.non_debug_locations = {}
        self.game_map = {}
        self.location = ''
        self.game_over = False
        self.post_handler = None
        self.winning_object = ''
        self.winning_message = ''
        self.commands0 = {
            'inventory': self.inventory,
            'look': self.look,
         }

        self.commands1 = {
            'get': self.pickup,
            'take': self.pickup,
            'drop': self.drop,
            'walk': self.walk,
            'go': self.walk,
            'run': self.walk,
        }

        self.commands2 = {}

    def set_post_command_handler(self, h):
        self.post_handler = h

    def set_goal(self, object, message):
        self.winning_message = message
        self.winning_object = object

    def set_debug(self, v) -> None:
        self.debug = v
        self.set_debug_locations()

    def place_objects(self, v) -> None:
        for item, location in v.items():
            self.objects.append(item)
            self.non_debug_locations[item] = self.locations[item] = location
        self.set_debug_locations()

    def add_object(self, name, location) -> None:
        if location in self.game_map:
            self.objects.append(name)
            self.locations[name] = self.non_debug_locations[name] = location
        else:
            print('Unknown location %s' % location)
        
    def set_debug_locations(self) -> None:
        for object in self.objects:
            if self.debug:
                self.locations[object] = 'body'
            else:
                self.locations[object] = self.non_debug_locations[object]

    def add_location(self, name, description) -> None:
        """
        Add a location to map with the name 'name'. 'description' is what
        you see if you look in the location.
        """
        self.game_map[name] = [ description, []]

    def add_route(self, start, direction, type, destination, enabled):
        """
        Add a connection between start and destination, which you get to
        by going via direction. 'type' describes the portal.
        """
        if start not in self.game_map:
            print('%s is not a valid location' % start)
        elif destination not in self.game_map:
            print('%s is not a valid location' % destination)
        else:
            self.game_map[start][1].append([direction, type, destination, enabled])

    def enable_route(self, start, direction) -> None:
        if start not in self.game_map:
            print('%s is not a valid location' % start)
        else:
            routes = self.game_map[start][1]
            for route in routes:
                if route[0] == direction:
                    route[3] = True
                    break

    def set_location(self, v):
        """
        Set the player's current location.
        """
        self.location = v

    def describe_location(self, location, game_map):
        return self.game_map[location][0] + '\n'

    def describe_path(self, path):
        return 'There is a %s going %s from here.\n' % (path[1], path[0])

    def describe_paths(self, location, game_map):
        result = ''
        for path in self.game_map[location][1]:
            result = result + self.describe_path(path)
        return result

    def is_at(self, item, location, object_locations):
        return item in object_locations and object_locations[item] == location

    def describe_floor(self, location, objects, object_locations):
        result = ''
        for object in objects:
            if self.is_at(object, location, object_locations):
                result = result + ('You see a %s on the floor.\n' % object)
        return result

    def look(self):
        return self.describe_location(self.location, self.game_map) + \
            self.describe_paths(self.location, self.game_map) + \
            self.describe_floor(self.location, self.objects, self.locations)

    def walk(self, direction):
        for path in self.game_map[self.location][1]:
            if path[0] == direction:
                if not path[3]:
                    return 'That way is blocked.\n'
                self.location = path[2]
                return self.look()
        return 'You cannot go that way.\n'

    def pickup(self, object):
        #print 'Try get ', object, ' locations ', locations, 'current', location
        if self.is_at(object, self.location, self.locations):
            self.locations[object] = 'body'
            return 'You are now carrying the %s.\n' % object
        else:
            return 'You cannot get that.\n'

    def drop(self, object):
        if self.is_at(object, 'body', self.locations):
            self.locations[object] = self.location
            return 'You dropped the %s in the %s.\n' % (object, self.location)
        else:
            return 'You don\'t have the %s.\n' % object

    def have(self, object):
        return self.is_at(object, 'body', self.locations)

    def inventory(self, ):
        for object in self.objects:
            if self.have(object):
                print(object)

    def conditional_game_action(self, command, subject, object, place, need_subject, flag,
                                condition, success_message, fail_message, s, o):
        if o != object or s != subject:
            return False, 'You cannot do that.\n'

        if flag:
            return True, 'You have already done that.\n'

        if not self.have(object):
            return False, ('You don\'t have the %s.\n' % object)

        if need_subject and not self.have(subject):
            return False, ('You don\'t have the %s.\n' % subject)

        if place != 'any' and self.location != place:
            return False, 'You cannot do that here.\n'

        if condition:
            return True, success_message
        else:
            return False, fail_message

    def game_action(self, command, subject, object, place, need_subject, flag,
                    success_message, s, o):
        return self.conditional_game_action(command, subject, object, place, 
                                            need_subject, flag, True, 
                                            success_message, '', s, o)

    def add_command(self, name, handler, num_args):
        """
        Register a command handler. name can be a string or list of strings.
        """
        if type(name) is list:
            names = name
        else:
            names = [name]
        for verb in names:
            if num_args == 0:
                self.commands0[verb] = handler
            elif num_args == 1:
                self.commands1[verb] = handler
            elif num_args == 2:
                self.commands2[verb] = handler
            else:
                print('num_args must be 0, 1 or 2')
                break

    def end_game(self):
        self.game_over = True

    def execute(self, line):
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

        tokens = [word for word in tokens if word not in
                ['around', 'to', 'on', 'in', 'the', 'a']]
        if 'with' in tokens:
            # Remove the 'with' and reverse subject/object
            tokens = list(reversed([word for word in tokens if word not in ['with']]))

        if not tokens:
            if verb in self.commands0:
                result = self.commands0[verb]()
            elif verb in self.commands1 or verb in self.commands2:
                return "%s what?\n" % verb.capitalize()
            else:
                return 'I don\'t know how to %s.\n' % line
        elif len(tokens) == 1:
            if verb in self.commands1:
                result = self.commands1[verb](tokens[0])
            elif verb in self.commands2:
                return '%s %s how?\n' % (verb.capitalize(), tokens[0])
            elif verb in self.commands0:
                return 'I\'m not sure what you mean.'
            else:
                return 'I don\'t know how to %s.\n' % line
        elif len(tokens) == 2:
            if verb in self.commands2:
                result = self.commands2[verb](tokens[1], tokens[0])
            elif verb in self.commands0 or verb in self.commands1:
                return 'I\'m not sure what you mean.\n'
            else:
                return 'I don\'t know how to %s.\n' % line

        if self.winning_object != '' and self.have(self.winning_object):
            result += '\n' + self.winning_message
            self.end_game()

        if self.post_handler:
            result = result + self.post_handler()
        return result

    def run_game(self):
        print(self.look())

        while not self.game_over:
            line = input()
            print(self.execute(line))

    def replay(self, actions):
        for action in actions:
            print(action)
            print(self.execute(action))

    def test(self, steps):
        i = 0
        for step in steps:
            result = self.execute(step[0])
            if sorted(result) == sorted(step[1]):
                print('Pass ', i)
            else:
                print('Fail %d:\n\tExpected [%s]\n\tActual: [%s]' % (i, step[1], result))
                break
            i = i + 1

