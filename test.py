#!/usr/bin/env python3.6

import quranAnalytics

##### Search #####
'''
quran_api = quranAnalytics.quranAnalytics()
quran_api.prepareData_search(database = 'root')
quran_api.search_keyword('nbA ktb', whole_keyword = False)
'''

##### Analytics #####
verseRange = ['2:15', '2:45']
quran_api = quranAnalytics.quranAnalytics()
quran_api.prepareData_analytics(verseRange)
quran_api.calculateCorrelation()
#quran_api.least_most_correlatedVersesToOtherVerses(10)
#quran_api.findCorrelatedVersesToAVerse('2:16', 6)
#quran_api.plotCorrelationMatrix()
