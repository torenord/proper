#!/usr/bin/env python3

"""

Proper: The world's first Tore-oriented programming language.

"""

### Primitives #############################################

def drop(stack):
    """Discards the top stack item."""

    stack.pop()

def swap(stack):
    """Reverses the top two stack items."""

    a = stack.pop()
    b = stack.pop()
    stack.append(a)
    stack.append(b)

def dup(stack):
    """Duplicates the top stack item."""

    a = stack.pop()
    stack.append(a)
    stack.append(a)

def rot(stack):
    """Rotates the third item to the top."""

    c = stack.pop()
    b = stack.pop()
    a = stack.pop()
    stack.append(b)
    stack.append(c)
    stack.append(a)

def over(stack):
    """Makes a copy of the second item and pushes it on top."""

    a = stack.pop()
    b = stack.pop()
    stack.append(b)
    stack.append(a)
    stack.append(b)

def inc(stack):
    """Increment."""

    a = stack.pop()
    stack.append(a + 1)

def dec(stack):
    """Decrement."""

    a = stack.pop()
    stack.append(a - 1)

def add(stack):
    """Addition."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a + b)

def sub(stack):
    """Subtraction."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a - b)

def mul(stack):
    """Multiplication."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a * b)

def _pow(stack):
    """Power."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a ** b)

def div(stack):
    """Division without remainder."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a // b)

def truediv(stack):
    """Division as float."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a / b)

def mod(stack):
    """Remainder of division."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a % b)

def eq(stack):
    """Equality."""

    a = stack.pop()
    b = stack.pop()
    stack.append(1 if a == b else 0)

def lt(stack):
    """Less than."""

    b = stack.pop()
    a = stack.pop()
    stack.append(1 if a < b else 0)

def _pop(stack):
    print(stack.pop())

def _list(stack):
    a = stack.pop()
    stack.append([a])

def append(stack):
    """Concatenate two lists."""

    b = stack.pop()
    a = stack.pop()
    stack.append(a + b)

def first(stack):
    """Find first element of list."""

    a = stack.pop()
    stack.append(a[0])

def rest(stack):
    """Return list without first element."""

    a = stack.pop()
    stack.append(a[1:])

def _print(stack):
    print(stack[-1])

def print_stack(stack):
    print("[", " ".join(str(e) for e in stack), "]", sep="")

def print_dictionary(stack):
    for k in dictionary:
        print(k)

def _quit(stack):
    exit(1)

### Dictionary #############################################

dictionary = {
    "drop": drop,
    "swap": swap,
    "dup": dup,
    "rot": rot,
    "over": over,

    "inc": inc,
    "dec": dec,
    "+": add,
    "-": sub,
    "*": mul,
    "^": _pow,
    "/": truediv,
    "//": div,
    "%": mod,

    "=": eq,
    "<": lt,

    "pop": _pop,

    "list": _list,
    "append": append,
    "first": first,
    "rest": rest,

    "print": _print,
    "print_stack": print_stack,
    "print_dictionary": print_dictionary,

    "quit": _quit,
}

### Parsing ################################################

def tokenize(inp):
    """Tokenize string to list of tokens."""

    tokens = []

    for line in inp.split("\n"):
        if line:
            if line.find("---") >= 0:
                line = line[:line.find("---")]
            tokens += [x for x in line.split(" ") if x]

    return tokens

def is_integer(token):
    return token.isnumeric()

def is_float(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_string(token):
    return token[0] == token[-1] == '"'

def is_quoted(token):
    return token[0] == "'"

def parse(tokens):
    """Parse list of tokens to structure."""

    result = []

    i = 0
    while i < len(tokens):
        if is_integer(tokens[i]):
            result.append(int(tokens[i]))
        elif is_float(tokens[i]):
            result.append(float(tokens[i]))
        elif is_string(tokens[i]):
            result.append(tokens[i])
        elif is_quoted(tokens[i]):
            result.append(tokens[i])
        elif tokens[i] == "{":
            depth = 0
            lst = []
            j = i + 1
            while True:
                if tokens[j] == "{":
                    depth += 1
                if tokens[j] == "}":
                    depth -= 1
                    if depth == -1:
                        break
                lst.append(tokens[j])
                j += 1
            i = j
            result.append(parse(lst))
        elif tokens[i] == "[":
            depth = 0
            lst = []
            j = i + 1
            while True:
                if tokens[j] == "[":
                    depth += 1
                if tokens[j] == "]":
                    depth -= 1
                    if depth == -1:
                        break
                lst.append(tokens[j])
                j += 1
            i = j
            result.append(parse(lst))
        else:
            try:
                result.append(tokens[i])
            except KeyError:
                print("Error: Undefined procedure:", tokens[i])

        i += 1

    return result

### Eval ###################################################

def _eval(inp, stack):
    while len(inp) > 0:
        token = inp.pop(0)

        try:
            if isinstance(token, str) \
            and not is_string(token) \
            and not is_quoted(token):
                if token == "define":
                    func = stack.pop()
                    if not isinstance(func, list):
                        func = [func]
                    name = stack.pop()
                    dictionary[name[1:]] = func
                elif token == "load":
                    filename = stack.pop()
                    inp = parse(tokenize(open(filename[1:-1]).read())) + inp
                elif token == "map":
                    func = stack.pop()
                    lst = stack.pop()
                    _inp = []
                    for e in lst:
                        _inp += [e] + [func[1:]]
                    _stack = []
                    _eval(_inp, _stack)
                    stack.append(_stack)
                elif token == "reduce":
                    func = stack.pop()
                    lst = stack.pop()
                    inp = lst + [func[1:]] * (len(lst) - 1) + inp
                elif token == "zip":
                    func = stack.pop()
                    lst2 = stack.pop()
                    lst1 = stack.pop()
                    _inp = []
                    for a, b in zip(lst1, lst2):
                        _inp += [a, b] + [func[1:]]
                    _stack = []
                    _eval(_inp, _stack)
                    stack.append(_stack)
                elif token == "times":
                    n = stack.pop()
                    func = stack.pop()
                    _inp = []
                    for _ in range(n):
                        _inp += [func[1:]]
                    inp = _inp + inp
                elif token == "ifelse":
                    alternative = stack.pop()
                    consequent = stack.pop()
                    condition = stack.pop()

                    if condition != 0:
                        inp = consequent + inp
                    else:
                        inp = alternative + inp
                elif token in dictionary:
                    # Primitive
                    if callable(dictionary[token]):
                        dictionary[token](stack)

                    # Non-primitive
                    else:
                        func = dictionary[token][:]
                        inp = func + inp
                else:
                    print("Error: Undefined procedure:", token)
            else:
                raise TypeError
        except TypeError as e:
            stack.append(token)

### Main ###################################################

if __name__ == '__main__':
    import sys

    STACK = []

    INP = parse(tokenize(open("library.proper").read()))
    _eval(INP, STACK)

    if len(sys.argv) == 2:
        INP = parse(tokenize(open(sys.argv[1]).read()))
        _eval(INP, STACK)
