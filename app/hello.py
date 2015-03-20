class OO(object):
    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value):
        self._foo = value

o = OO(foo=1)
print o.foo