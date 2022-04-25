lines = [
    ["never"],
    ["gonna"],
    ["give"],
    ["you"],
    ["up"]
]
starts = [
    "never",
    "gonna",
    "let",
    "you",
    "down"
]


import re

elements = "hello yall hi_the05re hi_there1 _ _hello hello_world".split()

for element in elements:
    if not re.match("^[a-zA-Z][a-zA-Z0-9_]*$", element):
        print(f"Invalid variable name: {element}")