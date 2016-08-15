from random import gauss as gaussian


class LevyMeasure(object):
    def __init__(self, is_finite=True):
        self._is_finite = is_finite

    @property
    def is_finite(self):
        return self._is_finite


class FiniteLevyMeasure(LevyMeasure):
    def __init__(self, integral_value):
        super(FiniteLevyMeasure, self).__init__(True)
        self._integral_value = integral_value

    @property
    def integral_value(self):
        return self._integral_value

    @property
    def lambda_value(self):
        raise NotImplementedError

    @property
    def z(self):
        raise NotImplementedError


class MertonMeasure(FiniteLevyMeasure):
    def __init__(self, mean, sigma, lambda_value):
        super(MertonMeasure, self).__init__(lambda_value)
        self._mean = mean
        self._sigma = sigma
        self._lambda_value = lambda_value

    @property
    def lambda_value(self):
        return self._lambda_value

    @property
    def sigma(self):
        return self._sigma

    @property
    def mean(self):
        return self._mean

    def z(self):
        return gaussian(self.mean, self.sigma)
