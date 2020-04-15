import networkx as nx

from .net import Net
from .cell import Cell
from pyMINT.mintdevice import MINTDevice


class Layout:

    def __init__(self) -> None:
        self.cells = dict()
        self.nets = dict()
        self.G = nx.MultiDiGraph()

    def importMINTwithoutConstraints(self, device: MINTDevice) -> None:
        for component in device.components:
            cell = Cell(component.ID, 0, 0, 1000, 1000)
            self.cells[cell.ID] = cell
            self.G.add_node(cell.ID)
        
        for connection in device.connections:
            net = Net(connection.ID, connection.source, connection.sinks)
            self.nets[net.ID] = net
            for sink in connection.sinks:
                self.G.add_edge(connection.source.component, sink.component)

    def importMINTwithConstraints(self, device: MINTDevice) -> None:
        #TODO: Process the constraints
        raise Exception('Not Implemented')
