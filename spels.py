__author__ = 'gram'


from engine import Game


class SpellGame(Game):

    def __init__(self, debug=False):
        super().__init__()


        # Set debug to true to skip having to get the bucket and chain etc

        self.chain_welded = debug
        self.bucket_filled = debug
        self.gate_unlocked = debug
        self.key_dropped = False
        self.wizard_splashed = False

        self.set_debug(debug)

        self.add_location('bedroom',
            'You are in the bedroom of a wizards house - there is a wizard snoring loudly on the bed.')

        self.add_location('garden',
            'You are in a beautiful garden - there is a well in front of you.')

        self.add_location('attic',
            'You are in the attic of the wizards house - there is a giant welding torch in the corner.')

        self.add_location('forest',
                    'You are in the middle of the deep woods. only a few rays of sunlight reach the ground from here. The porch of the wizard\'s house is to your right.')

        self.add_route('bedroom', 'west', 'door', 'garden', True)
        self.add_route('bedroom', 'upstairs', 'stairway', 'attic', True)
        self.add_route('garden', 'east', 'door', 'bedroom', True)
        self.add_route('attic', 'downstairs', 'stairway', 'bedroom', True)
        self.add_route('garden', 'outside', 'gate', 'forest', False)
        self.add_route('forest', 'inside', 'gate', 'garden', True)

        # Locations of the objects.
        self.place_objects({ 'bottle': 'bedroom', 
                    'bucket' : 'bedroom', 
                    'chain' : 'garden', 
                    'frog' : 'garden', 
                    'cake': 'forest' 
                    })

        self.set_location('bedroom')

        self.add_command(['splash', 'pour', 'empty'], self.splash, 2)
        self.add_command(['dunk', 'fill', 'lower'], self.dunk, 2)
        self.add_command(['weld', 'join', 'attach'], self.weld, 2)
        self.add_command(['hit', 'strike', 'attack'], self.hit, 2)
        self.add_command(['unlock', 'unlatch', 'open'], self.unlock, 2)

        self.set_goal('cake', 'YES! CAKE! YOU WIN THE GAME 100000000 TIMES!!!\n')


    def weld(self, subject, object):
        self.chain_welded, msg = self.game_action('weld', 'bucket', 'chain', 'attic', True,
                                self.chain_welded,
                                'The chain is now securely welded to the bucket.\n',
                                subject, object)
        return msg


    def dunk(self, subject, object):
        self.bucket_filled, msg = self.conditional_game_action('dunk', 'well', 'bucket', 'garden',
                                                False,
                                                self.bucket_filled, self.chain_welded,
                                                'The bucket is now full of water.\n',
                                                'The water is too low to reach.\n',
                                                subject, object)
        return msg


    def splash(self, subject, object):
        ok, msg = self.conditional_game_action('splash', 'wizard', 'bucket', 'bedroom',
                                    False, self.wizard_splashed, self.bucket_filled,
                                    'The wizard awakens from his slumber.\n',
                                    'You don\'t have a bucket of water.\n',
                                subject, object)
        if ok and not self.wizard_splashed:
            self.wizard_splashed = True
            if self.have('frog'):
                msg = msg + 'He see you that you stole his frog. He is so upset he banishes you to the netherworld. You lose!\n'
                self.end_game()
            else:
                msg = msg + 'He greets you warmly and drops a key. But he is confused why you woke him. What now?\n'
                self.add_object('key', 'bedroom')
        return msg


    def hit(self, subject, object):
        ok, msg = self.game_action('hit', 'wizard', 'bucket' , 'bedroom', False, False,
                    'The wizard awakens angrily and turns you into a toad. You lose.\n',
                    subject, object)
        if ok:
            self.end_game()
        return msg


    def unlock(self, subject, object):
        self.gate_unlocked, msg = \
            self.conditional_game_action('unlock', 'gate', 'key', 'garden',
                                    False, self.gate_unlocked, True,
                                'You unlock the gate! It\'s very dark outside...\n',
                                'The gate is locked! You need a key to get in!\n',
                                subject, object)
        if self.gate_unlocked:
            self.enable_route('garden', 'outside')
        return msg


if __name__ == "__main__":
    SpellGame().run_game()

