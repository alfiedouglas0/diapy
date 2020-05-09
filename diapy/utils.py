import os.path


def does_file_exist(path: str) -> bool:
    return os.path.isfile(path)


class classproperty(property):
    """ From https://stackoverflow.com/a/7864317/5084488 """

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
