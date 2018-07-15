def clean_string(string):
    accepted = "abcdefghijklmnopqrstuvwyyz_-'1234567890"
    return ''.join(filter(lambda x: x in accepted, string.lower().replace(' ', '_')))


def add_id(field):
    def decorator(func):
        def aux(*args, **kwargs):
            func(*args, **kwargs)
            self = args[0]
            self.id = clean_string(self.__getattribute__(field))

        return aux

    return decorator
