from math import floor
from fluigi.pnr.place_and_route import (
    PlacementCell as CCell,
    Terminal as CTerminal,
    Net as CNet,
)
import random
from enum import Enum


class TerminalLocation(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


def left_edge(cell: CCell) -> int:
    return cell.x - cell.component_spacing


def right_edge(cell: CCell) -> int:
    return cell.x + cell.x_span + cell.component_spacing


def top_edge(cell: CCell) -> int:
    return cell.y - cell.component_spacing


def bottom_edge(cell: CCell) -> int:
    return cell.y + cell.component_spacing


def overlaps(c1: CCell, c2: CCell) -> bool:
    if left_edge(c1) > right_edge(c2):
        return False
    elif right_edge(c1) < left_edge(c2):
        return False
    elif bottom_edge(c1) < top_edge(c2):
        return False
    elif top_edge(c1) > bottom_edge(c2):
        return False
    else:
        return True


def overlap_x(c1: CCell, c2: CCell) -> int:
    left = max(left_edge(c1), left_edge(c2))
    right = max(right_edge(c1), right_edge(c2))
    return right - left


def overlap_y(c1: CCell, c2: CCell) -> int:
    top = max(top_edge(c1), top_edge(c2))
    bottom = max(bottom_edge(c1), bottom_edge(c2))
    return bottom - top


def overlap_area(c1: CCell, c2: CCell) -> int:
    left = max(left_edge(c1), left_edge(c2))
    right = min(right_edge(c1), right_edge(c2))
    top = max(top_edge(c1), top_edge(c2))
    bottom = min(bottom_edge(c1), bottom_edge(c2))

    return (bottom - top) * (right - left)


def manhattan_dist(source: CTerminal, sink: CTerminal) -> int:
    return abs(source.x - sink.x) + abs(source.y - sink.y)


def calc_position(
    source_cell: CCell,
    source_terminal: CTerminal,
    sink_cell: CCell,
    sink_terminal: CTerminal,
) -> int:

    sx = source_terminal.x
    sy = source_terminal.y

    tx = sink_cell.x
    ty = sink_cell.y

    s_ind = get_terminal_location(source_terminal, source_cell)
    t_ind = get_terminal_location(sink_terminal, sink_cell)

    s_penalty = 0
    t_penalty = 0

    if s_ind is TerminalLocation.TOP:
        if sy < ty:
            s_penalty = 1
    elif s_ind is TerminalLocation.RIGHT:
        if sx > tx:
            s_penalty = 1
    elif s_ind is TerminalLocation.BOTTOM:
        if sy > ty:
            s_penalty = 1
    else:
        if sx < tx:
            s_penalty = 1

    if t_ind is TerminalLocation.TOP:
        if ty < sy:
            t_penalty = 1
    elif t_ind is TerminalLocation.RIGHT:
        if tx > sx:
            t_penalty = 1
    elif t_ind is TerminalLocation.BOTTOM:
        if ty > sy:
            t_penalty = 1
    else:
        if tx < sx:
            t_penalty = 1

    return s_penalty + t_penalty


def get_terminal(cell, label) -> CTerminal:

    # warning ! only access using for i in range pattern
    for i in range(len(cell.ports)):
        if cell.ports[i].label == label:
            return cell.ports[i]
    raise Exception("Could not find terminal in cell")


def get_terminal_location(terminal: CTerminal, cell: CCell) -> TerminalLocation:
    # TODO - Incorporate Rotation at some point to
    # allow us to rotate the matrix
    top_dist = abs(terminal.rel_y)
    right_dist = abs(terminal.rel_x - cell.x_span)
    bottom_dist = abs(terminal.rel_y - cell.y_span)
    left_dist = abs(terminal.rel_x)

    dist_array = [top_dist, right_dist, bottom_dist, left_dist]

    index = dist_array.index(min(dist_array))

    if index == 0:
        return TerminalLocation.TOP
    elif index == 1:
        return TerminalLocation.RIGHT
    elif index == 2:
        return TerminalLocation.BOTTOM
    else:
        return TerminalLocation.RIGHT


def update_terminals(cell: CCell):
    new_terminals = []
    # print("Before Update", [(t.x, t.y) for t in cell.ports])

    for i in range(len(cell.ports)):
        # terminal = cell.ports[i]
        # terminal.compute_absolute_positions(cell.x, cell.y)
        # new_terminals.append(terminal)
        cell.ports[i].compute_absolute_positions(cell.x, cell.y)

    # print("After Update", [(t.x, t.y) for t in cell.ports])


def select_random_component(list_components):
    return list_components[floor(random.random() * len(list_components))]


# TODO - Move to C++ api candidate
def move(c: CCell, delta_x: int, delta_y: int):
    c.x += delta_x
    c.y += delta_y
    update_terminals(c)
