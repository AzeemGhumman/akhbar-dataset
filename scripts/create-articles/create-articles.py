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
from multiprocessing.dummy import Pool as ThreadPool
import threading
import random

startTime = time.time()

if len(sys.argv) is 1:
    print ("Error: Please specify the config file path")
    sys.exit()

# Get config filepath from command-line parameter
configFilePath = sys.argv[1]
# configFilePath = "C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\configurations\\create-articles.yaml"

# Load Configuration data
outputFolderPath, inputSources, chunkSize, threads = common.loadConfiguration(configFilePath, ["outputFolderPath", "inputSources", "chunkSize", "threads"])

# Create folder if not exists
if not os.path.exists(outputFolderPath):
    os.makedirs(outputFolderPath)


# Create a lock for the chunk
lock = threading.Lock()

globalID = 1

def saveChunkToFile(articleChunk):
    global globalID

    chunkFileContents = ""
    for sourceFile, publisher in articleChunk:

        if not os.path.exists(sourceFile):
            print ("Error: file does not exists: " + articleSourceFile)
            continue

        articleSourceCode = open(sourceFile,"r", encoding='utf8').read()

        article, status = publisherModulesDict[publisher].createArticleObject(globalID = None, \
                                                     articleSourceFilename = sourceFile, \
                                                     articleSourceCode = articleSourceCode)

        # Write file to dataset only if status is empty
        if len(status) > 0:
            print ("File: " + sourceFile)
            print (status)
            continue

        lock.acquire()
        article.globalID = globalID
        globalID += 1
        lock.release()

        yamlOutput = "---\n" + yaml.dump(article.__dict__, default_flow_style = False) + "\n"
        chunkFileContents += yamlOutput

    # TODO: get unique file id of chunk
    fullPath = os.path.join(outputFolderPath, "dataset-" + str(random.getrandbits(128)) + ".yaml")
    outputFile = open(fullPath, 'w+')
    outputFile.write(chunkFileContents)
    outputFile.close()

    # print (chunkFileContents)


# def saveArticleToDataset(articleSourceFile):
#     # global fileID
#     global globalID
#     global chunkFileContents
#     # global lock
#
#     sourceFile, publisher = articleSourceFile
#
#
#     if not os.path.exists(sourceFile):
#         print ("Error: file does not exists: " + articleSourceFile)
#         return
#
#     articleSourceCode = open(sourceFile,"r", encoding='utf8').read()
#
#     article, status = publisherModulesDict[publisher].createArticleObject(globalID = None, \
#                                                          articleSourceFilename = sourceFile, \
#                                                          articleSourceCode = articleSourceCode)
#
#     # Write file to dataset only if status == ""
#     if len(status) > 0:
#         print ("File: " + sourceFile)
#         print (status)
#         return
#
#     # lock.acquire()
#     # setting the globalID here instead of article constructor to enable multiple thread create articles
#     # without worrying about unique globalIDs
#     article.globalID = globalID
#     yamlOutput = "---\n" + yaml.dump(article.__dict__, default_flow_style = False) + "\n"
#     chunkFileContents.append(yamlOutput)
#     globalID += 1
#
#     pdb.set_trace()
#
#     # # Add publisher count
#     # if publisherName in publisherCounts:
#     #     publisherCounts[publisherName] += 1
#     # else:
#     #     publisherCounts[publisherName] = 0
#     #
#     lock.release()

# Get a list of article files
'''
File filtered on 3 parameters
- must end with .html
- must be larger than 3KB in size
- cannot have amp as a folder in its path
'''

publisherCounts = {}
fileID = 1
globalID = 1

datasetForCurrentFeature = []
articleSourceFiles = []
publisherModulesDict = {}

for inputSource in inputSources:

    publisherName = inputSource['publisher']
    inputFolder = inputSource['folder']


    for filename in glob.iglob(inputFolder + '/**/*.html', recursive=True):
        if "/amp/" not in filename and "\\amp\\" not in filename:
            if os.path.getsize(filename) > 3 * 1024:
                articleSourceFiles.append((filename, publisherName))

    # Dynamically load publishers that are seen for the first time
    if publisherName not in publisherModulesDict:
        publisherModule = common.dynamicImport(publisherName)
        if publisherModule is None:
            print ("Error: Publisher class '" + publisherName + "' not found" )
            continue
        publisherModulesDict[publisherName] = getattr(publisherModule, publisherName)()


articleChunks = [articleSourceFiles[i:i + chunkSize] for i in range(0, len(articleSourceFiles), chunkSize)]

# Make the Pool of workers
pool = ThreadPool(threads)
# Extract Feature for given article
pool.map(saveChunkToFile, articleChunks)
# Close the pool and wait for the work to finish
pool.close()
pool.join()

endTime = time.time()
print ("Time taken: " + str(endTime - startTime) + " for " + str(globalID) + " articles\n\n")
# print ("Summary: ")
# for publisher in publisherCounts:
#     print ("name: " + str(publisher) + ", count: " + str(publisherCounts[publisher]))

print ("\nDone")

'''


    # Logic:
    # For each file:
    #     get the file contents
    #     get publisher name
    #     create article object
    #     log errors and warnings
    #     save article object in output folder in yaml/json format


    # for articleSourceFile in articleSourceFiles:
    #     saveArticleToDataset(articleSourceFile)

    # Make the Pool of workers
    pool = ThreadPool(threads)
    # Extract Feature for given article
    featureForDataset = pool.map(saveArticleToDataset, articleSourceFiles)
    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

# Add left over articles to a new dataset file
if len(datasetForCurrentFeature) > 0:
    fullPath = os.path.join(outputFolderPath, "dataset-" + str(fileID) + ".yaml")
    outputFile = open(fullPath, 'w+')
    outputFile.write("\n".join(datasetForCurrentFeature))
    outputFile.close()

endTime = time.time()
print ("Time taken: " + str(endTime - startTime) + " for " + str(globalID) + " articles\n\n")
print ("Summary: ")
for publisher in publisherCounts:
    print ("name: " + str(publisher) + ", count: " + str(publisherCounts[publisher]))

'''

print ("\nDone")
