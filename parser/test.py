import re
import enum


# ENUM -----------------------------------------
class TokenType(enum.Enum):
    TT_PLUS = 1  # +
    TT_TIMES = 2  # *
    TT_LPAREN = 3  # (
    TT_RPAREN = 4  # )
    TT_EQL = 5  # end of line
    TT_NUMBER = 6  # number
    TT_ERROR = 7  # Error
    TT_INDEN = 8  # Identifier
    TT_MINUS = 9  # -
    TT_KEYWORD = 10  # Keyword like if and else if
    TT_EQUAL = 11  # =
    TT_SEMICOLON = 12  # ;
    TT_DIVIDE = 13


# ----------------------------------------------
# Token Class -----------------------------------
class Token:
    def __init__(self, token_name, token_type, token_vaule):
        self.token_type = TokenType(token_type)
        self.token_value = int(token_vaule)
        self.token_name = str(token_name)


# ----------------------------------------------

# PARSER CLASS-------------------------------------------------
class PTNode:
    next_token = Token(0, TokenType.TT_ERROR, 0)
    scanlist = []
    iterator = 0

    def getLeftSubtree(self):
        pass

    def getRightSubtree(self):
        pass

    def print(self, file):
        pass

    def consume_token(self):
        print(self.iterator)
        if self.iterator >= len(self.scanlist) - 2:
            return 0
        self.iterator = self.iterator + 1
        self.next_token = self.scanlist[self.iterator + 1]

    # PARSING FUNCTIONS---------------------------------------------------
    def parse_piece(self):
        tree = self.parse_element()

        while self.next_token.token_type == TokenType.TT_TIMES:
            self.consume_token()
            tree = PTInteriorNode('*', tree, self.parse_element())

        return tree

    def parse_element(self):
        # if self.next_token.token_type == TokenType.TT_ERROR:
        # raise Exception("Some is not a part of this language")
        if self.next_token.token_type == TokenType.TT_LPAREN:
            self.consume_token()
            tree = self.parse_expr()
            if self.next_token.token_type == TokenType.TT_RPAREN:
                return tree
        elif self.next_token.token_type == TokenType.TT_INDEN:
            n = self.next_token
            self.consume_token()
            return PTLeafNode(n)
        elif self.next_token.token_type == TokenType.TT_NUMBER:
            n = self.next_token
            self.consume_token()
            return PTLeafNode(n)

    def parse_factor(self):
        tree = self.parse_piece()
        while self.next_token.token_type == TokenType.TT_DIVIDE:
            self.consume_token()
            tree = PTInteriorNode('/', tree, self.parse_piece())
        return tree

    def parse_term(self):
        tree = self.parse_factor()
        while self.next_token.token_type == TokenType.TT_MINUS:
            self.consume_token()
            tree = PTInteriorNode('-', tree, self.parse_factor())
        return tree

    def parse_expr(self):
        tree = self.parse_term()
        while self.next_token.token_type == TokenType.TT_PLUS:
            self.consume_token()
            tree = PTInteriorNode('+', tree, self.parse_term())
        return tree

    def parse(self, l):
        self.scanlist = l

        self.iterator = 0
        self.next_token = self.scanlist[self.iterator + 1]
        return self.parse_expr()


# ------------------------------------------------------------------------------


class PTInteriorNode(PTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def getOperator(self):
        return self.operator

    def getLeftSubtree(self):
        return self.left

    def getRightSubtree(self):
        return self.right

    def print(self, file):
        s = f"{self.getOperator()} : PUNCUATION \n"
        file.write(str(s))


class PTLeafNode(PTNode):
    ident = ""
    number = 0

    def __init__(self, node):
        self.node = node

    def get_ident(self):
        return self.ident

    def get_num(self):
        return self.number

    def set_ident(self, i):
        self.ident = i

    def set_num(self, n):
        self.number = n

    def getLeftSubtree(self):
        return None

    def getRightSubtree(self):
        return None

    def print(self, file):
        s = f"{self.node.token_name} : {self.node.token_type} \n"
        file.write(str(s))


def print_AST(tree, file):
    if tree:
        tree.print(file)

        print_AST(tree.getLeftSubtree(), file)
        print_AST(tree.getRightSubtree(), file)


# Switch cases------------------------------------
def lpar(t, c):
    if c == '(':
        t.token_type = TokenType.TT_LPAREN


def rpar(t, c):
    if c == ')':
        t.token_type = TokenType.TT_RPAREN


def plus(t, c):
    if c == '+':
        t.token_type = TokenType.TT_PLUS


def times(t, c):
    if c == '*':
        t.token_type = TokenType.TT_TIMES


def eol(t, c):
    if c == '\n':
        t.token_type = TokenType.TT_EQL


def mi(t, c):
    if c == '-':
        t.token_type = TokenType.TT_MINUS


def eql(t, c):
    if c == ":=":
        t.token_type = TokenType.TT_EQUAL


def semi(t, c):
    if c == ";":
        t.token_type = TokenType.TT_SEMICOLON


def div(t, c):
    if c == "/":
        t.token_type = TokenType.TT_DIVIDE


# -------------------------------------------------


# GET TOKEN : Determines what type of token the current string is --------------------
def getToken(curr):
    token = Token(curr, TokenType.TT_ERROR, 0)
    # Dictionary of different symbols and the functions that set token value type

    if isNumber(curr):
        token.token_type = TokenType.TT_NUMBER
        token.token_value = int(curr)
    elif isIdentifier(curr):
        token.token_type = TokenType.TT_INDEN
    elif isKeyword(curr):
        token.token_type = TokenType.TT_KEYWORD
    elif isPuncutation(curr):
        lpar(token, curr)
        rpar(token, curr)
        plus(token, curr)
        eol(token, curr)
        mi(token, curr)
        times(token, curr)
        eql(token, curr)
        semi(token, curr)
        div(token, curr)
    else:
        token.token_type = TokenType.TT_ERROR
    return token


# ---------------------------------------------------------------------------------
def build_ID(line):
    l = list(line)
    leng = len(l)
    for i in range(leng):
        if isPuncutation(l[i]):
            l.insert(i - 1, " ")
            while isPuncutation(l[i]):
                i += 1

            l.insert(i + 1, " ")
    x = "".join(l)

    return x


# SHOW TOKEN : Writes in output file what Token Type the token is ----------------
def ShowToken(t, name, file):
    if t.token_type == TokenType.TT_NUMBER:
        s = f"{t.token_type.name} : {t.token_value} \n"
        file.write(str(s))
    elif t.token_type == TokenType.TT_INDEN:
        s = f"{t.token_type.name} : {name}\n"
        file.write(str(s))
    elif t.token_type == TokenType.TT_KEYWORD:
        s = f"{t.token_type.name} : {name}\n"
        file.write(str(s))
    else:
        s = f"{t.token_type.name}\n"
        file.write(str(s))


# ---------------------------------------------------------------------------------

# IS FUNCTIONS: DETERMINES IF TOKEN IS A NUMBER , IDENTIFIER , OR PUNCTUATION -----
def isNumber(n):
    x = len(n)
    for i in range(x):
        y = re.match('[0-9]+', n[i])
        if not y:
            return 0
    return bool(y)


def isIdentifier(n):
    x = re.match('([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])', n)
    if re.search('[+*/()]', n):
        return 0
    else:
        return bool(x)


def isPuncutation(n):
    x = re.match('[+*/()\-:=;]', n)
    return bool(x)


def isKeyword(n):
    x = ["if", "then", "else", "endif", "while", "do", "endwhile", "skip"]
    xl = len(x)
    for i in range(xl):
        if n == x[i]:
            return 1
        else:
            return 0


# ---------------------------------------------------------------------------------

# TEST DRIVER ---------------------------------------------------------------------
def main():
    tokenlist = []
    f_input = open("input")
    f_output = open("output", 'w')
    fi = f_input.readline()

    while fi:
        f = fi.split()
        leng = len(f)
        for i in range(leng):
            x = build_ID(f[i])
            fx = x.split()
            lenx = len(fx)
            for y in range(lenx):
                token = getToken(fx[y])
                if token.token_type == TokenType.TT_EQL:
                    break

                tokenlist.append(token)

                ShowToken(token, fx[y], f_output)
        fi = f_input.readline()
    tree = PTNode().parse(tokenlist)
    print_AST(tree, f_output)

    f_input.close()
    f_output.close()


# -----------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
