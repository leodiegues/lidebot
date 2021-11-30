import numpy as np
from datetime import datetime

from lidebot.main import Headline, generate_thread, load_headlines

test_headlines = [
    Headline(
        title="a very very very long title1",
        url="url1",
        collected_at=datetime.strptime("2021-01-01 20:30:10.3242", "%Y-%m-%d %H:%M:%S.%f"),
        source="folha",
    ),
    Headline(
        title="a very very very long title2",
        url="url2",
        collected_at=datetime.strptime("2021-01-01 20:30:10.3242", "%Y-%m-%d %H:%M:%S.%f"),
        source="estadao",
    ),
    Headline(
        title="a very very very long title3",
        url="url3",
        collected_at=datetime.strptime("2021-01-01 20:30:10.3242", "%Y-%m-%d %H:%M:%S.%f"),
        source="oglobo",
    ),
]


def test_load_headlines() -> None:
    headlines = load_headlines("lidebot/tests/test_data")
    assert headlines == test_headlines


def test_generate_thread() -> None:
    small_post = generate_thread(test_headlines)
    long_post = generate_thread(np.repeat(test_headlines, 10))
    assert len(small_post) == 4
    assert len(long_post) > 4
