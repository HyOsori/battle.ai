class Player(object):
    def __init__(self, name, encrypted_password):
        self.name = name
        self.password = encrypted_password
        self.created_at =""
        self.game_info_list = []
