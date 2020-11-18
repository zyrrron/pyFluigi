from pymint.mintdevice import MINTDevice


def assign_single_port_terminals(device: MINTDevice):
    # Loop through each of the connections
    for connection in device.connections:
        # Check if the source component has a single port
        source_component = device.get_component(connection.source.component)

        if None is connection.source.port and len(source_component.ports) == 1:
            connection.source.port = source_component.ports[0].label

        for sink_target in connection.sinks:
            sink_component = device.get_component(sink_target.component)

            if None is sink_target.port and len(sink_component.ports) == 1:
                sink_component.port = sink_component.ports[0].label
