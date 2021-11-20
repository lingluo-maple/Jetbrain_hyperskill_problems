import string
from collections import deque


class Calculator:
    def __init__(self):
        self.variable = Variable()
        self.postfix = deque()
        self.operations = deque()

    def main(self):
        while True:
            data = input()
            if data.startswith("/"):
                self.command(data)
            elif data == "":
                continue
            else:
                err = self.check_valid(data)
                if not err:
                    if "=" in data:
                        data = data.replace(" ", "")
                        key, value = data.split("=")[0], data.split("=")[1]
                        self.variable.set(key, value)
                        continue
                    else:
                        self.calculate(data)
            self.postfix = deque()

    def calculate(self, expression):
        expression = expression.replace(" ", "")
        data = []
        n = ""
        o = ""
        digit = False
        _ = 0
        for i in expression:
            if i in "+-":
                if digit:
                    data.append(n)
                    n = ""
                    digit = False
                if not i.isdigit():
                    if i == "+" and o == "":
                        o = "+"
                    elif i != "+" and o == "+":
                        data.append(o)
                        o = ""
                    if i == "-":
                        _ += 1
                        o = "-"
                    elif i != "-" and o == "-":
                        if _ % 2:
                            data.append("-")
                        else:
                            data.append("+")
                        o = ""
                        _ = 0
            else:
                if i.isdigit():
                    n += i
                    digit = True
                else:
                    if n:
                        data.append(n)
                        digit = False
                        n = ""
                if o == "+":
                    data.append(o)
                    o = ""
                elif o == "-":
                    if _ % 2:
                        data.append("-")
                    else:
                        data.append("+")
                    o = ""
                    _ = 0
                if not i.isdigit():
                    data.append(i)
        if n:
            data.append(n)
        self.infix_to_postfix(data)
        main = deque()
        for i in self.postfix:
            if isinstance(i, int):
                main.append(i)
            else:
                b = main.pop()
                a = main.pop()
                main.append(eval(f"{a} {i} {b}"))
        if main:
            print(int(main.pop()))

    def infix_to_postfix(self, expression: list):
        for i in expression:
            if i.isdigit():
                i = int(i)
            if isinstance(i, str) and i not in "+-/*()":
                i = self.variable.get(i)
                if not isinstance(i, int):
                    return
            if isinstance(i, int):
                self.postfix.append(i)
            elif not self.operations:  # deque is empty
                self.operations.append(i)
            elif i == "(":
                self.operations.append(i)
            elif i == ")":
                while True:
                    operation = self.operations.pop()
                    if operation != "(":
                        self.postfix.append(operation)
                    else:
                        break
            elif self.operations[-1] == "(":
                self.operations.append(i)
            else:
                while True:
                    if self.operations and self.operations[-1] != '(' and \
                            self.priority(i) <= self.priority(self.operations[-1]):
                        self.postfix.append(self.operations.pop())
                    else:
                        self.operations.append(i)
                        break
        while self.operations:
            self.postfix.append(self.operations.pop())

    @staticmethod
    def priority(z):
        if z in ['×', '*', '/']:
            return 2
        elif z in ['+', '-']:
            return 1

    @staticmethod
    def check_valid(data):
        if data.endswith("+") or data.endswith("-"):
            print("Invalid expression")
            return True
        if ("(" in data and ")" not in data) or ("(" not in data and ")" in data) or "**" in data or "//" in data:
            print("Invalid expression")
            return True

    @staticmethod
    def command(cmd):
        if cmd == "/help":
            print("A calculator program")
        elif cmd == "/exit":
            print("Bye!")
            exit()
        else:
            print("Unknown command")


class Variable(dict):
    def get(self, key):
        result = super().get(key)
        if isinstance(result, int):
            return result
        else:
            print("Unknown variable")

    def set(self, key, value) -> None:
        v1 = self.test_var(key, mode="key")
        if v1:
            v2 = self.test_var(value, mode="value")
            if v2:
                try:
                    value = int(value)
                except ValueError:
                    value = super().get(value)
                self[key] = value

    def test_var(self, v, mode) -> bool:
        if mode == "key":
            for i in string.digits:
                if i in v:
                    print("Invalid identifier")
                    return False
            return True
        elif mode == "value":
            try:
                v = int(v)
            except ValueError:
                value = super().get(v)
                if not isinstance(value, int):
                    print("Invalid assignment")
                else:
                    return True
            else:
                return True  # No ascii letters


if __name__ == "__main__":
    c = Calculator()
    c.main()
