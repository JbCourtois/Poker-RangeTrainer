import itertools


class PeekableIter:
    def __init__(self, iterable):
        self.peeks = iter([])
        self.iterable = iter(iterable)

    def __iter__(self):
        while True:
            try:
                yield next(self)
            except StopIteration:
                return

    def __next__(self):
        try:
            return next(self.peeks)
        except StopIteration:
            self.peeks = iter([])
            return next(self.iterable)

    def peek(self, nb_items, all_items=False):
        items = [next(self) for _ in range(nb_items)]
        self.peeks = itertools.chain(items, self.peeks)
        return (items if all_items else items[-1])


class Cycle(PeekableIter):
    def __init__(self, iterable):
        super().__init__(itertools.cycle(iterable))
