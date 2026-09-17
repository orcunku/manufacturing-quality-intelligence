import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class QualityRAG:
    def __init__(self): self.records=[];self.v=None;self.m=None
    def fit(self,records):
        self.records=records
        if not records: self.v=self.m=None;return
        self.v=TfidfVectorizer(stop_words="english",ngram_range=(1,2),sublinear_tf=True,max_features=60000)
        self.m=self.v.fit_transform([r["text"] for r in records])
    def search(self,q,k=6):
        if self.m is None or not q.strip(): return []
        scores=cosine_similarity(self.v.transform([q]),self.m).ravel()
        idx=np.argsort(scores)[::-1][:k]
        return [{**self.records[i],"score":float(scores[i])} for i in idx if scores[i]>0]

def get(md,*names):
    low={k.lower():v for k,v in md.items()}
    for n in names:
        if low.get(n.lower()): return low[n.lower()]
    return ""

def cause_category(text):
    t=str(text).lower()
    rules={"Machine":["tool","wear","die","fixture","machine","insert","wheel"],
           "Method":["procedure","setup","offset","process","changeover","inspection overdue","work instruction"],
           "Material":["material","o-ring","seal","raw material"],
           "Measurement":["gauge","measurement","calibration","control limit"],
           "Man":["operator","training","manual","skipped","entered"],
           "Environment":["coolant","temperature","humidity","contamination","chip buildup"]}
    scores={c:sum(w in t for w in ws) for c,ws in rules.items()}
    return max(scores,key=scores.get) if max(scores.values()) else "Method"

def investigate(issue,hits):
    def unique(field):
        vals=[]
        for h in hits:
            v=get(h.get("metadata",{}),*field)
            if v and v not in vals: vals.append(v)
        return vals[:4]
    roots=unique(("Root_Cause","Root Cause"))
    conf="High" if hits and hits[0]["score"]>=.35 else "Medium" if hits and hits[0]["score"]>=.15 else "Low"
    return {
      "roots":roots,
      "containment":unique(("Containment",)),
      "corrective":unique(("Corrective_Action","Corrective Action")),
      "preventive":unique(("Preventive_Action","Preventive Action")),
      "confidence":conf,
      "whys":[
        f"Problem observed: {issue}",
        f"Historical evidence suggests: {roots[0] if roots else 'cause not yet established'}.",
        "The failure condition was able to reach the process because the relevant prevention/detection control may not have been effective.",
        "Verify whether standard work, setup controls, maintenance, measurement and escalation were followed and capable.",
        "Confirm the system-level cause with objective shop-floor evidence before approving CAPA."
      ],
      "gaps":["Confirm the occurrence point and last known good condition.",
              "Verify suspected cause using objective evidence or controlled trial.",
              "Define owner, due date, verification method and effectiveness check."]
    }
