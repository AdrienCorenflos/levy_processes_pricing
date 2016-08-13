from math import log, exp
from .levy_measures import MertonMeasure
from .levy_processes import MertonProcess
from .levy_sde import BSLevySDE, LevySchema
from .payoffs import Call


def my_x_0():
    return log(100.)


def monte_carlo(random_variable, n):
    _sum = sum(random_variable() for _ in range(n))
    return _sum / n


merton_measure = MertonMeasure(0.1, 0.2, 1.)
merton_process = MertonProcess(0.2 * 0.2, 0.05, 0.5, merton_measure, my_x_0())

bs_levy_sde = BSLevySDE(0.2, my_x_0)
bs_merton_levy_schema = LevySchema(0.01, 0.5, merton_process, bs_levy_sde, 0.)
call = Call(bs_merton_levy_schema.generate, log(100.), 0.05, 0.5)

print(exp(bs_merton_levy_schema.generate()))

print(monte_carlo(call, 10000))
