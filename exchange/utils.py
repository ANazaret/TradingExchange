def clean_string(string):
    accepted = "abcdefghijklmnopqrstuvwyyz_-'1234567890."
    return ''.join(filter(lambda x: x in accepted, string.lower().replace(' ', '_')))


def add_id(field):
    def decorator(func):
        def aux(*args, **kwargs):
            func(*args, **kwargs)
            self = args[0]
            self.id = clean_string(self.__getattribute__(field))

        return aux

    return decorator


def check_dict_fields(d, fields):
    for f in fields:
        if f not in d:
            return False
    return True


def check_data_errors(d: dict) -> bool:
    for f, v in d.items():
        if f == 'side':
            if v not in ['ask', 'bid']:
                raise KeyError("%s is not a valid side" % str(v))

        if f == 'price':
            if type(v) != float and type(v) != int:
                raise Exception
            if v <= 0:
                raise Exception

        if f == 'volume':
            if type(v) != int:
                raise Exception
            if v <= 0:
                raise Exception

    return True
