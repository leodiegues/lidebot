from datetime import datetime
from publish_tweet import Headline, generate_post


headlines = [
    Headline(
        title="a very very very long title1",
        url="url1",
        collected_at=datetime.now(),
        source="source1",
    ),
    Headline(
        title="a very very very long title2",
        url="url2",
        collected_at=datetime.now(),
        source="source2",
    ),
    Headline(
        title="a very very very long title3",
        url="url3",
        collected_at=datetime.now(),
        source="source3",
    ),
    Headline(
        title="a very very very long title4",
        url="url4",
        collected_at=datetime.now(),
        source="source4",
    ),
    Headline(
        title="a very very very long title5",
        url="url5",
        collected_at=datetime.now(),
        source="source5",
    ),
    Headline(
        title="a very very very long title6",
        url="url6",
        collected_at=datetime.now(),
        source="source6",
    ),
    Headline(
        title="a very very very long title6",
        url="url6",
        collected_at=datetime.now(),
        source="source6",
    ),
    Headline(
        title="a very very very long title6",
        url="url6",
        collected_at=datetime.now(),
        source="source6",
    ),
    Headline(
        title="a very very very long title6",
        url="url6",
        collected_at=datetime.now(),
        source="source6",
    ),
    Headline(
        title="a very very very long title6",
        url="url6",
        collected_at=datetime.now(),
        source="source6",
    ),
    Headline(
        title="a very very very long title6",
        url="url6",
        collected_at=datetime.now(),
        source="source6",
    ),
    Headline(
        title="a very very very long title6",
        url="url6",
        collected_at=datetime.now(),
        source="source6",
    ),
]

post = generate_post(headlines)
print(len(post))
print(post)
