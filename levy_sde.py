class LevySDE(object):
    def __init__(self, f, x_0):
        self._f = f
        self._x_0 = x_0

    @property
    def f(self):
        return self._f

    def x_0(self):
        return self._x_0()


class BSLevySDE(LevySDE):
    def __init__(self, sigma, x_0):
        super(BSLevySDE, self).__init__(lambda x: sigma * x, x_0)
        self._sigma = sigma

    @property
    def sigma(self):
        return self._sigma


class LevySchema(object):
    def __init__(self, dt, T, levy_process, levy_sde, t=0., last_jump=0., state_in=0.):
        self._dt = dt
        self._t = t
        self._T = T
        self._levy_process = levy_process
        self._levy_sde = levy_sde
        self._last_jump = last_jump
        self._state_in = state_in

        self._is_state_jump = False
        self._n = 0
        self._state_in = self.levy_sde.x_0()
        self._t = 0.
        self._last_jump = 0.
        self._next_jump = self.levy_process.next_jump()

    @property
    def t(self):
        return self._t

    @property
    def dt(self):
        return self._dt

    @property
    def T(self):
        return self._T

    @property
    def levy_process(self):
        return self._levy_process

    @property
    def levy_sde(self):
        return self._levy_sde

    @property
    def last_jump(self):
        return self._last_jump

    @property
    def state_in(self):
        return self._state_in

    @property
    def n(self):
        return self._n

    @property
    def last_jump(self):
        return self._last_jump

    @property
    def next_jump(self):
        return self._next_jump

    @property
    def is_state_jump(self):
        return self._is_state_jump

    def __call__(self):
        drift = self.levy_process.drift
        volatility = self.levy_process.volatility
        gaussian = self.levy_process.gaussian
        f = self.levy_sde.f

        if self.t > self.T:
            self._t = self.T
            return self._state_in

        if self.next_jump > self.T:
            if self.t + self.dt <= self.T:
                self._state_in += f(self.state_in) * (drift * self.dt + pow(volatility * self.dt, 0.5) * gaussian())
                self._t += self.dt
                self._is_state_jump = False
                self._n += 1
                return self.state_in

            else:
                dt = self.T - self.t
                self._state_in += f(self.state_in) * (drift * dt + pow(volatility * dt, 0.5) * gaussian())
                self._t += dt
                self._is_state_jump = False
                self._n += 1
                return self.state_in

        else:
            if self.t + self.dt < self.next_jump:
                self._state_in += f(self.state_in) * (drift * self.dt + pow(volatility * self.dt, 0.5) * gaussian())
                self._t += self.dt
                self._is_state_jump = False
                self._n += 1
                return self.state_in

            else:
                continuous_part = f(self.state_in) * (
                    drift * (self.next_jump - self.t) + pow(volatility * (self.next_jump - self.t), 0.5) * gaussian())

                self._t = self.next_jump
                jump_size = self.levy_process.next_jump_size()
                self._state_in += continuous_part + jump_size

                self._last_jump = self.t
                self._n += 1
                self._is_state_jump = True

                self._next_jump += self.levy_process.next_jump()
                return self.state_in

    def restart(self):
        self._t = 0.
        self._last_jump = 0.
        self._state_in = 0.
        self._is_state_jump = False
        self._n = 0
        self._state_in = self.levy_sde.x_0()
        self._t = 0.
        self._last_jump = 0.
        self._next_jump = self.levy_process.next_jump()

    def generate(self, restart=True):
        while self.t < self.T:
            _ = self()

        value = self()

        if restart:
            self.restart()

        return value
