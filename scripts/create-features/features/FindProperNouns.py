# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import common
import pdb
import nltk

class FindProperNouns(common.Feature):

    def __init__(self):
        super().__init__()

    def extract(self, article):
        tokens = nltk.word_tokenize(article.text)
        tags = nltk.pos_tag(tokens)
        properNouns = list(set([tag[0] for tag in tags if tag[1].startswith('NNP')]))
        return {"properNouns" : properNouns}
