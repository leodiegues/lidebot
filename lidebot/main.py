import io
import os
import csv
import tweepy
from typing import List
from datetime import datetime
from dataclasses import dataclass

# CONSUMER_KEY = os.environ["CONSUMER_KEY"]
# CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
# ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
# ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


SOURCES = {
    "g1": "G1",
    "folha": "Folha",
    "estadao": "Estadão",
    "veja": "Veja",
    "oglobo": "O Globo",
    "valor": "Valor",
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


def load_headlines(filename: str) -> List[Headline]:
    """
    Carrega as manchetes de um arquivo

    :param filename: Nome do arquivo
    :return: Lista de manchetes
    """
    headlines = []
    with open(filename, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            headline = Headline(
                title=row[0],
                url=row[1],
                collected_at=datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"),
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
            post.append(tweet)
            tweet = new_headline
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


def publish(api: tweepy.API, headlines: List[Headline]) -> List[int]:
    """
    Publica o tweet a partir de uma lista de manchetes

    :param headlines: Lista de manchetes
    :return: Lista de IDs dos tweets publicados
    """
    thread = generate_thread(headlines)
    first_tweet = api.update_status(thread[0])
    tweet_ids = [first_tweet.id]
    for tweet in thread[1:]:
        tweet_id = api.update_status(tweet, in_reply_to_status_id=first_tweet.id)
        tweet_ids.append(tweet_id.id)
    return tweet_ids


if __name__ == "__main__":
    api = authenticate()
    headlines = load_headlines("latest_headlines.txt")
    tweet_ids = publish(api, headlines)
    print(tweet_ids)
