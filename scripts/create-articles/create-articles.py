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
inputFolders = []

print ("Loading config file: " + configFilePath)
# Extract config data from config file
if os.path.exists(configFilePath):
    config = yaml.load(open(configFilePath))

    params = ["outputFolderPath", "outputType", "inputFolders"]
    # Check for elements in the config file
    for param in params:
        if param not in config:
            print("Error: " + param + " missing in config file")
            exit

    outputFolderPath = config["outputFolderPath"]
    outputTypeString = config["outputType"]
    inputFolders = config["inputFolders"]

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
articleSourceFiles = []
for inputFolder in inputFolders:
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


# TODO: only get request for now, otherwise update config file to include post request and post data
for articleSourceFile in articleSourceFiles:
    print ("working on: " + articleSourceFile)
    startTime = time.time()

    globalID = 1
    if os.path.exists(articleSourceFile):
        articleSourceCode = open(articleSourceFile,"r").read()

        # articleName = articleDict["articleName"]
        # articleUrl = articleDict["articleUrl"]
        # publisherName = articleDict["publisher"]
        # articleSourceCode = articleDict["sourceCode"]
        # timeDownloaded = articleDict["timeDownloaded"] # currently not being used

        publisherName = "TheNews" # TODO: find name of publisher based on folder name

        # Dynamically load the right publisher
        publisherModule = dynamicImport(publisherName)
        if publisherModule is None:
            print ("Error: Publisher class '" + publisherName + "' not found" )
            continue
        publisherClass = getattr(publisherModule, publisherName)()

        article = publisherClass.createArticleObject(globalID = str(globalID), articleSourceFilename = articleSourceFile, articleSourceCode = articleSourceCode)

        print ("path: " + outputFolderPath)

        # Save article to disk
        if article is not None:
            article.save(folderPath = outputFolderPath, filename = article.globalID, outputType = outputType)

        endTime = time.time()
        timeTaken = endTime - startTime
        globalID += 1
        print ("file saved. Time taken: " + str("%.2f" % timeTaken))
        # pdb.set_trace()
