#!/usr/bin/env python
# encoding: utf-8
"""
rally.py

Created by Brian Lalor on 2011-10-20.
"""

import sys
import os
import unittest

import exceptions
import platform

import httplib2
import urllib
import simplejson as json
import types

from pprint import pprint

CLIENT_INTEGRATION_INFO = {
    'X-RallyIntegrationName': 'ad-hoc Rally SupyBot plugin',
    'X-RallyIntegrationVendor': 'Pearson Education',
    'X-RallyIntegrationVersion': '0.000000000000001β',
    'X-RallyIntegrationOS': platform.platform(),
    'X-RallyIntegrationPlatform': '%s %s', # % (platform.python_implementation(), platform.python_version()),
    'X-RallyIntegrationLibrary': 'work in progress'
}

RALLY_WS_VERSION = '1.27'
BASE_URL = 'https://rally1.rallydev.com/slm/webservice/%s' % (RALLY_WS_VERSION,)

class RallyError(exceptions.Exception):
    pass


class RallyQuery(object):
    def __init__(self, username, password):
        self.__httpConn = httplib2.Http(disable_ssl_certificate_validation = True)
        self.__httpConn.add_credentials(username, password)
    
    
    def __do_query__(self, obj_type, query, fetch = True):
        request_data = {
            'query': query,
        }
        
        if type(fetch) == types.BooleanType:
            request_data['fetch'] = str(fetch).lower()
        elif type(fetch) in (types.TupleType, types.ListType):
            request_data['fetch'] = ",".join(fetch)
        
        _url = "%s/%s.js?%s" % (BASE_URL, obj_type, urllib.urlencode(request_data))
        
        resp, content = self.__httpConn.request(
            _url,
            headers = CLIENT_INTEGRATION_INFO,
        )
        
        if resp['status'] != '200':
            raise RallyError("unexpected response: %s" % (resp['status'],))
        
        query_resp = json.loads(content, 'utf-8')
        
        return query_resp[u'QueryResult']
    
    
    def findArtifactByFormattedId(self, artifact_id, artifact_type = 'artifact'):
        query_result = self.__do_query__(artifact_type, '(FormattedID = ' + artifact_id + ')')
        
        if query_result[u'TotalResultCount'] != 1:
            raise RallyError("expected 1 result, got %d" % (query_result[u'TotalResultCount'],))
        
        return query_result[u'Results'][0]
    


class rallyTests(unittest.TestCase):
    
    def setUp(self):
        self.rq = RallyQuery('brian.lalor@pearson.com', 'password')
    
    
    def tearDown(self):
        self.rq = None
    
    
    def testOne(self):
        pprint(self.rq.findArtifactByFormattedId(u"US42859", 'HierarchicalRequirement'))
        
        self.assertTrue(self.rq != None)
    


if __name__ == '__main__':
    unittest.main()

