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

from fluigi.pnr.place_and_route import Cell as Obstacle
from fluigi.pnr.place_and_route import Router as AARFRouter
from fluigi.pnr.place_and_route import Vertex, Route


class RouterAlgorithms(Enum):
    AARF = 0
    GRID = 1


def get_terminal(cell, label) -> CTerminal:
    for terminal in cell.ports:
        if terminal.label == label:
            return terminal
    raise Exception("Could not find terminal in exception")


class Layout:
    def __init__(self) -> None:
        self.cells = dict()
        self.nets = dict()
        self.G = nx.MultiDiGraph()
        self.__original_device = None
        self.__direct_map = []

    def applyLayout(self):
        device = self.__original_device
        for ID in self.cells.keys():
            component = device.get_component(ID)
            cell = self.cells[ID]
            component.params.set_param("position", [cell.x, cell.y])

        for ID in self.nets.keys():
            connection = device.get_connection(ID)
            net = self.nets[ID]
            for route in net.routes:
                path = []
                for vertex in route.waypoints:
                    path.append((vertex.x, vertex.y))

                connection.add_waypoints_path(path)

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
                print("Before Update: ({}, {})".format(t.x, t.y))
                t.compute_absolute_positions(component.xpos, component.ypos)
                print("After Update: ({}, {})".format(t.x, t.y))

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
                try:
                    source_terminal = get_terminal(source, connection.source.port)
                except Exception:
                    print(
                        "Could not find Terminal for source port: {} {} for connection: {}".format(
                            source.id, connection.source.port, id
                        )
                    )

            sink_cells = []
            sink_terminals = []
            for sink in connection.sinks:
                pcell = self.cells[sink.component]
                sink_cells.append(pcell)
                if sink.port is not None:
                    try:
                        t = get_terminal(pcell, sink.port)
                        sink_terminals.append(t)
                    except Exception:
                        print(
                            "Could not find Terminal for source port: {} for connection: {}".format(
                                source.id, id
                            )
                        )

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

    def route_nets(self, router_type: RouterAlgorithms = RouterAlgorithms.AARF) -> None:
        obstacles = []
        # Step 1 - generate the obstacles from the components
        for cell in list(self.cells.values()):
            obstacle = Obstacle()
            obstacle.x = cell.x
            obstacle.y = cell.y
            obstacle.x_span = cell.x_span
            obstacle.y_span = cell.y_span
            obstacles.append(obstacle)

        # Step 2 - generate the source and targets points for all the connections
        routes = []
        for net in list(self.nets.values()):
            # Just get a single source and sink
            source_vertex = Vertex()

            source_vertex.x = net.source_terminal.x
            source_vertex.y = net.source_terminal.y

            for sink_terminal in net.sink_terminals:
                target_vertex = Vertex()
                target_vertex.x = sink_terminal.x
                target_vertex.y = sink_terminal.y

                route = Route(
                    net.id,
                    source_vertex,
                    target_vertex,
                    800,  # net.channelWidth,
                    1600,  # net.channelSpacing,
                )
                # r = Route(net.ID, source_vertex, target_vertex)
                routes.append(route)

            net.routes = routes
        # Step 3 - Do the routing
        router = AARFRouter([])
        router.route(routes)

        # TODO - New API
        # router = AARFRouter(obstacles)
        # router.route(routes)

        print(routes)
        print("Routed route:")
        for route in routes:
            print(
                "Route: Start - ({}, {}) End - ({}, {})".format(
                    route.start.x, route.start.y, route.end.x, route.end.y
                )
            )
            print("Waypoints:")
            for waypoint in route.waypoints:
                print("({}, {})".format(waypoint.x, waypoint.y))

    def place_and_route_design(self):
        cells = list(self.cells.values())
        nets = list(self.nets.values())
        constraints = []
        placer = CPlacer(cells, nets, constraints)
        placer.place_and_route()
