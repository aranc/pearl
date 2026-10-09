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

        res_x_z = {0:0, 1:0}
        count_x_z = {0:0, 1:0}
        res_z_y = {0:0, 1:0}
        count_z_y = {0:0, 1:0}

        for sample in samples:
            x_val = sample[x]
            y_val = sample[y]
            z_val = sample[z]

            count_x_z[x_val] += 1
            res_x_z[x_val] += z_val

            count_z_y[z_val] += 1
            res_z_y[z_val] += y_val

        x_causes_z = res_x_z[1] / count_x_z[1]
        not_x_causes_z = res_x_z[0] / count_x_z[0]

        z_causes_y = res_z_y[1] / res_z_y[1]
        not_z_causes_y = res_z_y[0] / res_z_y[0]
        
        return (not_x_causes_z * z_causes_y + not_x_causes_not_z * not_z_causes_y)
                x_causes_z * z_causes_y + x_causes_not_z * not_z_causes_y)
