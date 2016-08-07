
class Room:
    def __init__(self, players=[], attendee=None):
        self.player_list = players
        self.attendee_list = []
        self.game = None

        if attendee:
            self.add_attendee(attendee)

    def add_attendee(self, attendee):
        self.attendee_list.append(attendee)

    def del_attendee(self, attendee):
        self.attendee_list.pop(attendee)

    def del_player(self, player):
        pass



