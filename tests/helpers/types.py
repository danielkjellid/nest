class AnyOrder:
    """
    A helper object that compers iterable content without caring about the order.
    """

    def __init__(self, iterable):
        self.iterable = iterable

    def __eq__(self, other):
        return set(self.iterable) == set(other)

    def __ne__(self, other):
        return not set(self.iterable) == set(other)

    def __repr__(self):
        return "<AnyOrder>"
