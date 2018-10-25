import spacy
from scripts.common import common


class nameEntity(common.Feature):
    def __init__(self):
        super().__init__()
        self.eng_model = 'en_core_wen_lg'
        self.nlp = spacy.load(self.eng_model)

    def extract(self, article):
        doc = self.nlp(article.text)
        return {'entity': [x.text for x in doc.ents], 'label': [x.label_ for x in doc.ents]}
