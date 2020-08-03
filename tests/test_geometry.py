from pdddf.geometry import *


def test_flatten():
    assert (
        sim_bbox([[0, 0], (1, 1), (1, 1), (0, 1)], [[0, 0], (1, 0.5), (1, 0), (0, 0.5)])
        == 0.5
    )

    assert (
        sim_bbox([[0, 0], (1, 1), (1, 1), (0, 1)], [[0, 0], (1, 1), (1, 0), (0, 1)])
        == 1
    )

    assert (
        sim_bbox([[0, 0], (1, 1), (1, 1), (0, 1)], [[5, 5], (1, 1), (1, 5), (5, 1)])
        == 0
    )
