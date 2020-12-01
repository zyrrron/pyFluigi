from fluigi.pnr.svgdraw import SVGDraw
from cairo import SVGSurface
import networkx as nx
from typing import Optional, List
from pymint.mintdevice import MINTDevice
import sys
from enum import Enum

from fluigi.pnr.place_and_route import Terminal as CTerminal
from fluigi.pnr.place_and_route import Net as CNet
from fluigi.pnr.place_and_route import PlacementCell as CCell
from fluigi.pnr.place_and_route import Placer as CPlacer

# from fluigi.pnr.aarf import Cell as Obstacle
# from fluigi.pnr.aarf import Router as AARFRouter
# from fluigi.pnr.aarf import Vertex, Route


class RouterAlgorithms(Enum):
    AARF = 0
    GRID = 1


class Layout:
    def __init__(self) -> None:
        self.cells = dict()
        self.nets = dict()
        self.G = nx.MultiDiGraph()
        self.__original_device = None
        self.__direct_map = []

    def applyLayout(self):
        device = self.__original_device
        for ID in self.__direct_map:
            component = device.get_component(ID)
            cell = self.cells[ID]
            component.params.set_param("position", [cell.x, cell.y])

    def ensureLegalCoordinates(self):
        # Make sure all the cell coordinates are positive
        minx = sys.maxsize
        miny = sys.maxsize
        maxx = -sys.maxsize
        maxy = -sys.maxsize

        for cell in [self.cells[id] for id in list(self.cells)]:
            if cell.x < minx:
                minx = cell.x
            if cell.x + cell.x_span > maxx:
                maxx = cell.x + cell.x_span

            if cell.y < miny:
                miny = cell.y
            if cell.y + cell.y_span > maxy:
                maxy = cell.y + cell.y_span

    def importMINTwithoutConstraints(self, device: MINTDevice) -> None:

        self.__original_device = device

        pcells = []

        for component in device.components:
            terminals = []
            for port in component.ports:
                t = CTerminal(port.label, port.x, port.y)
                terminals.append(t)

            if component.params.exists("componentSpacing"):
                component_spacing = component.params.get_param("componentSpacing")
            else:
                component_spacing = 1000  # Some random value
            pcell = CCell(
                component.ID,
                component.xpos,
                component.ypos,
                component.xspan,
                component.yspan,
                component_spacing,
                terminals,
            )

            pcells.append(pcell)
            self.cells[pcell.id] = pcell

        for connection in device.connections:
            id = connection.ID
            source = self.cells[connection.source.component]
            source_terminal = None
            if connection.source.port is not None:
                # Get C Terminal for this
                source_terminal = source.get_terminal(connection.source.port)

            sink_cells = []
            sink_terminals = []
            for sink in connection.sinks:
                pcell = self.cells[sink.component]
                sink_cells.append(pcell)
                if sink.port is not None:
                    t = pcell.get_terminal(sink.port)
                    sink_terminals.append(t)
                else:
                    sink_terminals.append(None)

            # cnet.sinks = sink_cells
            # cnet.sink_terminals = sink_terminals

            cnet = CNet()
            cnet.id = id
            cnet.source = source
            cnet.source_terminal = source_terminal

            # TODO - Figure out how to fix the interface later
            for sink_cell in sink_cells:
                cnet.sinks.append(sink_cell)

            # TODO - Figure out how to fix the interface later
            for sink_terminal in sink_terminals:
                cnet.sink_terminals.append(sink_terminal)

            self.nets[cnet.id] = cnet

    def importMINTwithConstraints(self, device: MINTDevice) -> None:
        # TODO: Process the constraints
        raise Exception("Not Implemented")

    # def get_cells(self) -> List[Cell]:
    #     return [self.cells[id] for id in list(self.cells)]

    # def get_nets(self) -> List[Net]:
    #     return [self.nets[id] for id in list(self.nets)]

    def route_nets(self, router_type: RouterAlgorithms = RouterAlgorithms.AARF) -> None:
        obstacles = []
        # Step 1 - generate the obstacles from the components
        for cell in self.get_cells():
            obstacle = Obstacle()
            obstacle.x = cell.x
            obstacle.y = cell.y
            obstacle.x_span = cell.x_span
            obstacle.y_span = cell.y_span
            obstacles.append(obstacle)

        # Step 2 - generate the source and targets points for all the connections
        sources = []
        targets = []
        routes = []
        for net in self.get_nets():
            # Just get a single source and sink
            source_vertex = Vertex()

            source_vertex.x = net.source_terminal.x
            source_vertex.y = net.source_terminal.y

            sources.append(source_vertex)

            target_vertex = Vertex()
            target_vertex.x = net.sink_terminals[0].x
            target_vertex.y = net.sink_terminals[0].y

            targets.append(target_vertex)
            # r = Route(net.ID, source_vertex, target_vertex)
            # routes.append(r)
        # Step 3 - Do the routing
        router = AARFRouter(obstacles, 100, 200)
        routes = router.route(sources, targets)

        # TODO - New API
        # router = AARFRouter(obstacles)
        # router.route(routes)

        print(routes)
        print("Routed route:")
        for route in routes:
            print(route)

        pass

    def place_and_route_design(self):
        cells = list(self.cells.values())
        nets = list(self.nets.values())
        constraints = []
        placer = CPlacer(cells, nets, constraints)
        placer.place_and_route()
