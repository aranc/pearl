#input: model description, parameters selection strategies, reality investigation strategies
#output: for each parameter selection startegy, use the model to instantiate a world we can sample from
#        then for each of these world, for each of the investigators, investigate the world by sampling it and see if and how much we succeeded in recovering the selected parameters:

import argparse
import importlib

from model import Template, World
from parameters import ParametersFactory

parser = argparse.parser()
parser.add_argument("--model")
parser.add_argument("--parameters", nargs="+")
parser.add_argument("--investigators", nargs="+")
args = parser.parse_args()

# Setup

investigators = []
for investigator in args.invetigators:
    investigators.append(importlib.import_module(investigator).Investigator)

template = Template(args.model)
worlds = []
for strategy in args.parameters:
    world = World(template, ParametersFactory(strategy, template.parameters()))
    worlds.append(world)


