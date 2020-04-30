#!/usr/bin/env python3.6

import csv
import numpy as np
import math
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import re
import scipy
import seaborn as sns
import scipy
from datetime import datetime

###################### CLASS QUR'AN ANALYTICS
class quranAnalytics:
    # =============================== Initializer / Instance attributes
    def __init__(self):
        self.corr = pd.DataFrame()
        self.dateTime = datetime.now().strftime('%Y%m%d_%H%M%S_')
        self.endVerse = 0
        self.inputData = []
        self.inputFileDir = 'inputFiles'
        self.inputFileName = ""
        self.input_file_format_analytics = '.csv'
        self.input_file_format_search = '.txt'
        self.input_file_name_quran_official_nowovel = 'quran_officialOrder_novowels'
        self.input_file_name_quran_official_wovel = 'quran_officialOrder_default'
        self.input_file_name_quran_lemma = 'quran_lemma_officialOrder'
        self.input_file_name_quran_revelation_nowovel = 'quran_revelationOrder_novowels'
        self.input_file_name_quran_revelation_wovel = 'quran_revelationOrder_default'
        self.input_file_name_quran_root = 'quran_root_officialOrder'
        self.isInputRange = False
        self.myPath = os.path.realpath(__file__)
        self.myDir = os.path.dirname(self.myPath)
        self.outputData_fileFormat_analyze = '.csv'
        self.outputData_fileFormat_search = '.txt'
        self.outputFig_fileFormat = 'pdf'
        self.outputFile_encoding = 'utf-8-sig'
        self.outputFileDir = 'outputFiles'
        self.startVerse = 0

    # =============================== Calculate correlation matrix of given verse range
    def calculateCorrelation (self, method = None):
        if not method in ['pearson', 'kendall', 'spearman']: method = 'pearson'
        
        print("\nSelected correlation method: %s" %method)

        # SQUARE MATRIX
        cnt = 0
        if self.isInputRange:
            for i in range(self.startVerse, self.endVerse + 1):
                self.inputData[i] = self.inputData.iloc[:, i].astype('category').cat.codes # this conversion is needed to calculate correlation with self.corr()
                if cnt % 100 == 0 or i == self.endVerse:
                    print("\nVerse %d completed out of %d" %(cnt + 1, self.endVerse - self.startVerse + 1))
                cnt += 1
        else:
            for i in self.selectedVerses: 
                self.inputData[i] = self.inputData.iloc[:, i].astype('category').cat.codes # this conversion is needed to calculate correlation with self.corr()
                if cnt % 100 == 0 or i == self.selectedVerses[-1]:
                    print("\nVerse %d completed out of %d" %(cnt + 1, len(self.selectedVerses)))
                cnt += 1
        corr2 = self.inputData.corr(method = method) # valid methods: ‘pearson’, ‘kendall’, ‘spearman’. Check out: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html
        self.corr = corr2.dropna()
        self.corr.columns = self.inputData.columns[self.startVerse:self.endVerse + 1] if self.isInputRange else self.inputData.columns[self.selectedVerses]
        self.corr.index = self.inputData.columns[self.startVerse:self.endVerse + 1] if self.isInputRange else self.inputData.columns[self.selectedVerses]
        self.writeOutputData(sys._getframe().f_code.co_name, self.corr)

    # =============================== Show correlation of selected verse as a network matrix
    def drawNetworkOfVerses(self):
        pass

    # =============================== Plot the correlation matrix of given verse range
    def plotCorrelationMatrix (self, colormap = 'cividis', opacity = 1, xticks_rotation = 90, yticks_rotation = 0):
        sns.heatmap(self.corr, cmap = colormap, alpha = opacity)
        plt.xticks(rotation = xticks_rotation)
        plt.yticks(rotation = yticks_rotation)
        self.writeOutputData(sys._getframe().f_code.co_name, None)
        plt.show()

    # =============================== Find correlated verses to a verse given by the user
    def findCorrelatedVersesToAVerse (self, verse, compareVerse_numOfVerses):
        # most/least correlated verses to a respective verse
        outputData = []
        funcAbbrev = 'findCorrelatedVersesToAVerse'
        corrVersesToAVerse = []
        for i in range(len(self.corr[verse])):
            if self.corr[verse][i] >= 0.9:
                corrVersesToAVerse.append(self.corr.columns[i])
        corrVersesToAVerse = self.corr[verse].sort_values(0)
        # print results on the terminal
        print("\nThe least %d correlated verses to %s:\n%s \n" 
        %(compareVerse_numOfVerses, verse, 
        corrVersesToAVerse[:compareVerse_numOfVerses]))
        corrVersesToAVerse = corrVersesToAVerse[::-1] # reverse the array to have the right descending order
        print("\nThe most %d correlated verses to %s:\n%s \n" 
        %(compareVerse_numOfVerses, verse, 
        corrVersesToAVerse[1:compareVerse_numOfVerses + 1]))  # +1 is not to show the original verse
        # save results to a txt file
        outputData = list(corrVersesToAVerse.index)
        outputData.append(compareVerse_numOfVerses)
        outputData.append(verse)
        self.writeOutputData(sys._getframe().f_code.co_name, outputData)

    # =============================== Find most and least correlated verses to other verses
    def least_most_correlatedVersesToOtherVerses (self, mostLeast_numOfVerses):
        mostLeastCorrVerse = []
        for i in self.corr.columns.tolist():
            mostLeastCorrVerse.append(self.corr[i].sum()) 
        mostLeastCorrVerse = pd.DataFrame(mostLeastCorrVerse, index = self.corr.columns.tolist())
        mostLeastCorrVerse = mostLeastCorrVerse.sort_values(0)
        print("\nThe least %d correlated verse to other verses: %s, Value: %s \n" 
        %(mostLeast_numOfVerses, mostLeastCorrVerse.columns[:mostLeast_numOfVerses], 
        mostLeastCorrVerse[:mostLeast_numOfVerses]))
        mostLeastCorrVerse = mostLeastCorrVerse[::-1] # reverse the array to have the right descending order
        print("\nThe most %d correlated verse to other verses: %s, Value: %s \n" 
        %(mostLeast_numOfVerses, mostLeastCorrVerse.columns[:mostLeast_numOfVerses], 
        mostLeastCorrVerse[:mostLeast_numOfVerses]))
        # save results to a txt file
        outputData = list(mostLeastCorrVerse.index)
        outputData.append(mostLeast_numOfVerses)
        self.writeOutputData(sys._getframe().f_code.co_name, outputData)

    # =============================== Prepare input data according to verse range given by user
    def prepareData_analytics (self, verseRange, textOrder = 'official', textType = 'default'):
        self.inputData = pd.DataFrame()
        if textOrder == 'official' and textType == 'default':
            self.inputFileName = self.input_file_name_quran_official_wovel + self.input_file_format_analytics
        elif textOrder == 'revelation' and textType == 'default':
            self.inputFileName = self.input_file_name_quran_revelation_wovel + self.input_file_format_analytics
        elif textOrder == 'revelation' and textType == 'novowel':
            self.inputFileName = self.input_file_name_quran_revelation_nowovel + self.input_file_format_analytics
        else:
            self.inputFileName = self.input_file_name_quran_official_nowovel + self.input_file_format_analytics
        
        print("\nSelected Qur'an database: %s" %self.inputFileName)
        
        self.inputData = pd.read_csv(self.myDir + os.sep + self.inputFileDir + os.sep + self.inputFileName)
        # Find the col nums of beginning and ending verses
        startVerseFound = False
        endVerseFound = False
        if not len(verseRange) == 0 and len(verseRange) <= 2: self.isInputRange = True
        if len(verseRange) == 1: # a whole chapter
            for i in range(len(self.inputData.columns)):
                chapter = self.inputData.columns[i] 
                chapter = chapter.split(':')[0] # https://stackoverflow.com/questions/8247792/python-how-to-cut-a-string-in-python
                if not startVerseFound and verseRange[0] == chapter:
                    self.startVerse = i
                    startVerseFound = True
                elif startVerseFound and not verseRange[0] == chapter:
                    self.endVerse = i - 1
                    endVerseFound = True
                if startVerseFound and endVerseFound: break
        elif len(verseRange) == 2: # a range of verses
            startVerseFound = False
            endVerseFound = False
            for i in range(len(self.inputData.columns)):
                if verseRange[0] == self.inputData.columns[i]:
                    self.startVerse = i
                    startVerseFound = True
                elif verseRange[1] == self.inputData.columns[i]:
                    self.endVerse = i
                    endVerseFound = True
                if startVerseFound and endVerseFound: break
        elif len(verseRange) > 2: # selection of individual verses
            self.selectedVerses = []
            for j in range(len(verseRange)):
                for i in range(len(self.inputData.columns)):
                    if verseRange[j] == self.inputData.columns[i]:
                        self.selectedVerses.append(i)
                        break
                    if i == len(self.inputData.columns) - 1:
                        print("\n%s could not be found in the database" %verseRange[j])
        else: # user did not provide any input 
            print("\nPlease provide a verse range.")

    # =============================== Prepare input data for search
    def prepareData_search(self, database = 'root'):
        if database == 'lemma':
            self.inputFileName = self.input_file_name_quran_lemma + self.input_file_format_search
        elif database == 'officialorder':
            self.inputFileName =  self.input_file_name_quran_official_wovel + self.input_file_format_search
        elif database == 'officialorder_novowels':
            self.inputFileName =  self.input_file_name_quran_official_nowovel + self.input_file_format_search
        elif database == 'revelationorder':
            self.inputFileName =  self.input_file_name_quran_revelation_wovel + self.input_file_format_search
        elif database == 'revelationorder_novowels':
            self.inputFileName =  self.input_file_name_quran_revelation_nowovel + self.input_file_format_search
        else: # root database
            self.inputFileName =  self.input_file_name_quran_root + self.input_file_format_search
        
        with open(self.myDir + os.sep + self.inputFileDir + os.sep + self.inputFileName, 'r') as search_data:
            for line in search_data:
                self.inputData.append(line)

        print("\nSelected Qur'an database: %s" %self.inputFileName)

    # =============================== Find keyword from database
    def search_keyword(self, keyword, whole_keyword = True):
        outputData = []
        if not whole_keyword: 
            keyword = keyword.split()
            store_keyword = keyword
            keyword = ''
            for i in range(len(store_keyword)):
                keyword += '(?=.*' + store_keyword[i] + ')'

        for lines in self.inputData:
            if whole_keyword:
                if (re.search(keyword, lines)):
                    cnt = 0
                    for i in lines:
                        if i == ' ':
                            outputData.append(lines[:cnt])
                            break
                        cnt += 1
            else:
                if (re.search(keyword, lines)):
                    cnt = 0
                    for i in lines:
                        if i == ' ':
                            outputData.append(lines[:cnt])
                            break
                        cnt += 1
        print("Total found number of verses: %d" %(len(outputData)))
        self.writeOutputData(sys._getframe().f_code.co_name, outputData)

    # =============================== Write the data to an output file
    def writeOutputData (self, prevFuncName, dataToWrite):
        outputFile_fullDir = self.myDir + os.sep + self.outputFileDir + os.sep + self.dateTime + '_' + prevFuncName 
        
        if prevFuncName in 'calculateCorrelation':
            dataToWrite.to_csv(outputFile_fullDir + self.outputData_fileFormat_analyze, ' ', encoding = self.outputFile_encoding)
        elif prevFuncName == 'search_keyword':
            with open(outputFile_fullDir + self.outputData_fileFormat_search, 'w', newline = '') as outputFile:
                writer = csv.writer(outputFile)
                writer.writerow(dataToWrite)
        elif prevFuncName == 'plotCorrelationMatrix':
            plt.savefig('%s.%s' %(outputFile_fullDir, self.outputFig_fileFormat), 
                    bbox_inches = 'tight', format = self.outputFig_fileFormat) 
        else:
            with open(outputFile_fullDir + self.outputData_fileFormat_analyze, 'w', encoding = self.outputFile_encoding) as outputFile:
                if prevFuncName == 'findCorrelatedVersesToAVerse':
                    verse = dataToWrite.pop()
                    compareVerse_numOfVerses = dataToWrite.pop()
                    outputFile.write("\nThe most %d correlated verses to %s: \n %s \n" %(compareVerse_numOfVerses,
                    verse, dataToWrite[1:compareVerse_numOfVerses + 1])) # +1 not to show the original verse
                    dataToWrite = dataToWrite[::-1] # reverse the array to have the right descending order
                    outputFile.write("\nThe least %d correlated verses to %s: \n %s \n" %(compareVerse_numOfVerses,
                    verse, dataToWrite[:compareVerse_numOfVerses]))
                elif prevFuncName == 'least_most_correlatedVersesToOtherVerses':
                    mostLeast_numOfVerses = dataToWrite.pop()
                    outputFile.write("\nThe most %d correlated verse to other verses: \n %s \n" 
                    %(mostLeast_numOfVerses, dataToWrite[:mostLeast_numOfVerses]))
                    dataToWrite = dataToWrite[::-1] # reverse the array to have the right descending order
                    outputFile.write("\nThe least %d correlated verse to other verses: \n %s \n" 
                    %(mostLeast_numOfVerses, dataToWrite[:mostLeast_numOfVerses]))
        print("Done!")      

'''
Check these out: 
https://stackoverflow.com/questions/55394673/how-to-find-the-correlation-between-two-strings-in-pandas
https://towardsdatascience.com/a-beginners-guide-to-word-embedding-with-gensim-word2vec-model-5970fa56cc92
https://www.linkedin.com/pulse/what-listening-look-facebooks-ai-engine-radim-%C5%99eh%C5%AF%C5%99ek?articleId=6145755112989134848#comments-6145755112989134848&trk=public_profile_article_view
TODO:
1. Make a column for each verse and add its words in the corresponding column, then find self.corr matrix of the verses
2. Make a column for each chapter and add its verses in the corresponding column, then find self.corr matrix of the chapters
3. Learn word2vec library to calculate the distance between verses and similar verses.
'''