from src.rag import QualityRAG
def test_search():
    r=QualityRAG();r.fit([{"source":"x","record_id":"1","text":"bore oversize tool offset","metadata":{}},{"source":"x","record_id":"2","text":"scratch handling","metadata":{}}])
    assert r.search("oversize bore offset",1)[0]["record_id"]=="1"
