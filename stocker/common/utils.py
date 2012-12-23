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

# source: http://code.activestate.com/recipes/68205-null-object-design-pattern/
class Null:
    """A class for implementing Null objects.

    This class ignores all parameters passed when constructing or 
    calling instances and traps all attribute and method requests. 
    Instances of it always (and reliably) do 'nothing'.

    The code might benefit from implementing some further special 
    Python methods depending on the context in which its instances 
    are used. Especially when comparing and coercing Null objects
    the respective methods' implementation will depend very much
    on the environment and, hence, these special methods are not
    provided here.
    """

    # object constructing

    def __init__(self, *args, **kwargs):
        "Ignore parameters."

    # object calling

    def __call__(self, *args, **kwargs):
        "Ignore method calls."
        return self

    # attribute handling

    def __getattr__(self, mname):
        "Ignore attribute requests."
        return self

    def __setattr__(self, name, value):
        "Ignore attribute setting."
        return self

    def __delattr__(self, name):
        "Ignore deleting attributes."
        return self

    # misc.

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"

