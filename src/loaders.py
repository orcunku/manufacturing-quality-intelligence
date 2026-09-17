from pathlib import Path
import io, pandas as pd
from pypdf import PdfReader
from docx import Document

def s(v): return "" if pd.isna(v) else " ".join(str(v).split())

def frame_records(df,source):
    out=[]
    for i,row in df.fillna("").iterrows():
        md={str(c):s(row[c]) for c in df.columns}
        rid=md.get("NCR_ID") or md.get("CAPA_ID") or md.get("SCRAP_ID") or str(i+1)
        text="\n".join(f"{k}: {v}" for k,v in md.items() if v)
        if text: out.append({"source":source,"record_id":rid,"text":text,"metadata":md})
    return out

def load_file(name,raw):
    ext=Path(name).suffix.lower(); bio=io.BytesIO(raw)
    if ext==".csv": return frame_records(pd.read_csv(bio),name)
    if ext in {".xlsx",".xlsm"}:
        xls=pd.ExcelFile(bio); out=[]
        for sh in xls.sheet_names: out+=frame_records(pd.read_excel(xls,sh),f"{name}::{sh}")
        return out
    if ext==".pdf":
        out=[]
        for i,p in enumerate(PdfReader(bio).pages):
            t=(p.extract_text() or "").strip()
            if t: out.append({"source":name,"record_id":f"page-{i+1}","text":t,"metadata":{"Page":str(i+1)}})
        return out
    if ext==".docx":
        t="\n".join(p.text for p in Document(bio).paragraphs if p.text.strip())
        return [{"source":name,"record_id":"document","text":t,"metadata":{}}] if t else []
    if ext in {".txt",".md"}:
        t=raw.decode("utf-8",errors="ignore")
        return [{"source":name,"record_id":"document","text":t,"metadata":{}}] if t.strip() else []
    raise ValueError(f"Unsupported file type: {ext}")

def chunk(records,size=2200,overlap=250):
    out=[]
    for r in records:
        if len(r["text"])<=size: out.append(r); continue
        start=0;n=1
        while start<len(r["text"]):
            x=dict(r); x["text"]=r["text"][start:start+size]; x["record_id"]=f'{r["record_id"]}-c{n}'
            out.append(x)
            if start+size>=len(r["text"]): break
            start+=size-overlap;n+=1
    return out
