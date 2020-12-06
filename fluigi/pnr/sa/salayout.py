from fluigi.pnr.sa.layoutgrid import LayoutGrid
from fluigi.parameters import AREA_PENALTY, OVERLAP_PENALTY, WIRE_PENALTY
from fluigi.pnr.place_and_route import PlacementCell as CCell, Terminal as CTerminal
from fluigi.pnr.place_and_route import Net as CNet
from fluigi.pnr.layout import Layout
import sys


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
    raise NotImplementedError()


def calc_position(net: CNet) -> int:
    raise NotImplementedError()


cur_top_edge = 0
cur_right_edge = 0
cur_bottom_edge = 0
cur_left_edge = 0

old_cost = 0
old_area = 0
old_overlap = 0
old_wirelength = 0

cur_cost = 0
cur_area = 0
cur_overlap = 0
cur_wirelength = 0

pre_move_comp_overlap = 0
pre_move_wirelength = 0


class SALayout(Layout):
    def __init__(self) -> None:
        super().__init__()
        self.grid: LayoutGrid = LayoutGrid()

    def calc_init_cost(self) -> int:
        old_cost = cur_cost
        old_overlap = cur_overlap
        old_wirelength = cur_wirelength
        cur_area = self.calculate_area()

        cur_overlap = self.calculate_overlap()
        cur_wirelength = self.calculate_wirelength()
        cur_cost = (
            cur_wirelength * WIRE_PENALTY
            + cur_area * AREA_PENALTY
            + cur_overlap * OVERLAP_PENALTY
        )

        return cur_cost

    def calculate_cost(self, randc: CCell) -> int:
        old_cost = cur_cost
        old_overlap = cur_overlap
        old_wirelength = cur_wirelength
        cur_area = self.calculate_area()

        self.cur_overlap = (
            old_overlap - pre_move_comp_overlap + self.calculate_comp_overlap(randc)
        )
        self.cur_cost = (
            cur_wirelength * WIRE_PENALTY
            + cur_area * AREA_PENALTY
            + cur_overlap * OVERLAP_PENALTY
        )

        return self.cur_cost

    def get_delta_cost(self) -> int:
        return cur_cost - old_cost

    def undo_update_cost(self) -> float:
        cur_area = old_area
        cur_overlap = old_overlap
        cur_wirelength = old_wirelength
        cur_cost = old_cost
        return cur_cost

    def calculate_wirelength(self) -> int:
        wire_sum = 0
        for net in list(self.nets.values()):
            source_terminal = net.source_terminal
            for sink_terminal in net.sink_terminals:
                m_dist = manhattan_dist(source_terminal, sink_terminal)
                penalty = calc_position(net)
                wire_sum += m_dist + OVERLAP_PENALTY / 2 * penalty
        return wire_sum

    def calc_prev_comp_wirelength(self, c: CCell) -> None:
        prev_move_wirelength = self.calc_comp_wirelength(c)

    def calc_comp_wirelength(self, c: CCell) -> None:
        wire_sum = 0
        # TODO : include the graph into the data structure
        raise NotImplementedError()

    def calc_prev_comp_overlap(self, randc: CCell) -> None:
        pre_move_comp_overlap = self.calculate_comp_overlap(randc)

    def calculate_area(self) -> int:
        """[summary]

        Returns:
            int: [description]
        """

        min_left = min_top = sys.maxsize
        max_right = max_bottom = 0

        for cell in list(self.cells.values()):
            if left_edge(cell) < min_left:
                min_left = left_edge(cell)
            if right_edge(cell) > max_right:
                max_right = right_edge(cell)
            if top_edge(cell) < min_top:
                min_top = top_edge(cell)
            if bottom_edge(cell) > max_bottom:
                max_bottom = bottom_edge(cell)

        self.cur_bottom_edge = max_bottom
        self.cur_top_edge = min_top
        self.cur_left_edge = min_left
        self.cur_right_edge = max_right

        return (max_bottom - min_top) * (max_right - min_left)

    # TODO - RENAME THIS LATER ON
    def calculate_overlap(self) -> int:
        overlap_sum = 0
        cells = list(self.cells.values())
        for i in range(len(cells)):
            c1 = cells[i]
            for j in range(i + 1, len(cells)):
                c2 = cells[j]
                overlap_sum += overlap_area(c1, c2)

        return overlap_sum

    def calculate_comp_overlap(self, randC) -> int:
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()
