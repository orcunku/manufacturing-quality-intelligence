import pandas as pd
def frame(records): return pd.DataFrame([{"source":r["source"],"record_id":r["record_id"],**r.get("metadata",{})} for r in records])
def col(df,*names):
    m={str(c).lower():c for c in df.columns}
    return next((m[n.lower()] for n in names if n.lower() in m),None)
def num(df,*names):
    c=col(df,*names)
    return pd.to_numeric(df[c],errors="coerce").fillna(0) if c else pd.Series([0]*len(df),index=df.index)
def pareto(df):
    d=col(df,"Defect","Defect_Type","Failure_Mode")
    if not d:return pd.DataFrame()
    q=col(df,"Scrap_Qty","Scrap Quantity","Qty","Quantity")
    p=(df.assign(_v=pd.to_numeric(df[q],errors="coerce").fillna(0)).groupby(d)["_v"].sum() if q else df.groupby(d).size())
    p=p.sort_values(ascending=False).reset_index(name="Impact")
    p["Cumulative %"]=100*p["Impact"].cumsum()/max(p["Impact"].sum(),1)
    return p
