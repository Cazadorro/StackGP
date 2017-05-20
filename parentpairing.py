#!/bin/bash

import random


def stochastic_pairing(selected, pair_size):
    assert len(selected) % pair_size == 0, \
        "ERROR, selected size should be a multiple of the pair size"
    random.shuffle(selected)
    return [tuple(selected[x:x + pair_size]) for x in
            range(0, len(selected), pair_size)]
