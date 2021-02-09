from pymint import MINTDevice


def size_nodes(device: MINTDevice) -> None:
    for component in device.components:
        if component.entity == "NODE":
            # Look at the connections
            nbers = device.G.edges(component.ID)
            gedge = list(nbers)[0]
            # Get channelWidth from there and update the node
            # connection_ref = device.G[gedge[0]][gedge[1]]
            connection = device.G.get_edge_data(gedge[0], gedge[1])[0]["connection_ref"]
            channel_width = connection.params.get_param("channelWidth")
            component.xspan = channel_width
            component.yspan = channel_width


def check_ref_and_assign_port(source_ref, connection, device, global_port_assign_map):
    source_name = source_ref.component
    source = device.get_component(source_name)
    if source_ref.port is None:
        print(
            "No port assigned to connection ref - {}:{}:{}".format(
                connection.ID, source.ID, source_ref.port
            )
        )
        if len(source.ports) == 1:
            print("Auto Port Assign Scheme - Target contains only 1 port option")
            source_ref.port = source.ports[0].label
        elif len(source.ports) == 2 or len(source.ports) == 4:
            print("Auto Port Assign Scheme - Target contains only 2 or 4 port options")
            if source.ID not in global_port_assign_map.keys():
                # Add component to global assign map
                global_port_assign_map[source.ID] = 0

            # Do the assignment of the port from the global assign map index
            port_index = global_port_assign_map[source.ID]
            source_ref.port = str(source.ports[port_index].label)
            port_index += 1
        else:
            print(
                "Error - Auto Port scheme does not work for target containing {} ports ".format(
                    len(source.ports)
                )
            )

        print("Assigned port - {}".format(source_ref.port))


def assign_component_ports(device: MINTDevice) -> None:
    print("Starting terminal/port assignment ...")
    global_port_assign_map = dict()
    for connection in device.connections:
        source_ref = connection.source
        check_ref_and_assign_port(
            source_ref, connection, device, global_port_assign_map
        )
        for sink_ref in connection.sinks:
            check_ref_and_assign_port(
                sink_ref, connection, device, global_port_assign_map
            )
