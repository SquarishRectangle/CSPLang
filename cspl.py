import sys, yaml, os, re

with open("elements.yaml", 'r') as file:
    elements = yaml.load(file, Loader=yaml.Loader)



def main(*args):
    filePath = args[0]
    with open(filePath, 'r') as file:
        inCode = file.read()
    lines = inCode.split("\n")
    outLines = []
    for line in lines:
        words = line.split()
        outWords = []
        #convert to elements
        for word in words:
            pass

if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)