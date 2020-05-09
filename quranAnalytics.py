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
        self.handleinput = handleInput()
        self.handleoutput = handleOutput(self.handleinput)
        self.handleplot = handlePlot(self.handleinput, self.handleoutput)
        self.search = search(self.handleinput, self.handleoutput, self.handleplot)
        self.correlations = correlations(self.handleinput, self.handleoutput, self.handleplot, self.search)
        self.networks = networks()

class correlations(quranAnalytics):
    # =============================== Initializer / Instance attributes
    def __init__(self, handleinput, handleoutput, handleplot, search):
        self.corr = pd.DataFrame()
        self.endVerse = 0
        self.handleinput = handleinput
        self.handleoutput = handleoutput
        self.handleplot = handleplot
        self.search = search
        self.startVerse = 0

    # =============================== Calculate correlation matrix of given verse range
    def calculate_correlations(self, colormap = 'cividis', method = 'pearson', opacity = 1, plot = False,
            textOrder = 'official', textType = 'default', verseRange = ['1:1', '114:5'], xticks_rotation = 90, 
            yticks_rotation = 0):
        self.handleinput.preparedata_correlations(textOrder, textType, verseRange)
        if not method in ['pearson', 'kendall', 'spearman']: method = 'pearson'
        
        print("\nSelected correlation method: %s" %method)

        # SQUARE MATRIX
        cnt = 0
        if self.handleinput.isInputRange:
            for i in range(self.handleinput.startVerse, self.handleinput.endVerse + 1):
                self.handleinput.inputdata[i] = self.handleinput.inputdata.iloc[:, i].astype('category').cat.codes # this conversion is needed to calculate correlation with self.corr()
                if cnt % 100 == 0 or i == self.handleinput.endVerse:
                    print("\nVerse %d completed out of %d" %(cnt + 1, self.handleinput.endVerse - self.handleinput.startVerse + 1))
                cnt += 1
        else:
            for i in self.handleinput.selectedVerses: 
                self.handleinput.inputdata[i] = self.handleinput.inputdata.iloc[:, i].astype('category').cat.codes # this conversion is needed to calculate correlation with self.corr()
                if cnt % 100 == 0 or i == self.handleinput.selectedVerses[-1]:
                    print("\nVerse %d completed out of %d" %(cnt + 1, len(self.handleinput.selectedVerses)))
                cnt += 1
        corr2 = self.handleinput.inputdata.corr(method = method) # valid methods: ‘pearson’, ‘kendall’, ‘spearman’. Check out: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html
        self.corr = corr2.dropna()
        self.corr.columns = self.handleinput.inputdata.columns[self.handleinput.startVerse:self.handleinput.endVerse + 1] if self.handleinput.isInputRange else self.handleinput.inputdata.columns[self.handleinput.selectedVerses]
        self.corr.index = self.handleinput.inputdata.columns[self.handleinput.startVerse:self.handleinput.endVerse + 1] if self.handleinput.isInputRange else self.handleinput.inputdata.columns[self.handleinput.selectedVerses]
        if plot: self.handleplot.correlationmatrix(self.corr, colormap, opacity, xticks_rotation, yticks_rotation)
        self.handleoutput.outputdata_write(sys._getframe().f_code.co_name, self.corr)
    
    # =============================== Find correlated verses to a verse given by the user
    def find_correlatedverses(self, numofverses, verse, colormap = 'cividis', method = 'pearson',  opacity = 1, 
            plot = False, textOrder = 'official', textType = 'default', verseRange = ['1:1', '114:5'], xticks_rotation = 90, 
            yticks_rotation = 0):
        self.calculate_correlations(method = method, textOrder = textOrder, 
                textType = textType, verseRange = verseRange)

        # most/least correlated verses to a respective verse
        outputData = []
        corrVersesToAVerse = []
        for i in range(len(self.corr[verse])):
            if self.corr[verse][i] >= 0.9:
                corrVersesToAVerse.append(self.corr.columns[i])
        corrVersesToAVerse = self.corr[verse].sort_values(0)
        # print results on the terminal
        print("\nThe least %d correlated verses to %s:\n%s \n" 
        %(numofverses, verse, 
        corrVersesToAVerse[:numofverses]))
        corrVersesToAVerse = corrVersesToAVerse[::-1] # reverse the array to have the right descending order
        print("\nThe most %d correlated verses to %s:\n%s \n" 
        %(numofverses, verse, 
        corrVersesToAVerse[1:numofverses + 1]))  # +1 is not to show the original verse
        # save results to a txt file
        outputData = list(corrVersesToAVerse.index)
        outputData.append(numofverses)
        outputData.append(verse)
        if plot: self.handleplot.correlationmatrix(self.corr, colormap, opacity, xticks_rotation, yticks_rotation)
        self.handleoutput.outputdata_write(sys._getframe().f_code.co_name, outputData)

    # =============================== Find most and least correlated verses to other verses
    def rank_correlations(self, numofverses, colormap = 'cividis', method = 'pearson', opacity = 1, plot = False, 
            textOrder = 'official', textType = 'default', verseRange = ['1:1', '114:5'], xticks_rotation = 90, 
            yticks_rotation = 0):
        self.calculate_correlations(method = method, textOrder = textOrder, 
                textType = textType, verseRange = verseRange)

        mostLeastCorrVerse = []
        for i in self.corr.columns.tolist():
            mostLeastCorrVerse.append(self.corr[i].sum()) 
        mostLeastCorrVerse = pd.DataFrame(mostLeastCorrVerse, index = self.corr.columns.tolist())
        mostLeastCorrVerse = mostLeastCorrVerse.sort_values(0)
        print("\nThe least %d correlated verse to other verses: %s, Value: %s \n" 
        %(numofverses, mostLeastCorrVerse.columns[:numofverses], 
        mostLeastCorrVerse[:numofverses]))
        mostLeastCorrVerse = mostLeastCorrVerse[::-1] # reverse the array to have the right descending order
        print("\nThe most %d correlated verse to other verses: %s, Value: %s \n" 
        %(numofverses, mostLeastCorrVerse.columns[:numofverses], 
        mostLeastCorrVerse[:numofverses]))
        # save results to a txt file
        outputData = list(mostLeastCorrVerse.index)
        outputData.append(numofverses) 
        if plot: self.handleplot.correlationmatrix(self.corr, colormap, opacity, xticks_rotation, yticks_rotation)
        self.handleoutput.outputdata_write(sys._getframe().f_code.co_name, outputData)

class handleInput(quranAnalytics):
    # =============================== Initializer / Instance attributes
    def __init__(self):
        self.inputdata = []
        self.inputfile_directory = 'inputFiles'
        self.inputfile_format_correlations = '.csv'
        self.inputfile_format_search = '.txt'
        self.inputfile_name = ""
        self.inputfile_name_quran_official_nowovel = 'quran_officialOrder_novowels'
        self.inputfile_name_quran_official_wovel = 'quran_officialOrder_default'
        self.inputfile_name_quran_lemma = 'quran_lemma_officialOrder'
        self.inputfile_name_quran_revelation_nowovel = 'quran_revelationOrder_novowels'
        self.inputfile_name_quran_revelation_wovel = 'quran_revelationOrder_default'
        self.inputfile_name_quran_root = 'quran_root_officialOrder'
        self.isInputRange = False
        self.mypath = os.path.realpath(__file__)
        self.mydirectory = os.path.dirname(self.mypath)
        self.verserange_default = ['1:1', '114:5']

    # =============================== Prepare input data according to verse range given by user
    def preparedata_correlations (self, textOrder, textType, verseRange):
        self.inputdata = pd.DataFrame()
        if textOrder == 'official' and textType == 'default':
            self.inputfile_name = self.inputfile_name_quran_official_wovel + self.inputfile_format_correlations
        elif textOrder == 'revelation' and textType == 'default':
            self.inputfile_name = self.inputfile_name_quran_revelation_wovel + self.inputfile_format_correlations
        elif textOrder == 'revelation' and textType == 'novowel':
            self.inputfile_name = self.inputfile_name_quran_revelation_nowovel + self.inputfile_format_correlations
        else:
            self.inputfile_name = self.inputfile_name_quran_official_nowovel + self.inputfile_format_correlations
        
        print("\nSelected Qur'an database: %s" %self.inputfile_name)
        
        self.inputdata = pd.read_csv(self.mydirectory + os.sep + self.inputfile_directory + os.sep + self.inputfile_name,)
        # Find the col nums of beginning and ending verses
        startVerseFound = False
        endVerseFound = False
        if not len(verseRange) == 0 and len(verseRange) <= 2: self.isInputRange = True
        if len(verseRange) == 1: # a whole chapter
            for i in range(len(self.inputdata.columns)):
                chapter = self.inputdata.columns[i] 
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
            for i in range(len(self.inputdata.columns)):
                if verseRange[0] == self.inputdata.columns[i]:
                    self.startVerse = i
                    startVerseFound = True
                elif verseRange[1] == self.inputdata.columns[i]:
                    self.endVerse = i
                    endVerseFound = True
                if startVerseFound and endVerseFound: break
        elif len(verseRange) > 2: # selection of individual verses
            self.selectedVerses = []
            for j in range(len(verseRange)):
                for i in range(len(self.inputdata.columns)):
                    if verseRange[j] == self.inputdata.columns[i]:
                        self.selectedVerses.append(i)
                        break
                    if i == len(self.inputdata.columns) - 1:
                        print("\n%s could not be found in the database" %verseRange[j])
        else: # user did not provide any input 
            print("\nPlease provide a verse range.")

    # =============================== Prepare input data for search
    def preparedata_search(self, database):
        if database == 'lemma':
            self.inputfile_name = self.inputfile_name_quran_lemma + self.inputfile_format_search
        elif database == 'officialorder':
            self.inputfile_name =  self.inputfile_name_quran_official_wovel + self.inputfile_format_search
        elif database == 'officialorder_novowels':
            self.inputfile_name =  self.inputfile_name_quran_official_nowovel + self.inputfile_format_search
        elif database == 'revelationorder':
            self.inputfile_name =  self.inputfile_name_quran_revelation_wovel + self.inputfile_format_search
        elif database == 'revelationorder_novowels':
            self.inputfile_name =  self.inputfile_name_quran_revelation_nowovel + self.inputfile_format_search
        else: # root database
            self.inputfile_name =  self.inputfile_name_quran_root + self.inputfile_format_search
        
        with open(self.mydirectory + os.sep + self.inputfile_directory + os.sep + self.inputfile_name, 'r', encoding = 'utf-8') as search_data:
            for line in search_data:
                self.inputdata.append(line)

        print("\nSelected Qur'an database: %s" %self.inputfile_name)

    # =============================== validate user inputs
    def validate_inputs(self):
        pass

class handleOutput(quranAnalytics):
    # =============================== Initializer / Instance attributes
    def __init__(self, handleinput):
        self.dateTime = datetime.now().strftime('%Y%m%d_%H%M%S_')
        self.handleinput = handleinput
        self.outputfile_directory = 'outputFiles'
        self.outputfile_encoding = 'utf-8-sig'
        self.outputdata_fileformat_correlations = '.csv'
        self.outputdata_fileformat_search = '.txt'
        self.outputfigure_fileformat = 'pdf'

    # =============================== Write the data to an output file
    def outputdata_write(self, prevFuncName, dataToWrite):
        outputFile_fullDir = self.handleinput.mydirectory + os.sep + self.outputfile_directory + os.sep + self.dateTime + '_' + prevFuncName 
        
        if prevFuncName in 'calculate_correlations':
            dataToWrite.to_csv(outputFile_fullDir + self.outputdata_fileformat_correlations, ' ', encoding = self.outputfile_encoding)
        elif prevFuncName == 'search_keyword':
            with open(outputFile_fullDir + self.outputdata_fileformat_search, 'w', newline = '') as outputFile:
                writer = csv.writer(outputFile)
                writer.writerow(["Total number of occurences: %d" %(len(dataToWrite))])
                writer.writerow(dataToWrite)
        elif prevFuncName == 'correlationmatrix':
            plt.savefig('%s.%s' %(outputFile_fullDir, self.outputfigure_fileformat), 
                    bbox_inches = 'tight', format = self.outputfigure_fileformat) 
        else:
            with open(outputFile_fullDir + self.outputdata_fileformat_correlations, 'w', encoding = self.outputfile_encoding) as outputFile:
                if prevFuncName == 'find_correlatedverses':
                    verse = dataToWrite.pop()
                    numofverses = dataToWrite.pop()
                    outputFile.write("\nThe most %d correlated verses to %s: \n %s \n" %(numofverses,
                    verse, dataToWrite[1:numofverses + 1])) # +1 not to show the original verse
                    dataToWrite = dataToWrite[::-1] # reverse the array to have the right descending order
                    outputFile.write("\nThe least %d correlated verses to %s: \n %s \n" %(numofverses,
                    verse, dataToWrite[:numofverses]))
                elif prevFuncName == 'rank_correlations':
                    numofverses = dataToWrite.pop()
                    outputFile.write("\nThe most %d correlated verse to other verses: \n %s \n" 
                    %(numofverses, dataToWrite[:numofverses]))
                    dataToWrite = dataToWrite[::-1] # reverse the array to have the right descending order
                    outputFile.write("\nThe least %d correlated verse to other verses: \n %s \n" 
                    %(numofverses, dataToWrite[:numofverses]))
        print("Done!")     

class handlePlot(quranAnalytics):
    # =============================== Initializer / Instance attributes
    def __init__(self, handleinput, handleoutput):
        self.handleinput = handleinput
        self.handleoutput = handleoutput

    # =============================== Plot the correlation matrix of given verse range
    def correlationmatrix(self, data, colormap, opacity, xticks_rotation, yticks_rotation):
        sns.heatmap(data, cmap = colormap, alpha = opacity)
        plt.xticks(rotation = xticks_rotation)
        plt.yticks(rotation = yticks_rotation)
        self.handleoutput.outputdata_write(sys._getframe().f_code.co_name, None)
        plt.show()

class networks(quranAnalytics):
    # =============================== Initializer / Instance attributes
    def __init__(self):
        pass
    # =============================== Show correlation of selected verse as a network matrix
    def versenetwork(self):
        pass

class search(quranAnalytics):
    # =============================== Initializer / Instance attributes
    def __init__(self, handleinput, handleoutput, handleplot):
        self.handleinput = handleinput
        self.handleoutput = handleoutput
        self.handleplot = handleplot

    # =============================== Find keyword from database
    def search_keyword(self, keyword, database = 'root', whole_keyword = True):
        self.handleinput.preparedata_search(database)
        interdistance, outputData = [], []
        if not whole_keyword: 
            keyword = keyword.split()
            store_keyword = keyword
            keyword = ''
            for i in range(len(store_keyword)):
                keyword += '(?=.*' + store_keyword[i] + ')'

        cnt_interdistance = 0
        for lines in self.handleinput.inputdata:
            if whole_keyword:
                if (re.search(keyword, lines)):
                    cnt = 0
                    for i in lines:
                        if i == ' ':
                            for j in range(len(re.findall(keyword, lines))): # catch multiple occurences in a verse
                                outputData.append(' ' + lines[:cnt])
                                interdistance.append(cnt_interdistance)
                                cnt_interdistance = 0
                            break
                        cnt += 1
            else:
                if (re.search(keyword, lines)):
                    cnt = 0
                    for i in lines:
                        if i == ' ':
                            for j in range(len(re.findall(keyword, lines))): # catch multiple occurences in a verse
                                outputData.append(' ' + lines[:cnt])
                                interdistance.append(cnt_interdistance)
                                cnt_interdistance = 0
                            break
                        cnt += 1
            cnt_interdistance += 1
        print("Total number of occurences: %d" %(len(outputData)))
        self.handleoutput.outputdata_write(sys._getframe().f_code.co_name, outputData)

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