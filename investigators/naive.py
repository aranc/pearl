import random

class Investigator:
    def __init__(self, args):
        assert args is None

    def __call__(self, world, num_samples, question):
        x, y = question
        samples = [world() for _ in range(num_samples)]

        res = {0:0, 1:0}
        count = {0:0, 1:0}

        for sample in samples:
            x_val = sample[x]
            y_val = sample[y]

            count[x_val] += 1
            res[x_val] += y_val

        return (res[0]/count[0], res[1]/count[1])
