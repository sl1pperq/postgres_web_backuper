from os import remove
from pyminizip import compress


class Archiver:
    def __init__(self, password, compression=5):
        self.__password = password
        self.__compression = compression

    def apply(self, filename):
        outfile = filename + '.zip'

        compress(filename, None, outfile, self.__password, self.__compression)
        remove(filename)

        return outfile

    def db_apply(self, filename):
        return self.apply(filename)

    def file_apply(self, filename):
        return self.apply(filename)
