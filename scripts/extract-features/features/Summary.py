import textrank
from scripts.common import common


class Summary(common.Feature):
    def __init__(self):
        super().__init__()

    def extract(self, article):
        return {'summary': textrank.extract_key_phrases(article.text)}
