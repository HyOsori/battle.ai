from server.User import User
from m_format import *
import json

class Attendee(User):
    def __init__(self, connect):
        User.__init__(self, connect)

    def notice_user_added(self, added_player):
        msg = {MSG: NOTICE+USER_ADDED, USER: added_player}
        json_msg = json.dumps(msg)
        self.conn().write(json_msg)
        pass

    def notice_user_removed(self, removed_player):
        msg = {MSG: NOTICE + USER_REMOVED, USER: removed_player}
        json_msg = json.dumps(msg)
        self.conn().write(json_msg)
        pass

    # What TO DO when Attendee exit, room send msg to Attendee



