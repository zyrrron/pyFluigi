from fluigi.pnr.place_and_route import Terminal
from typing import List


class Net:
    def __init__(self, ID, source, sinks) -> None:
        self.ID = ID
        self.source: Terminal = source
        self.sinks: List[Terminal] = sinks
        self.waypoints: List[List[int]] = []

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Net) and o.ID == self.ID:
            return True
        else:
            return False
