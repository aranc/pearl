#backdoor casual investigator
import random

class Investigator:
    def __init__(self, args):
        assert args is not None
        self.args = args

    def __call__(self, world, num_samples, question):
        x, y = question
        z = self.args

        samples = [world() for _ in range(num_samples)]

        res0 = {0:0, 1:0}
        count0 = {0:0, 1:0}
        res1 = {0:0, 1:0}
        count1 = {0:0, 1:0}
        countz = 0

        for sample in samples:
            x_val = sample[x]
            y_val = sample[y]
            z_val = sample[z]

            if not z_val:
                count0[x_val] += 1
                res0[x_val] += y_val
            else:
                count1[x_val] += 1
                res1[x_val] += y_val
                countz += 1

        z_prop = countz / num_samples

        return (res0[0]/count0[0] * (1-z_prop) + res1[0]/count1[0] * z_prop,
                res0[1]/count0[1] * (1-z_prop) + res1[1]/count1[1] * z_prop)
