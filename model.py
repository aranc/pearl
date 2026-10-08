#baysean casual model

from copy import deepcopy
from functools import cached_property

class Template:
    def __init__(self, edges:dict[str, str]):
        self.edges = deepcopy(edges)
        self.nodes = []
        self.parents = {}
        self.childs = {}

        for x, y in edges.items():
            if x not in nodes:
                self.nodes.append(x)
                self.parents[x] = []
                self.childs[x] = []
            if y not in nodes:
                self.nodes.append(y)
                self.parents[y] = []
                self.childs[y] = []

            if y not in self.parents[x]:
                self.parents[x].append(y)

            if x not in self.childs[y]:
                self.childs[y].append(x)

    @cached_property
    def parameters(self):
        pass
