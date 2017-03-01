"""
structure description

all json format var keep convention Camel
ex) findViewById ...

[user]
{
  _id: (string),
  name: (string),
  password: (string),
  imageUrl: (string), -- optional
  gitHubId: (string) -- optional
}
* _id: key value that identifies user in server
* name: name that user choose
* password: password ...

[game_log]
{
  game_id: (string),
  winner: [(string), (string) ..],
  loser: [(string), (string), ..],
  drawer: [(string), (string) ...]
}

* game_id: key value that identifies game in server
* winner: winner's _id list
* loser: loser's _id list
* drawers: drawer's _id list

"""

import json


class DBHandler(object):
    def __init__(self):
        self.conn = None
        self.db = None

        self.users = None
        self.game_log_list = None
        pass

    def insert_user(self, user):
        pass
    pass

dbh = DBHandler()
print(json.dumps(dbh.__dict__))


