import argparse
from whoosh import index
from whoosh.fields import *
from whoosh.qparser import QueryParser


argParser = argparse.ArgumentParser(description='Full text search')
argParser.add_argument('-q', action='append', help='query to lookup (one or more)')
args = argParser.parse_args()

indexpath = "/tmp/findex"
schema = Schema(path=ID(stored=True, unique=True), content=TEXT)

ix = index.open_dir(indexpath)

if args.q:
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(" ".join(args.q))
        results = searcher.search(query, limit=None)
        for x in results:
            print x['path']
