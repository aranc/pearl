import random
from util import extract_func_and_args

def ParametersFactory(strategy, template_parameters):
    if "rand" in strategy:
        f, n = extract_func_and_args(strategy)
        assert f == "rand"
        if n is None:
            n = 1
        res = []
        for _ in range(n):
            res.append([random.random() for _ in range(len(template_parameters))])
        return res

    res = strategy.split(",")
    assert len(res) == len(template_parameters)
    res = [float(_) for float in res]
    return [res]
