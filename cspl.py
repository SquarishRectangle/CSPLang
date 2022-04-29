from lib2to3.pytree import convert
import sys, yaml, re
from numpy import var
from typing import Union

variables = []

with open("elements.yaml", 'r') as file:
    elements = yaml.load(file, Loader=yaml.Loader)


def getElements(string:str) -> list:
    splitters = elements["unchanged"]
    splitters.append(' ')
    splitters = ["\\".join(s) for e in splitters for s in e]
    splitters = [f"(\\{s})" for s in splitters]
    splitters = "|".join(splitters)
    rElements = [e for e in re.split(splitters, string) if e]
    rElements = [e.strip() for e in rElements if e.strip()]
    return rElements


def replaceUncommons(string:str) -> str:
    for key, value in elements["uncommons"].items():
        string = string.replace(key, value)
    return string


def combineStrings(line:list) -> list:
    strings = ['"', "'"]
    while set(line).intersection(set(strings)):
        startI, str = next(([i, e] for i, e in enumerate(line) if e in strings), None)
        del line[startI]

        endI = next((i for i, e in enumerate(line) if e == str), None)
        
        if not endI:
            print("String not closed")
            sys.exit(1)

        del line[endI]
        
        line[startI:endI] = [str + " ".join(line[startI:endI]) + str]
    
    return line


def checkInvalid(line:list) -> Union[str, None]:
    global variables
    iterLine = iter(line)
    for element in iterLine:
        #check for strings
        if element.startswith('"') or element.startswith("'"):
            pass

        #check for numbers
        elif element.replace(".", "", 1).isdigit():
            pass

        #check for curley brackets
        elif element == "{" or element == "}":
            if len(line) > 1:
                return "Curley brackets must be on a separate line"

        elif element not in elements["unchanged"] and element not in elements["translate"] and element not in variables:
            try:
                if next(iterLine) == "\u2190":
                    #check for valid variable name
                    if not re.match("^[a-zA-Z][a-zA-Z0-9_]*$", element):
                        return f"Invalid variable name: {element}"
                    variables.append(element)

                else:
                    return f"{element} is not defined"

            except StopIteration:
                return f"{element} is not defined"


def checkEnclosed(condition:list) -> None:
    numparen = 0
    if condition[-1] != ')':
        print("Condition must be enclosed in parentheses")
        sys.exit(1)
    for e in condition[:-1]:
        if e == "(":
            numparen += 1
        elif e == ")":
            numparen -= 1
        if numparen <= 0:
            print("Condition must be enclosed in parentheses")
            sys.exit(1)


def seperateParams(params:list) -> list[list]:
    commas = [params.index(e) for e in params if e == ',']
    commaPairs = zip(commas[:-1], commas[1:])
    rParams = [params[:commas[0]], *[params[start+1:end] for start, end in commaPairs], params[commas[-1]+1:]]
    return rParams


def convertSyntax(line:list) -> list:
    global variables

    if not line:
        return line

    if line[0] == "IF":
        if len(line) < 4:
            print("Invalid IF statement")
            sys.exit(1)

        checkEnclosed(line[1:])
        line.append(':')

    elif line[0] == "ELSE":
        if len(line) > 1:
            print("ELSE must be on its own line")
            sys.exit(1)
        
        line.append(':')
        
    elif line[0] == "REPEAT":
        if line[1] == "UNTIL":
            if len(line) < 5:
                print("Invalid REPEAT statement")
                sys.exit(1)
            
            checkEnclosed(line[2:])
            line[:2] = "while not"
            line.append(':')
        
        elif line[-1] == "TIMES":
            if len(line) < 3:
                print("Invalid REPEAT statement")
                sys.exit(1)

            checkEnclosed(line[1:-1])
            line = ["for _ in range(", *line[1:-1], ')']
            line.append(':')
        
        else:
            print("Invalid REPEAT statement")
            sys.exit(1)

    elif line[0] == "INSERT":
        if len(line) < 8:
            print("Invalid INSERT statement")
            sys.exit(1)
            
        checkEnclosed(line[1:])
        params = seperateParams(line[2:-1])
        if len(params) != 3:
            print("Invalid INSERT statement")
            sys.exit(1)
        
        line = [f"{params[0]}.insert({params[1]}, {params[2]})"]

    elif line[0] == "APPEND":
        if len(line) < 6:
            print("Invalid APPEND statement")
            sys.exit(1)
        
        checkEnclosed(line[1:])
        params = seperateParams(line[2:-1])
        if len(params) != 2:
            print("Invalid APPEND statement")
            sys.exit(1)

        line = [f"{params[0]}.append({params[1]})"]
        
    elif line[0] == "REMOVE":
        if len(line) < 6:
            print("Invalid REMOVE statement")
            sys.exit(1)
        
        checkEnclosed(line[1:])
        params = seperateParams(line[2:-1])
        if len(params) != 2:
            print("Invalid REMOVE statement")
            sys.exit(1)

        line = [f"{params[0]}.pop({params[1]})"]
        
    elif line[0] == "FOR":
        if len(line) < 5: 
            print("Invalid FOR EACH statement")
            sys.exit(1)
        if (line[1], line[3]) != ("EACH", "IN"):
            print("Invalid FOR EACH statement")
            sys.exit(1)
        
        line.pop(1)
        line.append(':')

    elif line[0] == "PROCEDURE":
        if len(line) < 4:
            print("Invalid PROCEDURE definition")
            sys.exit(1)

        variables.append(line[1])
        line.append(':')

    elif line[0] == "RETURN":
        checkEnclosed(line[1:])

    return line


def parseLine(line:str) -> list:
    global variables
    #convert line to list of elements
    line = getElements(line)

    #combine strings into one element
    line = combineStrings(line)

    #check for invalid elements
    error = checkInvalid(line)
    if error:
        print(error)
        sys.exit(1)

    #convert syntax
    line = convertSyntax(line)
    
    #translate elements
    line = [elements["translate"][e] if e in elements["translate"] else e for e in line]
    return line


def main(*args):
    filePath = args[0]
    with open(filePath, 'r') as file:
        raw = file.read()

    raw = replaceUncommons(raw)

    lines = raw.split("\n")
    rLines = [["from", "random", "import", "randint"]]

    #parse lines
    for line in lines:
        rLines.append(parseLine(line))
    
    rLines = [l for l in rLines if l]
    
    #indent lines
    indent = 0
    indents = []
    for line in rLines:
        if line == ["{"]:
            indent += 1
        elif line == ["}"]:
            indent -= 1
        else:
            indents.append(indent)
    
    #remove curley brackets
    rLines = [l for l in rLines if l != ["{"] and l != ["}"]]

    #add indents
    for line, indent in zip(rLines, indents):
        if indent > 0:
            line.insert(0, "   " + "    " * (indent-1))
    
    rCode = "\n".join([" ".join(l) for l in rLines])
    print(rCode)
    exec(rCode)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)