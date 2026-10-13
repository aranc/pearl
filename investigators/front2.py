#frontdoor casual investigator
import random
from utils import safediv

class Investigator:
    def __init__(self, args):
        assert args is not None
        self.args = args

    def __call__(self, world, num_samples, question):
        x, y = question
        z = self.args

        samples = [world() for _ in range(num_samples)]

        count_x = 0
        count_z = 0
        count_z_x = 0
        count_not_z_x = 0
        count_not_z_not_x = 0
        count_z_not_x = 0
        count_y_cond_z = 0
        count_y_cond_not_z = 0

        for sample in samples:
            x_val = sample[x]
            y_val = sample[y]
            z_val = sample[z]

            count_x += x_val
            count_z_x += z_val * x_val
            count_not_z_x += (1-z_val) * x_val
            count_not_z_not_x += (1-z_val) * (1-x_val)
            count_z_not_x += z_val * (1-x_val)

            count_z += z_val
            if z_val:
                count_y_cond_z += y_val
            else:
                count_y_cond_not_z += y_val

        p_x = {}
        p_x[1] = count_x / num_samples
        p_x[0] = 1 - p_x[1]

        p_z = {}
        p_z[1] = count_z / num_samples
        p_z[0] = 1 - p_z[1]

        p_z_x = {}
        p_z_x[(1,1)] = safediv(count_z_x,num_samples)
        p_z_x[(0,1)] = safediv(count_not_z_x,num_samples)
        p_z_x[(1,0)] = safediv(count_z_not_x,num_samples)
        p_z_x[(0,0)] = safediv(count_not_z_not_x,num_samples)

        p_y_cond_z = {}
        p_y_cond_z[1] = count_y_cond_z / count_z
        p_y_cond_z[0] = 1 - p_y_cond_x_z[1]

        p_z_cond_x = {}
        for x in (0, 1):
            for z in (0, 1):
                p_z_cond_x[(z, x)] = p_z_x[(z, x)] / p_x[x]

        p_not_z_cond_x = {}
        p_not_z_cond_x[1] = 1 - p_z_cond_x[1]
        p_not_z_cond_x[0] = 1 - p_z_cond_x[0]

        b = p_z_cond_x[1] * p_y_cond_z[1] + p_not_z_cond_x[1] * p_y_cond_z[0]
        a = p_z_cond_x[0] * p_y_cond_z[1] + p_not_z_cond_x[0] * p_y_cond_z[0]

        return a, b
