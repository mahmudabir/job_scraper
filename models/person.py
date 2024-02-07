class Person:
    def __init__(self, name=None, url=None, age=None):
        self.name = name
        self.url = url
        self.age = age

    def __keys__(self):
        dict_keys = Person().__dict__.keys()
        key_list = list(dict_keys)
        return key_list
