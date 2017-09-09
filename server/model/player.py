import time

class Player(object):
    def __init__(self, name, encrypted_password):
        self.name = name
        self.password = encrypted_password
        self.created_at = int(time.time() * 1000)
        self.game_info_list = []
        self.image_url = ""


