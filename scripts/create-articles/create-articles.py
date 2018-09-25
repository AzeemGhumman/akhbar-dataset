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

kSubsetTestArticles = 5

def dynamicImport(name):
    try:
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    except:
        return None

if len(sys.argv) is 1:
    print ("Error: Please specify the config file path")
    sys.exit()

# Get config filepath from command-line parameter
configFilePath = sys.argv[1]
# configFilePath = "C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\configurations\\create-articles.yaml"


publisher = None
folderPath = None
outputTypeString = None
inputSources = []

print ("Loading config file: " + configFilePath)
# Extract config data from config file
if os.path.exists(configFilePath):
    config = yaml.load(open(configFilePath))

    params = ["outputFolderPath", "outputType", "inputSources"]
    # Check for elements in the config file
    for param in params:
        if param not in config:
            print("Error: " + param + " missing in config file")
            exit

    outputFolderPath = config["outputFolderPath"]
    outputTypeString = config["outputType"]
    inputSources = config["inputSources"]

else:
    print ("config file does not exist")
    exit

# Create folder if not exists
if not os.path.exists(outputFolderPath):
    os.makedirs(outputFolderPath)

# Set output type
outputType = None
if outputTypeString.lower() == "yaml":
    outputType = common.OutputType.YAML
elif outputTypeString.lower() == "json":
    outputType = common.OutputType.JSON

# Get a list of article files
'''
File filtered on 3 parameters
- must end with .html
- must be larger than 3KB in size
- cannot have amp as a folder in its path
'''

# Create and clean the output dataset.yaml file
fullPath = os.path.join(outputFolderPath, "dataset.yaml")
outputFile = open(fullPath, 'w+')
outputFile.close()

globalID = 1
for inputSource in inputSources:

    publisherName = inputSource['publisher']
    inputFolder = inputSource['folder']

    articleSourceFiles = []
    for filename in glob.iglob(inputFolder + '/**/*.html', recursive=True):
        if "/amp/" not in filename and "\\amp\\" not in filename:
            if os.path.getsize(filename) > 3 * 1024:
                articleSourceFiles.append(filename)
    '''
    Logic:
    For each file:
        get the file contents
        get publisher name
        create article object
        log errors and warnings
        save article object in output folder in yaml/json format
    '''

    articleSubsetForTesting = random.sample(articleSourceFiles, kSubsetTestArticles)
    print ("\n-----------------------------")
    print ("Publisher: " + publisherName)
    print ("-----------------------------\n")
    for articleSourceFile in articleSubsetForTesting:
        print ("\nworking on: " + articleSourceFile)
        startTime = time.time()

        if os.path.exists(articleSourceFile):
            articleSourceCode = open(articleSourceFile,"r", encoding='utf8').read()

            # Dynamically load the right publisher
            publisherModule = dynamicImport(publisherName)
            if publisherModule is None:
                print ("Error: Publisher class '" + publisherName + "' not found" )
                continue
            publisherClass = getattr(publisherModule, publisherName)()

            article, status = publisherClass.createArticleObject(globalID = globalID, articleSourceFilename = articleSourceFile, articleSourceCode = articleSourceCode)

            print (status)

            yamlOutput = "---\n" + yaml.dump(article.__dict__, default_flow_style = False) + "\n"

            globalID += 1 # TODO: Dont increment globalID if the current article is not going to be added to the dataset

            # Add article to dataset
            # TODO: Dont add article to dataset if an error occurred while parsing

            # TODO: Suppress the console outputs when working on the full dataset

            fullPath = os.path.join(outputFolderPath, "dataset.yaml")
            outputFile = open(fullPath, 'a')
            outputFile.write(yamlOutput)
            outputFile.close()

print ("Done")
