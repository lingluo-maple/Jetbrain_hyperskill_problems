import string
import os

import requests

from pathlib import Path
from bs4 import BeautifulSoup


def main():
    pages = int(input(">"))
    require_type = input(">")
    print("Running")
    for page in range(1, pages + 1):
        path = Path(f"Page_{page}")
        if not path.exists():
            os.mkdir(path)
        url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page}"
        rep = requests.get(url)
        if rep.status_code != 200:
            print(f"The URL returned {rep.status_code}")
            return
        soup = BeautifulSoup(rep.content, "html.parser")
        articles = soup.find_all("article")

        print("Downloading")
        for article in articles:
            title = article.find("a", {"class": "c-card__link u-link-inherit"}).text
            article_type = article.find("span", {"class": "c-meta__type"}).text
            if article_type == require_type:
                new_url = article.find("a", {"class": "c-card__link u-link-inherit"}).get("href")
                name = title.replace(" ", "_").lower()
                new_word = []
                for i in name:
                    if i in string.punctuation and i != "_":
                        continue
                    else:
                        new_word.append(i)
                name = "".join(new_word) + ".txt"
                file = Path(name)
                content = get_content(new_url)
                if content:
                    with open(os.path.join(path, file), "w", encoding="utf8") as f:
                        f.write(content)
        print(f"Finish {page}")
    print("Finish ALL")


def get_content(url) -> str:
    rep = requests.get(f"https://www.nature.com{url}")
    soup = BeautifulSoup(rep.content, "html.parser")
    try:
        body = soup.find("div", {"class": "c-article-body"}).text
    except AttributeError:
        body = None
    return body


if __name__ == "__main__":
    main()
