import re

from math import ceil


class ArticleReadTimeEngine:

    @staticmethod
    def words_count(text):
        return len(re.findall(r"\w+", text))

    @classmethod
    def estimate_reading_time(
            cls, article, words_per_minute: int = 250, seconds_per_image: int = 10, seconds_per_tag: int = 2
    ):
        words_count_body = cls.words_count(article.body)
        word_count_title = cls.words_count(article.title)
        word_count_description = cls.words_count(article.description)

        total_words_count = word_count_title + word_count_description + words_count_body
        reading_time = total_words_count / words_per_minute

        if article.banner_image:
            reading_time += (seconds_per_image / 60)

        tag_count = article.tags.count()
        reading_time += (tag_count * seconds_per_tag) / 60
        reading_time = ceil(reading_time)

        return reading_time
