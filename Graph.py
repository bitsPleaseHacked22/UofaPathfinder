import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 

class Graph:

  def __init__(self, am, names):
    self.names = np.loadtxt(names, dtype=str, delimiter=',');
    matrix = np.genfromtxt(am, delimiter=',', filling_values=1000)
    

    self.G = nx.from_numpy_matrix(matrix)

    no_edges = list(filter(lambda e: e[2] == 1000, (e for e in self.G.edges.data('weight'))))
    le_ids = list(e[:2] for e in no_edges)


    self.G.remove_edges_from(le_ids)


  def getWeight(self, i, j):
    node = self.G[i][i]
    return node['weight']
      

  def getName(self, i):
    return self.names[i]

  def printGraph(self):
    nx.draw(self.G) 
    plt.show()
