class InfiniteLoopError(Exception):

    def __init__(self, number):
        self.number = number

    def __str__(self):
        return 'All the numbers with digits {0} are used.'.format(self.number)
