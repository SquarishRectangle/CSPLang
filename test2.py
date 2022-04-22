import yaml, random


operators = {
    "<-": "assign",
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "/": "divide"
}

keywords = {
    "TRUE": True,
    "FALSE": False
}

functions = {
    "DISPLAY": "print",
    "RANDOM": "random"
}

elements = {
    "operators": operators,
    "keywords": keywords,
    "functions": functions
}

with open("elements.yaml", 'w') as file:
    yaml.dump(elements, file, Dumper=yaml.Dumper)