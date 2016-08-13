class LevyProcess(object):
    def __init__(self, volatility, drift, t, levy_measure):
        self._vol = volatility
        self._drift = drift
        self._t = t
        self._levy_measure = levy_measure
        self._gaussian = gaussian

    def origin(self):
        raise NotImplementedError

    def next_jump(self):
        integral_value = self.levy_measure.integral_value
        return expovariate(integral_value)

    def gaussian(self):
        return gaussian(0., 1.)

    @property
    def t(self):
        return self._t

    @property
    def drift(self):
        return self._drift

    @property
    def volatility(self):
        return self._vol

    @property
    def levy_measure(self):
        return self._levy_measure

    def next_jump_size(self):
        raise NotImplementedError

    def __call__(self):
        raise NotImplementedError


class MertonProcess(LevyProcess):
    def __init__(self, volatility, rate_free, t, merton_measure, origin):
        ksi = 1. - exp(merton_measure.mean + 0.5 * merton_measure.sigma ** 2.)
        drift = rate_free - 0.5 * volatility + merton_measure.lambda_value * ksi
        super(MertonProcess, self).__init__(volatility,
                                            drift,
                                            t,
                                            merton_measure)

        self._origin = origin

    def uniform(self):
        return uniform()

    @property
    def origin(self):
        return self._origin

    def next_jump_size(self):
        return self.levy_measure.z()

    def __call__(self):
        lambda_value = self.levy_measure.lambda_value
        poisson_process = PoissonProcess(lambda_value, self.t)

        nb_jumps = poisson_process()

        jumps_size = sum([self.next_jump_size() for _ in range(nb_jumps)])

        diffusion_value = self.drift * self.t + pow(self.volatility * self.t, 0.5) * self.gaussian()

        return self.origin + jumps_size + diffusion_value
