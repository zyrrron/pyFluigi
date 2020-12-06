from fluigi.parameters import (
    DEFAULT_MOVES_PER_TEMP_PER_MODULE,
    DEVICE_X_DIM,
    DEVICE_Y_DIM,
    LAMBDA,
)
from fluigi.pnr.sa.salayout import SALayout
from math import exp, floor
import random
import time
import sys

layout: SALayout = None
seed = 0
list_components = []
init_temp = sys.maxsize
rate_accept = 0.0
temp = 0
range_x = DEVICE_X_DIM / LAMBDA
range_y = DEVICE_Y_DIM / LAMBDA


class SAPlace:
    def __init__(self, salayout: SALayout) -> None:
        super().__init__()
        seed = random.seed(time.time_ns())
        layout = salayout
        rand = random.random()

    def cleanup(self) -> None:
        self.reset()
        list_components = []
        layout = None

    def reset(self) -> None:
        layout.clear()

    def place(self) -> None:
        self.init_place()
        self.init_temp()
        temp = init_temp

        while (
            temp >= 0.005 * layout.cur_cost / len(list_components)
            and layout.cur_cost > 2
        ):
            for i in range(len(list_components) * DEFAULT_MOVES_PER_TEMP_PER_MODULE):
                # TODO - Shouldnt this be a random component
                randc = list_components[i % len(list_components)]
                if random.random() > 0.5:
                    randx = int(range_x / 2 * random.random())
                else:
                    randx = -int(range_x / 2 * random.random())

                if random.random() > 0.5:
                    randy = int(range_x / 2 * random.random())
                else:
                    randy = -int(range_x / 2 * random.random())

                if random.random() > 0.5:
                    randx = 0
                else:
                    randy = 0

                layout.calc_prev_comp_overlap(randc)
                layout.calc_prev_comp_wirelength(randc)
                layout.grid.new_move(randc, randx, randy)
                layout.calculate_cost(randc)

                test = random.random()
                if layout.get_delta_cost() <= 0:
                    layout.grid.apply_move()
                    rate_accept += 1.0
                elif test < exp(-(layout.get_delta_cost() / temp)):
                    layout.grid.apply_move()
                    rate_accept += 1.0
                else:
                    layout.grid.undo_move()
                    layout.undo_update_cost()

            rate_accept = rate_accept / float(
                len(list_components) * DEFAULT_MOVES_PER_TEMP_PER_MODULE
            )

            range_x = int(floor(range_x) * (1.0 - 0.44 + rate_accept))
            range_y = int(floor(range_y) * (1.0 - 0.44 + rate_accept))

            if range_x >= DEVICE_X_DIM / LAMBDA:
                range_x = DEVICE_X_DIM / LAMBDA

            if range_y >= DEVICE_Y_DIM / LAMBDA:
                range_y = DEVICE_Y_DIM / LAMBDA

            if rate_accept > 0.96:
                temp = 0.5 * temp
            elif rate_accept <= 0.96 and rate_accept > 0.8:
                temp = 0.9 * temp
            elif rate_accept <= 0.8 and rate_accept > 0.15:
                temp = 0.95 * temp
            else:
                temp = 0.8 * temp
            print("-> Temp = {}".format(temp))

        print("Final Temp = {}".format(temp))
        print("Overlap = {}".format(layout.calculate_overlap()))

    def init_place(self):
        raise NotImplementedError()

    def init_temp(self):
        raise NotImplementedError()
