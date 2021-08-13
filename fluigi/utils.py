from typing import Tuple
from networkx import nx
import fluigi.parameters as parameters
import os
import cairo
from fluigi.parameters import DEVICE_X_DIM, DEVICE_Y_DIM, PT_TO_UM
from parchmint import Device, Target


def printgraph(G, filename: str) -> None:
    tt = os.path.join(parameters.OUTPUT_DIR, filename)
    print("output:", tt)
    nx.nx_agraph.to_agraph(G).write(tt)

    os.system("dot -Tpdf {} -o {}.pdf".format(tt, tt))


def get_ouput_path(filename: str) -> str:
    return os.path.join(parameters.OUTPUT_DIR, filename)


def calcuate_waypoint(device: Device, target: Target) -> Tuple[int, int]:
    """Calculates the coordinates of the Target

    [extended_summary]

    Args:
        device (Device): [description]
        target (Target): [description]

    Returns:
        Tuple[float]: [description]
    """
    # Get  position of the of target and calculate the offset from the base component
    component = device.get_component(target.component)
    if target.port is not None:
        port = component.get_port(target.port)
        xoffset = component.xpos + port.x
        yoffset = component.ypos + port.y
        return (xoffset, yoffset)
    else:
        # Return the center of the component instead
        return (
            int(component.xpos + component.xspan / 2),
            int(component.ypos + component.yspan / 2),
        )


def render_svg(d: Device, suffix) -> None:

    suffix = suffix.replace(d.name, "")
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
        str(parameters.OUTPUT_DIR.joinpath("{}.svg".format(d.name + suffix))),
        xspan * PT_TO_UM,
        yspan * PT_TO_UM,
    )
    ctx = cairo.Context(surface)
    ctx.scale(PT_TO_UM, PT_TO_UM)

    for component in d.components:
        if component.params.exists("position"):
            # Set the color to black
            ctx.set_source_rgb(0, 0, 0)
            xpos = component.xpos
            ypos = component.ypos

            # Printing
            ctx.rectangle(xpos, ypos, component.xspan, component.yspan)
            ctx.fill()
        else:
            print(
                "Could not render component:{} since no position information was found".format(
                    component.ID
                )
            )

    ctx.set_source_rgb(0, 0, 1)
    for connection in d.connections:

        for path in connection.paths:
            channelwidth = connection.params.get_param("channelWidth")
            waypoints = path.waypoints
            for i in range(len(waypoints) - 1):
                # Set the color to blue
                ctx.set_source_rgb(0, 0, 1)
                waypoint = waypoints[i]
                next_waypoint = waypoints[i + 1]
                ctx.move_to(waypoint[0], waypoint[1])
                ctx.line_to(next_waypoint[0], next_waypoint[1])
                ctx.set_line_width(channelwidth / 2)
                ctx.stroke()
            else:
                if path.source.component is None or path.source.port is None:
                    print(
                        "Could not render connection {} path [{}] becasue of missing information (Component- {}, Port - {})".format(
                            connection.ID,
                            connection.paths.index(path),
                            path.source.component,
                            path.source.port,
                        )
                    )
                    continue
                # Set the color to grey
                ctx.set_source_rgb(0.5, 0.5, 0.5)
                # Get the source and target locations from the corresponding components
                source_waypoint = calcuate_waypoint(d, path.source)
                target_waypoint = calcuate_waypoint(d, path.sink)
                ctx.move_to(source_waypoint[0], source_waypoint[1])
                ctx.line_to(target_waypoint[0], target_waypoint[1])
                ctx.set_line_width(channelwidth / 2)
                ctx.stroke()

    # Draw ports at the end so that all the port connections are visible thoroughly
    for component in d.components:
        if component.params.exists("position"):
            # Set the color to black
            xpos = component.xpos
            ypos = component.ypos
            # Draw small cicles for all the ports
            for port in component.ports:
                # Set the color to red
                ctx.set_source_rgb(1, 0, 0)
                # Draw circle of radius 5
                ctx.arc(xpos + port.x, ypos + port.y, 100, 0, 2 * 3.14)
                ctx.fill()
        else:
            print(
                "Could not render port of component :{} since no position information was found".format(
                    component.ID
                )
            )

    surface.finish()
