#baysean casual model
#assuming noisy-or model

from copy import deepcopy
from functools import cache

def parse_question(s):
    return parse_arrow_expression(s)

def parse_arrow_expression(s):
    return (_.strip() for _ in s.split("->"))

def prod(*args):
    res = 1
    for arg in args:
        res *= arg
    return res

class Template:
    def __init__(self, edges:str):
        _edges = {}
        for arrow in edges.split(";"):
            a, b = parse_arrow_expression(arrow)
            _edges[a] = b
        self.init(_edges)

    def init(self, edges:dict[str, str]):
        self.edges = deepcopy(edges)
        self.nodes = []
        self.parents = {}
        self.childs = {}

        for x, y in edges.items():
            if x not in self.nodes:
                self.nodes.append(x)
                self.parents[x] = []
                self.childs[x] = []
            if y not in self.nodes:
                self.nodes.append(y)
                self.parents[y] = []
                self.childs[y] = []

            if y not in self.parents[x]:
                self.parents[x].append(y)

            if x not in self.childs[y]:
                self.childs[y].append(x)

    @cache
    def parameters(self):
        params = []
        for node in self.nodes:
            if not self.parents[node]:
                params.append(node)
            else:
                for parent in self.parents[node]:
                    params.append((parent, node))

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

    def __call__(self, do):
        # need to topologically sort and fill values, but overwrite those that are present in the "do operator"

        dependencies = deepcopy(self.parents)
        next_up = list(self.prime.keys())
        res = {}
        while next_up:
            x = next_up.pop()
            if x in do:
                res[x] = do[x]
            else:
                #noisy or sampling
                p = 1 - prod(1 - self.noisy_or[x][parent] for parent in self.parents[x])
                res[x] = 1 if random.random() <= p else 0

            # update dependencies graph and update next_up
            for child in self.childs[x]:
                assert x in dependencies[child]
                del dependencies[child][x]
                assert x not in dependencies[child]

                if not dependencies[child]:
                    del dependencies[child]
                    next_up.append(child)

        assert len(res) == len(self.nodes)
        return res

    def parameters():
        s = ""
        for x in self.prime:
            s += f"{x}:{self.prime[x]} "
        for x in self.noisy_or:
            for y in self.noisy_or[x]:
                s += f"{y}->{x}:{self.noisy_or[x][y]} "
        return s
