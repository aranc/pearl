import random

class Investigator:
    def __init__(self, args):
        assert args is None

    def __call__(self, world, num_samples, question):
        x, y = question

        res = {0:0, 1:0}
        count = {0:0, 1:0}

        for i in range(num_samples):
            x_val = random.choice([0, 1])
            sample = world(do={x:x_val})
            y_val = sample[y]

            count[x_val] += 1
            res[x_val] += y_val

        return (res[0]/count[0], res[1]/count[1])
