__author__ = 'adalekin'
import os.path
from ConfigParser import SafeConfigParser


class MemoryStorage(object):
    data = {}

    def set(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.data[k] = v

    def get(self, *args):
        r = {}
        for a in args:
            r[a] = self.data.get(a, None)

        if len(args) == 1:
            return r[args[0]]

        return r


class FileStorage(MemoryStorage):

    def __init__(self, path):
        self.path = path
        self._load_from_file(self.path)

    def set(self, **kwargs):
        super(FileStorage, self).set(**kwargs)
        self._save_to_file(self.path)

    def _load_from_file(self, *args):
        config = SafeConfigParser()
        config.read(args)

        for section in config.sections():
            for option in config.options(section):
                self.data[unicode(option)] = config.get(section, option)

    def _save_to_file(self, *args):
        section = "wrike"
        config = SafeConfigParser()
        config.add_section(section)

        for k, v in self.data.iteritems():
            config.set(section, k, unicode(v))

        for path in args:
            with open(path, "w") as fp:
                config.write(fp)