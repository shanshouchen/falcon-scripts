# Solr Monitor

## 1.  Monitoring metrics

| Metrics |
|---------|
filterCache.stats.hitratio|
filterCache.stats.evictions|
perSegFilter.stats.hitratio|
perSegFilter.stats.evictions|
documentCache.stats.hitratio|
documentCache.stats.evictions|
fieldValueCache.stats.hitratio|
fieldValueCache.stats.evictions|
queryResultCache.stats.hitratio|
queryResultCache.stats.evictions|
jvm.memory.raw.total|
jvm.memory.raw.free|
jvm.memory.raw.max|
jvm.memory.raw.used|
jvm.memory.raw.used.percentage|
system.totalPhysicalMemorySize|
system.freePhysicalMemorySize|



## 2. URl description


To return information and statistics about the CACHE category only, formatted in JSON:
```
solr/%s/admin/mbeans?stats=true&cat=CACHE&wt=json
```


To return system info
```
solr/admin/info/system?wt=json
```


To return cores info
```
solr/admin/cores?wt=json&indexInfo=false
```
