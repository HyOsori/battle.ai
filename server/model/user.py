class User(object):
    def __init__(self, name, encrypted_password, *, image_url=None, message=None):
        self.name = name
        self.password = encrypted_password
        self.image_url = image_url
        self.message = message
