#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'shouchen.shan@hotmail.com'

from solr_admin import SolrAdmin
import urllib2
import json

# Multiple instances on a host
servers = ['http://127.0.0.1:8983', 'http://127.0.0.1:8984', 'http://127.0.0.1:8985']


def push_data(content):
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = 'http://127.0.0.1:1988/v1/push'
    request = urllib2.Request(url, data=json.dumps(content))
    request.add_header("Content-Type", 'application/json')
    request.get_method = lambda: "POST"
    try:
        connection = opener.open(request)
    except urllib2.HTTPError, e:
        connection = e

    if connection.code == 200:
        print connection.read()
    else:
        print '{"error":1,"message":"%s"}' % connection


for server in servers:
    solrAdmin = SolrAdmin(server)
    data = solrAdmin.get_metrics()
    print json.dumps(data)
    push_data(data)
