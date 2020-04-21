#!/usr/bin/env python3.6

import quranAnalytics

verseRange = ['1:1', '114:5']

quran_api = quranAnalytics.quranAnalytics()
quran_api.prepareData_search(database = 'root')
quran_api.search_keyword('rsl ktb', whole_keyword = False)
#quran_api.calculateCorrelation()
#quran_api.least_most_correlatedVersesToOtherVerses(10)
#quran_api.findCorrelatedVersesToAVerse('2:1', 6)
#quran_api.plotCorrelationMatrix()
