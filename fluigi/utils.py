from networkx import nx
import fluigi.parameters as parameters
import os
import cairo
from fluigi.parameters import DEVICE_X_DIM, DEVICE_Y_DIM, PT_TO_UM


def printgraph(G, filename: str) -> None:
    tt = os.path.join(parameters.OUTPUT_DIR, filename)
    print("output:", tt)
    nx.nx_agraph.to_agraph(G).write(tt)

    os.system("dot -Tpdf {} -o {}.pdf".format(tt, tt))


def get_ouput_path(filename: str) -> str:
    return os.path.join(parameters.OUTPUT_DIR, filename)


def render_svg(d, suffix) -> None:

    suffix.replace(d.name, "")
    if d.params.exists("xspan"):
        xspan = d.params.get_param("xspan")
    else:
        xspan = DEVICE_X_DIM

    if d.params.exists("yspan"):
        yspan = d.params.get_param("yspan")
    else:
        yspan = DEVICE_Y_DIM

    print(
        "Rendering {} components and {} connections".format(
            len(d.components), len(d.connections)
        )
    )

    surface = cairo.SVGSurface(
        "{}.svg".format(parameters.OUTPUT_DIR.joinpath(d.name + suffix)),
        xspan * PT_TO_UM,
        yspan * PT_TO_UM,
    )
    ctx = cairo.Context(surface)
    ctx.scale(PT_TO_UM, PT_TO_UM)

    for component in d.components:
        if component.params.exists("position"):
            xpos = component.params.get_param("position")[0]
            ypos = component.params.get_param("position")[1]

            # Printing
            ctx.rectangle(xpos, ypos, component.xspan, component.yspan)
            ctx.fill()

    for connection in d.connections:
        if connection.params.exists("wayPoints"):
            waypoints = connection.params.get_param("wayPoints")
            channelwidth = connection.params.get_param("channelWidth")
            for i in range(len(waypoints) - 1):
                waypoint = waypoints[i]
                next_waypoint = waypoints[i + 1]
                ctx.move_to(waypoint[0], waypoint[1])
                ctx.line_to(next_waypoint[0], next_waypoint[1])
                ctx.set_line_width(channelwidth / 2)
                ctx.stroke()

    surface.finish()
