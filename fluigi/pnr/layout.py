from fluigi.pnr.terminal import Terminal
from fluigi.pnr.svgdraw import SVGDraw
from cairo import SVGSurface
import networkx as nx
from typing import Optional, List
from fluigi.pnr.net import Net
from fluigi.pnr.cell import Cell
from pymint.mintdevice import MINTDevice
import sys
from enum import Enum
from fluigi.pnr.aarf import Cell as Obstacle
from fluigi.pnr.aarf import Router as AARFRouter
from fluigi.pnr.aarf import Vertex, Route


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
            if cell.x + cell.xdim > maxx:
                maxx = cell.x + cell.xdim

            if cell.y < miny:
                miny = cell.y
            if cell.y + cell.ydim > maxy:
                maxy = cell.y + cell.ydim

    def importMINTwithoutConstraints(self, device: Optional[MINTDevice]) -> None:

        self.__original_device = device

        for component in device.components:
            cell = Cell(component.ID, 0, 0, 1000, 1000)
            self.cells[cell.ID] = cell
            self.G.add_node(cell.ID)
            self.__direct_map.append(cell.ID)

        for connection in device.connections:
            source = Terminal()
            source_component = device.get_component(connection.source.component)
            coordinates = source_component.get_absolute_port_coordinates(
                connection.source.port
            )
            source.label = connection.source.port
            source.x = coordinates[0]
            source.y = coordinates[1]
            sinks = []
            for sink in connection.sinks:
                t = Terminal()
                t.label = sink.port
                sink_component = device.get_component(sink.component)
                coordinates = sink_component.get_absolute_port_coordinates(t.label)
                t.x = coordinates[0]
                t.y = coordinates[1]
                sinks.append(t)
            net = Net(connection.ID, source, sinks)
            self.nets[net.ID] = net
            for sink in connection.sinks:
                self.G.add_edge(connection.source.component, sink.component)

    def importMINTwithConstraints(self, device: MINTDevice) -> None:
        # TODO: Process the constraints
        raise Exception("Not Implemented")

    def get_cells(self) -> List[Cell]:
        return [self.cells[id] for id in list(self.cells)]

    def get_nets(self) -> List[Net]:
        return [self.nets[id] for id in list(self.nets)]

    def route_nets(self, router_type: RouterAlgorithms = RouterAlgorithms.AARF) -> None:
        obstacles = []
        # Step 1 - generate the obstacles from the components
        for cell in self.get_cells():
            obstacle = Obstacle()
            obstacle.x = cell.x
            obstacle.y = cell.y
            obstacle.x_span = cell.xdim
            obstacle.y_span = cell.ydim
            obstacles.append(obstacle)

        # Step 2 - generate the source and targets points for all the connections
        sources = []
        targets = []
        routes = []
        for net in self.get_nets():
            # Just get a single source and sink
            source_vertex = Vertex()

            source_vertex.x = net.source.x
            source_vertex.y = net.source.y

            sources.append(source_vertex)

            target_vertex = Vertex()
            target_vertex.x = net.sinks[0].x
            target_vertex.y = net.sinks[0].y

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

    def place_and_route_design()