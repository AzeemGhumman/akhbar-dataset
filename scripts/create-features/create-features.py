# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 17:53:07 2018
"""
import sys
sys.path.append('features/')
sys.path.append('../common/')
import common

import glob
import pdb
import yaml
import json
import os
import time

startTime = time.time()

if len(sys.argv) is 1:
    print ("Error: Please specify the config file path")
    sys.exit()

# Get config filepath from command-line parameter
configFilePath = sys.argv[1]
# configFilePath = "C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\configurations\\extract-features.yaml"

# Load configuration data
outputFolder, dataset, features = common.loadConfiguration(configFilePath, ["outputFolder", "dataset", "features"])

# Create folder if not exists
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

if not os.path.exists(dataset):
    print ("Error: dataset does not exists")
    exit

# TODO: Should i use list or generator here
# List may take more space but will help with multi-threaded application
datasetDict = list(yaml.safe_load_all(open(dataset)))

for featureName in features:
    # Dynamically load the right feature class
    fetureModule = common.dynamicImport(featureName)
    featureClass = getattr(fetureModule, featureName)()

    print ("Generating feature: " + featureName)
    # Create one file per feature
    featureOutput = []
    for articleDict in datasetDict:
        # Check if all Article elements are present
        if articleDict is None:
            print ("Error: dataset is empty")
            exit

        tempArticle = common.Article()
        for element in vars(tempArticle):
            if element not in articleDict:
                print ("Error: Missing Element " + element + " while processing " + article)

        # Create Article
        article = common.Article(articleDict = articleDict)

        # Extract feature for this articles
        featureDict = {}
        try:
            featureDict["globalID"] = article.globalID
            featureDict["features"] = featureClass.extract(article)
        except:
            print ("Error: while extracting feature " + featureName)

        featureOutput.append(featureDict)

    # Output To File
    fileContents = None
    fileContents = yaml.dump(featureOutput, default_flow_style = False)

    fullPath = os.path.join(outputFolder, featureName + ".yaml")
    outputFile = open(fullPath, 'w+')
    outputFile.write(fileContents)
    outputFile.close()

endTime = time.time()
print ("Time Taken: " + str(endTime - startTime))

print ("Done")
