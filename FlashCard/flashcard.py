import os
import io
import sys
import json
import random
import logging
import argparse
from pathlib import Path


class FlashCard:
    def __init__(self):
        self.stream = io.StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.console = logging.StreamHandler(sys.stdout)
        self.handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s: %(message)s'))
        self.cards = []
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def add_handler(self):
        self.logger.addHandler(self.handler)
        self.logger.addHandler(self.console)

    def remove_handler(self):
        self.logger.removeHandler(self.handler)
        self.logger.removeHandler(self.console)

    def run(self):
        args = get_args()
        self.menu(args)

    def menu(self, args: dict):
        if args.get("import"):
            self.import_cards(args.get("import"))
        while True:
            self.add_handler()
            self.logger.info("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
            self.remove_handler()
            action = input()
            if action == "add":
                self.add()
            elif action == "remove":
                self.remove()
            elif action == "import":
                self.import_cards()
            elif action == "export":
                self.export_cards()
            elif action == "ask":
                self.ask()
            elif action == "log":
                self.log()
            elif action == "hardest card":
                self.hardest_card()
            elif action == "reset stats":
                self.reset()
            elif action == "exit":
                self.add_handler()
                self.logger.info("Bye bye!")
                self.remove_handler()
                if args.get("export"):
                    self.export_cards(args.get("export"))
                exit(0)

    def add(self):
        self.add_handler()
        self.logger.info(f"The card:")
        while True:
            term = input()
            if term in Card.terms:
                self.logger.info(f'The term "{term}" already exists. Try again:')
                continue
            else:
                break
        self.logger.info(f"The definition of the card:")
        while True:
            definition = input()
            if definition in Card.definitions:
                self.logger.info(f'The definition "{definition}" already exists. Try again:')
                continue
            else:
                break
        new_card = Card(term, definition)
        self.cards.append(new_card)
        self.logger.info(f'The pair ("{term}":"{definition}") has been added.')
        self.remove_handler()

    def remove(self):
        self.add_handler()
        self.logger.info("Which card?")
        term = input()
        card = self.get_by_term(term)
        if card:
            Card.definitions.remove(card.definition)
            Card.terms.remove(card.term)
            self.cards.remove(card)
            self.logger.info("The card has been removed.")
        else:
            self.logger.info(f'''Can't remove "{term}": there is no such card.''')
        self.remove_handler()

    def import_cards(self, file_name=None):
        self.add_handler()
        if not file_name:
            self.logger.info("File name:")
            file_name = input()
        file = Path(os.path.join(os.path.curdir, file_name))
        if file.exists():
            with open(file, "r") as f:
                new_cards: dict = json.loads(f.read())
                new_cards: list = [Card(x, new_cards[x]) for x in new_cards]
                self.cards += new_cards
                self.logger.info(f"{len(new_cards)} cards have been loaded.")
        else:
            self.logger.info("File not found.")
        self.remove_handler()

    def export_cards(self, file_name=None):
        self.add_handler()
        if not file_name:
            self.logger.info("File name:")
            file_name = input()
        file = Path(os.path.join(os.path.curdir, file_name))
        with open(file, "w") as f:
            f.write(json.dumps({x.term: x.definition for x in self.cards}))
            self.logger.info(f"{len(self.cards)} cards have been saved.")
        self.remove_handler()

    def log(self):
        self.add_handler()
        self.logger.info("File name:")
        file_name = input()
        file = Path(os.path.join(os.path.curdir, file_name))
        logs = self.stream.getvalue()
        with open(file, "w") as f:
            f.write(logs)
        self.logger.info("The log has been saved.")
        self.remove_handler()

    def hardest_card(self):
        self.add_handler()
        if self.cards:
            largest = max([card.mistake for card in self.cards])
        else:
            largest = None
        if not largest:
            self.logger.info("There are no cards with errors.")
            self.remove_handler()
            return
        hardest: list[Card] = [card for card in self.cards if card.mistake == largest]
        if len(hardest) == 1:
            output = f'is "{hardest[0].term}"'
            card_s = "card"
            it_them = "it"
        else:
            output = f'are "{hardest[0].term}"'
            card_s = "cards"
            it_them = "them"
            for i in hardest[1:]:
                output += f', "{i.term}"'
        self.logger.info(f'The hardest {card_s} {output}. You have {largest} errors answering {it_them}.')
        self.remove_handler()

    def reset(self):
        self.add_handler()
        for card in self.cards:
            card.mistake = 0
        self.logger.info("Card statistics have been reset.")
        self.remove_handler()

    def ask(self):
        self.add_handler()
        self.logger.info("How many times to ask?")
        times = int(input())
        for _ in range(1, times + 1):
            card = random.choice(self.cards)
            self.logger.info(f'{_}: Print the definition of "{card.term}":')
            definition = input()
            if definition == card.definition:
                self.logger.info("Correct!")
            else:
                if definition in Card.definitions:
                    true_card = self.get_by_definition(definition)
                    self.logger.info(
                        f'Wrong. The right answer is "{card.definition}".but your definition is correct for "{true_card.term}".')
                else:
                    self.logger.info(f'Wrong. The right answer is "{card.definition}".')
                card.mistake += 1
        self.remove_handler()

    def get_by_definition(self, given_definition):
        for idx, card in enumerate(self.cards):
            if card.definition == given_definition:
                return card

    def get_by_term(self, given_term):
        for idx, card in enumerate(self.cards):
            if card.term == given_term:
                return card


class Card:
    terms = []
    definitions = []

    def __init__(self, term, definition):
        self.term = term
        self.definition = definition
        self.mistake = 0

    def __new__(cls, term, definition, *args, **kwargs):
        cls.terms.append(term)
        cls.definitions.append(definition)
        return super().__new__(cls)


def get_args() -> dict[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from", required=False)
    parser.add_argument("--export_to", required=False)
    args = parser.parse_args()
    return {"import": args.import_from, "export": args.export_to}


if __name__ == "__main__":
    app = FlashCard()
    app.run()
