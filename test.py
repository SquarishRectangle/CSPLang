import yaml


unchanged = [
    '+', '-', '*', '/',
    '>', '<',
    '(', ')',
    '[', ']',
    ',', 
    '"', "'"
]

translate = {
    "\u2190": "=",
    "=": "==",
    "DISPLAY": "print",
    "INPUT": "input",
    "MOD": "%",
    "RANDOM": "randint",
    "\u2260": "!=",
    "\u2264": "<=",
    "\u2265": ">=",
    "NOT": "not",
    "AND": "and",
    "OR": "or",
    "IF": "if",
    "ELSE": "else", 
    "LENGTH": "len",
    "PROCEDURE": "def",
    "RETURN": "return"   
}

uncommons = {
    "<-": "\u2190",
    "!=": "\u2260",
    "<=": "\u2264",
    ">=": "\u2265"
}

elements = {
    "unchanged": unchanged,
    "translate": translate,
    "uncommons": uncommons
}

with open("elements.yaml", 'w') as file:
    yaml.dump(elements, file, Dumper=yaml.Dumper)