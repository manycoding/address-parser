import six


class EnumValue(object):
    def __init__(self, value, name=None):
        self.value = value
        self.name = name

    def __hash__(self):
        return self.value

    def __lt__(self, other):
        if isinstance(other, EnumValue):
            return self.value.__lt__(other.value)
        else:
            return self.value.__lt__(other)

    def __gt__(self, other):
        if isinstance(other, EnumValue):
            return self.value.__gt__(other.value)
        else:
            return self.value.__gt__(other)

    def __le__(self, other):
        if isinstance(other, EnumValue):
            return self.value.__le__(other.value)
        else:
            return self.value.__le__(other)

    def __ge__(self, other):
        if isinstance(other, EnumValue):
            return self.value.__ge__(other.value)
        else:
            return self.value.__ge__(other)

    def __ne__(self, other):
        if isinstance(other, EnumValue):
            return self.value.__ne__(other.value)
        else:
            return self.value.__ne__(other)

    def __eq__(self, other):
        if isinstance(other, EnumValue):
            return self.value.__eq__(other.value)
        else:
            return self.value.__eq__(other)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class EnumMeta(type):
    def __init__(self, name, bases, dict_):
        self.registry = self.registry.copy()
        self.name_registry = self.name_registry.copy()
        for k, v in six.iteritems(dict_):
            if isinstance(v, EnumValue) and v not in self.registry:
                if v.name is None:
                    v.name = k
                self.registry[v.value] = v
                self.name_registry[v.name] = v
        return super(EnumMeta, self).__init__(name, bases, dict_)

    def __iter__(self):
        return self.registry.itervalues()

    def __getitem__(self, key):
        return self.registry[key]


class Enum(six.with_metaclass(EnumMeta, object)):
    registry = {}
    name_registry = {}

    @classmethod
    def from_id(cls, value):
        try:
            return cls.registry[value]
        except KeyError:
            raise ValueError('Invalid value for {}: {}'.format(cls.__name__, value))

    @classmethod
    def from_string(cls, name):
        try:
            return cls.name_registry[name]
        except KeyError:
            raise ValueError('Invalid name for {}: {}'.format(cls.__name__, name))
