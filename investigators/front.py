#frontdoor casual investigator
import random

class Investigator:
    def __init__(self, args):
        assert args is not None
        self.args = args

    def __call__(self, world, num_samples, question):
        x, y = question
        z = self.args

        samples = [world() for _ in range(num_samples)]

        count_x = 0
        count_z_x = 0
        count_not_z_x = 0
        count_not_z_not_x = 0
        count_z_not_x = 0
        count_y_cond_x_z = 0
        count_y_cond_not_x_z = 0
        count_y_cond_x_not_z = 0
        count_y_cond_not_x_not_z = 0

        for sample in samples:
            x_val = sample[x]
            y_val = sample[y]
            z_val = sample[z]

            count_x += x_val
            count_z_x += z_val * x_val
            count_not_z_x += (1-z_val) * x_val
            count_not_z_not_x += (1-z_val) * (1-x_val)
            count_z_not_x += z_val * (1-x_val)

            if x_val * z_val:
                count_y_cond_x_z += y_val
            if (1-x_val) * z_val:
                count_y_cond_not_x_z += y_val
            if x_val * (1-z_val):
                count_y_cond_x_not_z += y_val
            if (1-x_val) * (1-z_val):
                count_y_cond_not_x_not_z += y_val

        p_x = {}
        p_x[1] = count_x / num_samples
        p_x[0] = 1 - p_x[1]

        p_z_x = {}
        p_z_x[(1,1)] = count_z_x/num_samples
        p_z_x[(0,1)] = count_not_z_x/num_samples
        p_z_x[(1,0)] = count_z_not_x/num_samples
        p_z_x[(0,0)] = count_not_z_not_x/num_samples

        p_y_cond_x_z = {}
        p_y_cond_x_z[(1,1)] = count_y_cond_x_z / count_z_x
        p_y_cond_x_z[(0,1)] = count_y_cond_not_x_z / count_z_not_x
        p_y_cond_x_z[(1,0)] = count_y_cond_x_not_z / count_not_z_x
        p_y_cond_x_z[(0,0)] = count_y_cond_not_x_not_z / count_not_z_not_x

        b = 0
        for z in (0, 1):
            t = 0
            for x in (0, 1):
                t += p_y_cond_x_z[(x, z)] * p_x[x]
            b += p_z_x(z, 1) * t

        a = 0
        for z in (0, 1):
            t = 0
            for x in (0, 1):
                t += p_y_cond_x_z[(x, z)] * p_x[x]
            a += p_z_x(z, 0) * t

        return a, b
