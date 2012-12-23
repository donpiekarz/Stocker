import cPickle


class Stream(object):
    @staticmethod
    def next_event(filename):
        with open(filename, 'rU') as f:
            while True:
                try:
                    yield cPickle.load(f)
                except EOFError:
                    break

    def begin(self, filename):
        self.f = open(filename, 'wb')

    def end(self):
        self.f.close()

    def add_event(self, event):
        cPickle.dump(event, self.f, cPickle.HIGHEST_PROTOCOL)
