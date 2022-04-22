import yaml


unchanged = [
    '+', '-', '*', '/',
    '>', '<',
    '(', ')',
    '[', ']',
    ',', 
    '"', "'",
]

translate = {
    "<-": "=",
    "=": "==",
    "DISPLAY": "print",
    "INPUT": "input",
    "MOD": "%",
    "RANDOM": "random.randint",
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

elements = {
    "unchanged": unchanged,
    "translate": translate
}

with open("elements.yaml", 'w') as file:
    yaml.dump(elements, file, Dumper=yaml.Dumper)