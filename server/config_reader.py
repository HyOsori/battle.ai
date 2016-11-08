class ConfigReader:

    def __init__(self):
        self.f = open("config", "r")

    def read(self):
        config_value = {}

        for line in self.f:
            if line[0] == '#' or line[0] == '\n':
                continue

            tmp = line.split('=')
            print tmp
            if len(tmp) == 2:
                config_value[tmp[0]] = int(tmp[1])

        return config_value
