class Player(object):
    """Represents a player in a game of Secret Hitler."""
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.role = None
        self.party = None
        self.is_dead = False
        self.inspected_players = {}
