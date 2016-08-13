from math import exp


class Payoff(object):
    def __init__(self, levy_process):
        self._levy_process = levy_process

    @property
    def levy_process(self):
        return self._levy_process

    def __call__(self):
        raise NotImplementedError


class Call(Payoff):
    def __init__(self, levy_process, strike, rate_free, maturity):
        self._maturity = maturity
        self._rate_free = rate_free
        self._strike = strike
        super(Call, self).__init__(levy_process)

    @property
    def maturity(self):
        return self._maturity

    @property
    def strike(self):
        return self._strike

    @property
    def rate_free(self):
        return self._rate_free

    def __call__(self):
        value = exp(self.levy_process())
        strike = exp(self.strike)
        if value < strike:
            return 0.
        else:
            return exp(-self.rate_free * self.maturity) * (value - strike)
