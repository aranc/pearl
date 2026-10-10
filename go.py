#input: model description, parameters selection strategies, reality investigation strategies
#output: for each parameter selection startegy, use the model to instantiate a world we can sample from
#        then for each of these world, for each of the investigators, investigate the world by sampling it and see if and how much we succeeded in recovering the selected parameters:

import argparse
import importlib

from model import Template, World, parse_question
from parameters import ParametersFactory
from utils import extract_func_and_args

parser = argparse.ArgumentParser()
parser.add_argument("--model", default="x->y;z->x;z->y")
parser.add_argument("--parameters", nargs="+", default=["rand"])
parser.add_argument("--investigators", nargs="+", default=["rct"])
parser.add_argument("--num_samples", type=int, default=10000)
parser.add_argument("--question", default="x->y")
args = parser.parse_args()
print(args)

# Setup

investigators = []
for investigator in args.investigators:
    investigator, args = extract_func_and_args(investigator)
    investigators.append((investigator, importlib.import_module(f"investigators.{investigator}").Investigator(args)))

template = Template(args.model)
worlds = []
for strategy in args.parameters:
    for parameters in ParametersFactory(strategy, template.parameters()):
        world = World(template, parameters)
        worlds.append(world)

x, y = parse_question(args.question)

# Benchmark

for world_idx, world in enumerate(worlds):
    print(f"Running for world #{world_idx}")
    print(world.parameters)

    for investigator_name, investigator in invetigators:
        print("Investigator:", investigator_name)
        answer = investigator(world, args.num_samples, (x, y))
        print("Answer:", answer)


