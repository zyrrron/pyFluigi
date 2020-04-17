import networkx as nx
import matplotlib.pyplot as plt
from pnr.layout import Layout


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