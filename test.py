#!/usr/bin/env python3.6


import quranAnalytics

##### Search #####
verseRange = ['2:15', '2:45']
quran_api = quranAnalytics.quranAnalytics()
quran_api.search.search_keyword('muwsaY`', database = 'lemma', whole_keyword = True)
# quran_api.correlations.calculate_correlations(verseRange = verseRange, plot = True)
# quran_api.correlations.rank_correlations(10, verseRange = verseRange, plot = False)
# quran_api.correlations.find_correlatedverses(10, '2:20', verseRange = verseRange, plot = False)

##### Analytics #####
'''
verseRange = ['2:15', '2:45']
quran_api = quranAnalytics.quranAnalytics()
quran_api.prepareData_analytics(verseRange)
quran_api.calculateCorrelation()
#quran_api.least_most_correlatedVersesToOtherVerses(10)
#quran_api.findCorrelatedVersesToAVerse('2:16', 6)
#quran_api.plotCorrelationMatrix()
'''