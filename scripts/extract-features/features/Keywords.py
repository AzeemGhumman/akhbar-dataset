import textrank
from scripts.common import common

class Keywords(common.Feature):
    def __init__(self):
        super().__init__()

    def extract(self, article):
        return {'keywords': textrank.extract_key_phrases(article.text)}
