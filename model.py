#baysean casual model
#assuming noisy-or model

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
        params = []
        for node in self.nodes:
            if not self.parents[node]:
                params.add(node)
            else:
                for parent in self.parents[node]:
                    params.add((parent, node))

        return tuple(params)

class World:
    def __init__(self, template, parameters):
        self.edges = deepcopy(template.edges)
        self.nodes = deepcopy(template.nodes)
        self.parents = deepcopy(template.parents)
        self.childs = deepcopy(template.childs)
        
        self.prime = {}
        self.noisy_or = {}

        for key, value in zip(template.parameters(), parameters):
            if type(key) is not tuple:
                assert key in self.nodes
                self.prime[key] = value
            else:
                parent, child = key
                assert parent in self.nodes
                assert child in self.nodes
                if child not in self.noisy_or:
                    self.noisy_or[child] = {}
                self.noisy_or[child][parent] = value
