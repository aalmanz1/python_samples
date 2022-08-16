""" OUTPUT FILE INCLUDED IN .ZIP. NAME IS JUST 'OUTPUT' """
""" RUN USING > python3 scanner.py <input_file> output """

""""""""""""""""""""""""""""""""""""
"""
Alex Almanza
Professor Sepehr Amir-Mohammadian
COMP 141
26 January 2021

COURSE PROJECT
Phase 1.2: Scanner for Limp
"""
""""""""""""""""""""""""""""""""""""

import os
import re
import sys
from collections import namedtuple

# used namedtuple instead of a class for simplicity,
token = namedtuple('Token', ['type', 'value'])

# our regex language covering numbers, symbols, and identifiers
# also included are whitespaces (so that they are ignored in our test_output)
# and errors (essentially anything else not specified by the language)
# used ?P to be able to assign a name to each expression
keywords = '(?P<KEYWORD>[if|then|else|endif|while|do|endwhile|skip]+)'
identifiers = '(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z_0-9]*)'
numbers = '(?P<NUMBER>\d+)'
symbols = '(?P<SYMBOL>[\+|\-|\*|\/|\(|\)|\;|\:=].)'
whitespaces = '(?P<WHITESPACE>\s+)'  # catches newline, tab, space
errors = '(?P<ERROR>.)'  # ensures any erroneous character will be counted as an error


# gen_tokens uses the language defined above to identify and tokenize
# each character in the given string individually. returns (yields) namedtuple:
# token(i.lastgroup, i.group()), meaning token(type of token, value of token)
# re.compile, lastgroup, re.finditer(), re.group() all from python regex library
def generate_tokens(line):
    # compile all expressions into one language
    language = re.compile('|'.join([keywords, identifiers, numbers, symbols, whitespaces, errors]))
    found_error = False
    for i in language.finditer(line):
        if i.lastgroup != 'WHITESPACE':  # whitespaces ignored per longest substring principle

            if i.lastgroup == 'ERROR':  # check for characters not in the language and return error if found
                if not found_error:
                    yield token(i.lastgroup, i.group())
                    found_error = True
            else:
                yield token(i.lastgroup, i.group())
                found_error = False

        else:
            found_error = False


def main(argv):
    verification = os.listdir()
    n = len(sys.argv)

    if n > 3:
        print("ERROR: Please only enter one input file and one output file.\n"
              "unix> python3 scanner.py <input_file> <output_file>")
        sys.exit()
    elif n < 3:
        print("ERROR: Please enter two files.\n"
              "unix> python3 scanner.py <input_file> <output_file>")
        sys.exit()

    # I'm not sure if this is the best way I could've handled cmd line args ¯\_(ツ)_/¯
    i = sys.argv[1]
    o = sys.argv[2]

    while i not in verification or o not in verification:
        print("ERROR: No such file or directory.")
        sys.exit()

    output = open(o, 'w')

    with open(i) as file:
        for line in file:
            print("\n--------------------------")
            print("Line: " + line.strip())
            print("--------------------------")
            output.write("\nLine: " + line.strip() + "\n")
            # Each character in line in file is separated according to regex definitions,
            # tokenized, and then printed to the console and written to the output file.
            for i in generate_tokens(line):
                print(i.type + " : " + i.value)
                output.write(i.type + " : " + i.value + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
