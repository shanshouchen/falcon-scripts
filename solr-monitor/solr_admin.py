#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'shouchen.shan@hotmail.com'

import urlparse
import urllib2
import json
import time
import socket
import urllib


class SolrAdmin:
    SYSTEM_URL = '/solr/admin/info/system?wt=json'
    CORES_URL = '/solr/admin/cores?wt=json&indexInfo=false'
    CACHE_URL_FORMAT = '/solr/%s/admin/mbeans?stats=true&wt=json&cat=CACHE'

    system_map = [
        ('jvm.memory.raw.free', 'jvm.memory.raw.free'),
        ('jvm.memory.raw.total', 'jvm.memory.raw.total'),
        ('jvm.memory.raw.max', 'jvm.memory.raw.max'),
        ('jvm.memory.raw.used', 'jvm.memory.raw.used'),
        ('jvm.memory.raw.used.percentage', 'jvm.memory.raw.used%'),
        ('system.totalPhysicalMemorySize', 'system.totalPhysicalMemorySize'),
        ('system.freePhysicalMemorySize', 'system.freePhysicalMemorySize'),
    ]

    cache_map = [
        ('filterCache.stats.hitratio', 'filterCache.stats.hitratio'),
        ('filterCache.stats.evictions', 'filterCache.stats.evictions'),

        ('perSegFilter.stats.evictions', 'perSegFilter.stats.hitratio'),
        ('perSegFilter.stats.evictions', 'perSegFilter.stats.evictions'),

        ('documentCache.stats.evictions', 'documentCache.stats.hitratio'),
        ('documentCache.stats.evictions', 'documentCache.stats.evictions'),

        ('fieldValueCache.stats.evictions', 'fieldValueCache.stats.hitratio'),
        ('fieldValueCache.stats.evictions', 'fieldValueCache.stats.evictions'),

        ('queryResultCache.stats.evictions', 'queryResultCache.stats.hitratio'),
        ('queryResultCache.stats.evictions', 'queryResultCache.stats.evictions'),
    ]

    _ts = int(time.time())
    _step = 60
    _p = []
    _hostname = socket.gethostname()

    def __init__(self, host):
        self.host = host
        _, port = urllib.splitport(host)
        self._port = port
        print port

    def get_metrics(self):
        self._collect(self._read_solr_response(self.SYSTEM_URL), self.system_map,
                      tags='port=%s' % (self._port,))

        for core in self._get_cores():
            url = self.CACHE_URL_FORMAT % (core,)
            json_response = self._read_solr_response(url)
            detail = self._get_core_detail_info(core)
            tags = 'collection=%s,shard=%s,replica=%s,port=%s' % (
                detail['collection'], detail['shard'], detail['replica'], self._port,)
            self._collect(json_response['solr-mbeans'][1], self.cache_map, tags)
        return self._p

    def _get_cores(self):
        cores = self._read_solr_response(self.CORES_URL)
        return cores['status'].keys()

    def _collect(self, json_dict, entry_map, tags):
        for (key, path) in entry_map:
            self._p.append({
                'endpoint': 'solr.%s' % (self._hostname,),
                'metric': key,
                'value': self._jpath(json_dict, path),
                'timestamp': self._ts,
                'step': self._step,
                'counterType': 'GAUGE',
                'tags': tags,
            })

    def _read_solr_response(self, path):
        url = urlparse.urljoin(self.host, path)
        response = urllib2.urlopen(url).read()
        return json.loads(response)

    def _get_core_detail_info(self, core):
        return {'collection': core[:core.index('_shard')],
                'shard': core[len(core[:core.index('_shard')]) + 1:core.index('_replica')],
                'replica': core[core.index('_replica') + 1:len(core)]}

    def _jpath(self, json_dict, path):
        element = json_dict
        try:
            for x in path.split("."):
                element = element.get(x)
        except:
            pass
        return element
