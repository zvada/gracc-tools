#!/usr/bin/python

import elasticsearch
from elasticsearch_dsl import Search, A, Q
#import logging
import operator
import sys
import os


#logging.basicConfig(level=logging.WARN)
es = elasticsearch.Elasticsearch(
        ['localhost'],
        timeout=300, use_ssl=False, verify_certs=False)

osg_raw_index = 'gracc.osg.raw-*'

s = Search(using=es, index=osg_raw_index)

# AS* AAF* ARCH* BFAS*
# CRUSH-OSG*
# *.pvt.bridges.*
# comet-*

s = s.query("wildcard",  Host_description="comet-*")
s = s.query("match", ResourceType="Payload")
response = s.execute()

print "Query took %i milliseconds" % response.took

print "Query got %i hits" % response.hits.total

#print response.hits[1].to_dict()

for hit in s.scan():
    print "Updating %s with Host_description = %s, ResouceType = %s to SiteName = %s" % (hit.meta.id, hit.Host_description, hit.ResourceType, hit.SiteName)
    #print "Updating %s with Host_description = %s, ResouceType = %s to Batch" % (hit.meta.id, hit.Host_description, hit.ResourceType)
    es.update(index=hit.meta.index, doc_type=hit.meta.doc_type, id=hit.meta.id, body={'doc': {'Host_description': hit.SiteName}})
    #es.update(index=hit.meta.index, doc_type=hit.meta.doc_type, id=hit.meta.id, body={'doc': {'ResourceType': 'Batch'}})
