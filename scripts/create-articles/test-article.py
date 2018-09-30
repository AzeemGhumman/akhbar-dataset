# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 16:22:20 2018
"""

import sys
sys.path.append('publishers/')
sys.path.append('../common/')
import common

import os
import yaml
import glob
import time
import pdb
import random

def dynamicImport(name):
    try:
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    except:
        return None

articleSourceFile = "/Users/aghumman/Desktop/newspapers/akhbar-dataset/artifacts/source-code/geo-156294.html"
publisherName = "Geo"

articleSourceCode = open(articleSourceFile,"r", encoding='utf8').read()
publisherModule = dynamicImport(publisherName)
publisherClass = getattr(publisherModule, publisherName)()
article, status = publisherClass.createArticleObject(globalID = 1, articleSourceFilename = articleSourceFile, articleSourceCode = articleSourceCode)

print (status)

yamlOutput = "---\n" + yaml.dump(article.__dict__, default_flow_style = False) + "\n"
print (yamlOutput)
