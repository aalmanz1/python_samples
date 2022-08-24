""" OUTPUT FILE INCLUDED IN .ZIP. NAME IS JUST 'OUTPUT' """
""" RUN USING > python3 scanner.py <input_file> output """

""""""""""""""""""""""""""""""""""""
"""
Alex Almanza
Professor Sepehr Amir-Mohammadian
COMP 141
7 March 2021

COURSE PROJECT
Phase 2.1: Parser for Lexp
"""
""""""""""""""""""""""""""""""""""""

import os
import re
import sys
from collections import namedtuple

# used namedtuple instead of a class for simplicity,
TOKEN = namedtuple('Token', ['type', 'value'])

"""
class Token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value
"""


class PTNode:
    # next_token = Token('ERROR', 0)  # temporary, this assignment of 'ERROR' is nonfunctional
    next_token = TOKEN('ERROR', 0)
    scan_list = []
    iterator = 0

    def get_left_subtree(self):
        pass

    def get_right_subtree(self):
        pass

    def consume(self):
        print(self.iterator)
        if self.iterator >= len(self.scan_list) - 2:
            return 0
        self.iterator = self.iterator + 1
        self.next_token = self.scan_list[self.iterator + 1]

    # Parsing functions for Lexp
    def parse_expr(self):
        tree = self.parse_term()
        while self.next_token.value == '+':
            self.consume()
            tree = PTInteriorNode('+', tree, self.parse_term())
        return tree

    def parse_term(self):
        tree = self.parse_factor()
        while self.next_token.value == '-':
            self.consume()
            tree = PTInteriorNode('-', tree, self.parse_factor())
        return tree

    def parse_factor(self):
        tree = self.parse_piece()
        while self.next_token.value == '/':
            self.consume()
            tree = PTInteriorNode('/', tree, self.parse_piece())
        return tree

    def parse_piece(self):
        tree = self.parse_element()
        while self.next_token.value == '*':
            self.consume()
            tree = PTInteriorNode('*', tree, self.parse_element())
        return tree

    def parse_element(self):
        if self.next_token.value == '(':
            self.consume()
            tree = self.parse_expr()
            if self.next_token.value == ')':
                return tree
        elif self.next_token.type == 'IDENTIFIER':
            n = self.next_token
            self.consume()
            return PTLeafNode(n)

    def parse(self, x_list):
        self.scan_list = x_list
        self.iterator = 0
        self.next_token = self.scan_list[self.iterator + 1]
        return self.parse_expr()


class PTInteriorNode(PTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def get_operator(self):
        return self.operator

    def get_left_child(self):
        return self.left

    def get_right_child(self):
        return self.right


class PTLeafNode(PTNode):
    identifier = ""
    number = 0

    def __init__(self, node):
        self.node = node

    def get_identifier(self):
        return self.identifier

    def get_number(self):
        return self.number

    def set_identifier(self, i):
        self.identifier = i

    def set_number(self, n):
        self.number = n

    def get_left_subtree(self):
        return None

    def get_right_subtree(self):
        return None


def print_AST(tree):
    if tree:
        print_AST(tree.get_left_child())
        print_AST(tree.get_right_child())


# our regex language covering numbers, symbols, and identifiers
# also included are whitespaces (so that they are ignored in our test_output)
# and errors (essentially anything else not specified by the language)
# used ?P to be able to assign a name to each expression
keywords = '(?P<KEYWORD>[if|then|else|endif|while|do|endwhile|skip]+)'
identifiers = '(?P<IDENTIFIER>([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*)'
numbers = '(?P<NUMBER>\d+)'
symbols = '(?P<SYMBOL>[+*/()\-:=;]+)'
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
                    yield TOKEN(i.lastgroup, i.group())
                break
            else:
                yield TOKEN(i.lastgroup, i.group())
                found_error = False

        else:
            found_error = False


def main():
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
    token_list = []

    with open(i) as file:
        for line in file:
            print("--------------------------\nLine: " +
                  line.strip() +
                  "\n--------------------------")
            output.write("Line: " + line.strip() + "\n")

            # Each character in line in file is separated according to regex definitions,
            # tokenized, and then printed to the console and written to the output file.
            for x in generate_tokens(line):
                print(x.type + " : " + x.value)
                output.write(x.type + " : " + x.value + "\n")
                token_list.append(x)

    # remove parentheses for ease of parsing
    parentheses = {'(', ')'}
    token_list = [ele for ele in token_list if ele not in parentheses]
    print("--------------------------\nAST:\n")

    tree = PTNode().parse(token_list)
    print_AST(tree)

    print("\nPlease see README")


if __name__ == "__main__":
    main()
