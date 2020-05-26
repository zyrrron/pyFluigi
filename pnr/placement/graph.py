import networkx as nx
import matplotlib.pyplot as plt
from pnr.layout import Layout
import parameters


def generatePlanarLayout(layout: Layout):
    positions = nx.planar_layout(layout.G)
    print('Positions for all the cells:', positions)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()
    plt.savefig('test.png')


def generateSpectralLayout(layout: Layout):
    positions = nx.spectral_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.planar_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.circular_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.bipartite_layout(layout.G, nx.bipartite.sets(layout.G)[0])
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()
    
    positions = nx.shell_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()
    
    positions = nx.random_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.spiral_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()


    # plt.savefig('test.png')


def generateSpringLayout(layout: Layout):
    positions = nx.spring_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()
    # plt.savefig('test.png')

    x_scale_factor = 0.7*parameters.DEVICE_X_DIM/2
    y_scale_factor = 0.7*parameters.DEVICE_Y_DIM/2

    center_x = parameters.DEVICE_X_DIM/2
    center_y = parameters.DEVICE_Y_DIM/2

    # Scale the positions based on the spring layout
    for cell_id in positions.keys():
        position = positions[cell_id]
        cell = layout.cells[cell_id]
        cell.x = int(center_x + position[0] * x_scale_factor)
        cell.y = int(center_y + position[1] * y_scale_factor)
    
    # Expand the components 
    