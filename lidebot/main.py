import io
import os
import csv
import tweepy
import argparse
from typing import List
from datetime import datetime
from dataclasses import dataclass

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


SOURCES = {
    "g1": "G1",
    "folha": "Folha",
    "estadao": "Estadão",
    "veja": "Veja",
    "oglobo": "O Globo",
    "valor": "Valor",
    "uol": "UOL",
}


@dataclass
class Headline:
    """
    Classe para armazenar as informações de uma manchete.

    :param title: Título da manchete.
    :param url: Link da manchete.
    :param collected_at: Data em que a manchete foi coletada.
    :param source: Fonte da manchete.
    """

    title: str
    url: str
    collected_at: datetime
    source: str

    def as_csv(self) -> str:
        """
        Retorna uma string com os dados da manchete formatados para ser
        salva no arquivo CSV.

        :return: String formatada.
        """
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([self.title, self.url, self.collected_at, self.source])
        return output.getvalue()


def load_headlines(directory: str) -> List[Headline]:
    """
    Carrega as manchetes de um arquivo

    :param filename: Nome do arquivo
    :return: Lista de manchetes
    """
    headlines = []
    hl_files = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")
    ]
    for f in hl_files:
        with open(f, "r") as f:
            spamreader = csv.reader(f, delimiter=",")
            next(spamreader)
            for row in spamreader:
                if row[0] == "":
                    continue
                headline = Headline(
                    title=row[0].strip(),
                    url=row[1],
                    collected_at=datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f"),
                    source=row[3],
                )
                headlines.append(headline)
    return headlines


def generate_thread(headlines: List[Headline]):
    """
    Gera o tweet a partir de uma lista de manchetes

    :param headlines: Lista de manchetes
    :return: Tweet
    """
    headlines = sorted(headlines, key=lambda h: h.source)
    post = []
    tweet = ""
    for i, headline in enumerate(headlines):
        source = SOURCES[headline.source]
        new_headline = f"{source}: {headline.title}\n\n"
        if len(tweet + new_headline) > 280:
            post.append(tweet + "\n+")
            tweet = ""
        tweet += new_headline
        if i == len(headlines) - 1:
            post.append(tweet)
    post = [*post, *[hl.url for hl in headlines]]
    return post


def authenticate() -> tweepy.API:
    """
    Autentica o usuário no Twitter

    :return: API do Twitter
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def publish_thread(api: tweepy.API, headlines: List[Headline]) -> List[int]:
    """
    Publica o tweet a partir de uma lista de manchetes

    :param headlines: Lista de manchetes
    :return: Lista de IDs dos tweets publicados
    """
    thread = generate_thread(headlines)
    first_tweet = api.update_status(thread[0])
    last_tweet_id = first_tweet.id
    tweet_ids = [first_tweet.id]
    for tweet in thread[1:]:
        tweet_id = api.update_status(tweet, in_reply_to_status_id=last_tweet_id)
        tweet_ids.append(tweet_id.id)
        last_tweet_id = tweet_id.id
    return tweet_ids


def delete_thread(api: tweepy.API, tweet_ids: List[int]) -> None:
    """
    Deleta os tweets a partir de uma lista de IDs

    :param tweet_ids: Lista de IDs dos tweets
    :return: None
    """
    for tweet_id in tweet_ids:
        api.destroy_status(tweet_id)


def parse_args() -> argparse.Namespace:
    """
    Parse os argumentos da linha de comando
    """
    parser = argparse.ArgumentParser(description="lidebot")
    parser.add_argument(
        "--option", "-o", type=str, help="option", choices=["publish", "delete"]
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    if args.option == "publish":
        api = authenticate()
        headlines = load_headlines("data")
        tweet_ids = publish_thread(api, headlines)
        with open("data/latest_thread.txt", "w") as f:
            for tweet_id in tweet_ids:
                f.write(str(tweet_id) + "\n")
    elif args.option == "delete":
        api = authenticate()
        with open("data/latest_thread.txt", "r") as f:
            tweet_ids = [int(line) for line in f.readlines()]
        delete_thread(api, tweet_ids)
    else:
        raise ValueError("Invalid option")
