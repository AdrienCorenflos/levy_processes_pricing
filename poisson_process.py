from math import exp
from random import uniform


class PoissonProcess(object):
    def __init__(self, lambda_value, t):
        self._lambda_value = lambda_value
        self._t = t

    @property
    def lambda_value(self):
        return self._lambda_value

    @staticmethod
    def uniform():
        return uniform(0, 1)

    @property
    def t(self):
        return self._t

    def exponential(self):
        return exp(-self.lambda_value * self.t)

    def __call__(self):
        nb_events = 0
        product = self.uniform()
        while product > self.exponential():
            product *= self.uniform()
            nb_events += 1

        return nb_events
