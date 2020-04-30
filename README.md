# QuranAnalytics

```diff
- README to be written later. 
```

For search functions, you must call:
- quranAnalytics.quranAnalytics()
- prepareData_search()

For analytics functions, you must define a range of verses and call:
- e.g. verseRange = ['2:15', '3:30'] (range from 2:15 to 3:30) OR ['2'] (whole chapter of Bakarah) OR ['1:4', '2:245', '11:1', '13:6'] (individual verses)
- quranAnalytics.quranAnalytics()
- prepareData_analytics(verseRange)
- calculateCorrelation()

An example usage can be found in *test.py*. 