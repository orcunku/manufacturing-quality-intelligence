from pathlib import Path
import streamlit as st, pandas as pd, plotly.express as px, plotly.graph_objects as go
from src.ui import setup,hero,kpi
from src.loaders import load_file,chunk
from src.rag import QualityRAG,investigate,cause_category
from src.analytics import frame,col,num,pareto
setup()
if "records" not in st.session_state: st.session_state.records=[]
if "rag" not in st.session_state: st.session_state.rag=QualityRAG()
def index(rs): st.session_state.records=chunk(rs);st.session_state.rag.fit(st.session_state.records)

with st.sidebar:
    st.markdown("## ⚙️ Quality Intelligence");st.caption("NCR · CAPA · Scrap")
    page=st.radio("Navigation",["Dashboard","New Investigation","Ask Quality RAG","Similar Cases","NCR Records","CAPA Management","Scrap Analysis","Analytics & Reports","Data Management"],label_visibility="collapsed")
    st.divider()
    records=st.session_state.records
    if records:
        df=frame(records)
        def options(*n):
            c=col(df,*n);return ["All"]+sorted(df[c].dropna().astype(str).unique().tolist()) if c else ["All"]
        st.markdown("### Quick filters")
        fp=st.selectbox("Part / Product",options("Part","Product"));fpr=st.selectbox("Process",options("Process"))
        fm=st.selectbox("Machine",options("Machine"));fd=st.selectbox("Defect",options("Defect","Defect_Type"));fs=st.selectbox("Status",options("Status"))
    st.divider();st.caption("Manufacturing Excellence\n\nBetter Quality · Higher Uptime")

records=st.session_state.records; df=frame(records) if records else pd.DataFrame(); view=df.copy()
if records:
    for val,names in [(fp,("Part","Product")),(fpr,("Process",)),(fm,("Machine",)),(fd,("Defect","Defect_Type")),(fs,("Status",))]:
        c=col(view,*names)
        if c and val!="All":view=view[view[c].astype(str)==val]

if page=="Data Management":
    hero("Data Management","Load controlled quality history into this demo session.")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("### Factory demo dataset")
        st.write("Use the included realistic NCR/CAPA/Scrap dataset to explore every screen.")
        if st.button("Load sample factory dataset",type="primary"):
            p=Path("data/sample/quality_events.csv");index(load_file(p.name,p.read_bytes()));st.success("Sample dataset indexed. Select Dashboard.")
    with c2:
        st.markdown("### Upload your quality records")
        up=st.file_uploader("CSV · XLSX · XLSM · PDF · DOCX · TXT · MD",type=["csv","xlsx","xlsm","pdf","docx","txt","md"],accept_multiple_files=True)
        if st.button("Index uploaded files"):
            rs=[]
            for f in up or []:
                try:rs+=load_file(f.name,f.getvalue())
                except Exception as e:st.error(f"{f.name}: {e}")
            if rs:index(rs);st.success(f"Indexed {len(st.session_state.records)} records/chunks.")
    if records:st.dataframe(df.head(30),use_container_width=True,hide_index=True)

elif not records:
    hero("NCR / CAPA / Scrap Root-Cause Analysis","Factory quality intelligence · evidence retrieval · recurrence prevention.")
    st.info("Select **Data Management** in the left navigation and load the sample factory dataset.")

elif page=="Dashboard":
    hero("NCR / CAPA / Scrap Root-Cause Analysis","Turn quality data into actionable insights with evidence-grounded analysis.")
    sc=col(view,"Status");dc=col(view,"Defect","Defect_Type")
    total=len(view);scrap=int(num(view,"Scrap_Qty","Qty").sum())
    openx=int(view[sc].astype(str).str.lower().isin(["open","in progress"]).sum()) if sc else 0
    recur=int((view[dc].value_counts()>1).sum()) if dc else 0
    closed=int(view[sc].astype(str).str.lower().eq("closed").sum()) if sc else 0
    vals=[("Total NCRs",total,"current filtered view"),("Open CAPAs",openx,"open / in progress"),("Scrap Quantity",scrap,"pieces"),
          ("Recurring Defects",recur,"repeated defect families"),("Closure Rate",f"{round(100*closed/max(total,1))}%","closed events")]
    for c,v in zip(st.columns(5),vals):
        with c:kpi(*v)
    p=pareto(view);a,b=st.columns([1.55,1])
    with a:
        st.markdown("### Top Defects · Pareto")
        if not p.empty:
            fig=go.Figure();fig.add_bar(x=p.iloc[:,0],y=p["Impact"],name="Impact");fig.add_scatter(x=p.iloc[:,0],y=p["Cumulative %"],name="Cumulative %",yaxis="y2")
            fig.update_layout(height=330,margin=dict(l=10,r=10,t=25,b=10),yaxis2=dict(overlaying="y",side="right",range=[0,105]),legend_orientation="h")
            st.plotly_chart(fig,use_container_width=True)
    with b:
        st.markdown("### NCR Status")
        if sc:
            x=view[sc].replace("","Unknown").value_counts().reset_index()
            fig=px.pie(x,names=sc,values="count",hole=.62);fig.update_layout(height=330,margin=dict(l=5,r=5,t=25,b=5))
            st.plotly_chart(fig,use_container_width=True)
    a,b=st.columns([1.6,1])
    with a:
        st.markdown("### Recent Quality Records")
        wanted=[x for x in ["Date","NCR_ID","Part","Process","Machine","Defect","Root_Cause","Status"] if x in view]
        st.dataframe(view[wanted].tail(10).iloc[::-1],use_container_width=True,hide_index=True)
    with b:
        st.markdown("### Root Cause Categories")
        rc=col(view,"Root_Cause","Root Cause")
        if rc:
            x=view[rc].fillna("").map(cause_category).value_counts().reset_index();x.columns=["Category","Count"]
            st.plotly_chart(px.bar(x,x="Category",y="Count"),use_container_width=True)
            st.markdown("**Top recurring root causes**")
            for i,(x,n) in enumerate(view[rc].value_counts().head(5).items(),1):st.write(f"{i}. {x} · **{n}**")

elif page=="New Investigation":
    hero("New Quality Investigation","Structure a shop-floor issue and compare it with historical NCR/CAPA evidence.")
    with st.form("new"):
        a,b,c=st.columns(3);part=a.text_input("Part / Product *");proc=b.text_input("Process *");machine=c.text_input("Machine")
        a,b,c=st.columns(3);defect=a.text_input("Defect / Failure Mode *");qty=b.number_input("Affected / Scrap Qty",0,100000,0);lot=c.text_input("Lot / Work Order")
        issue=st.text_area("Problem Statement *",height=130,placeholder="What happened? Where? Specification vs actual? Detection point?")
        go=st.form_submit_button("Run Root-Cause Investigation",type="primary")
    if go and issue:
        hits=st.session_state.rag.search(" ".join([part,proc,machine,defect,issue]),6);inv=investigate(issue,hits)
        a,b,c=st.columns(3);a.metric("Historical evidence",len(hits));b.metric("Evidence confidence",inv["confidence"]);c.metric("Affected quantity",qty)
        l,r=st.columns([1.15,1])
        with l:
            st.markdown("### Suspected Root Causes")
            for x in inv["roots"] or ["No supported historical cause found."]:st.markdown(f'<div class="step">{x}</div>',unsafe_allow_html=True)
            st.markdown("### 5-Why Draft")
            for i,x in enumerate(inv["whys"],1):st.markdown(f'<div class="step"><b>Why {i}</b> · {x}</div>',unsafe_allow_html=True)
        with r:
            for title,key in [("Immediate Containment","containment"),("Corrective Actions From History","corrective"),("Preventive Actions From History","preventive"),("Evidence Gaps / Verification","gaps")]:
                st.markdown(f"### {title}")
                for x in inv[key] or ["No historical evidence."]:st.write("•",x)
        st.markdown("### Traceable Historical Evidence")
        for h in hits:
            with st.expander(f'{h["record_id"]} · relevance {h["score"]:.3f} · {h["source"]}'):st.text(h["text"])
        out=pd.DataFrame({"Section":["Problem","Root Causes","Containment","Corrective","Preventive","Evidence Gaps"],
                          "Content":[issue," | ".join(inv["roots"])," | ".join(inv["containment"])," | ".join(inv["corrective"])," | ".join(inv["preventive"])," | ".join(inv["gaps"])]})
        st.download_button("Download Investigation",out.to_csv(index=False).encode(),"quality_investigation.csv","text/csv")

elif page=="Ask Quality RAG":
    hero("Ask Quality RAG","Search NCR, CAPA and scrap history without inventing unsupported factory facts.")
    q=st.text_area("Question",height=110,placeholder="What historical root causes caused bore oversize and what actions prevented recurrence?")
    if st.button("Search Evidence",type="primary") and q:
        hits=st.session_state.rag.search(q,7);inv=investigate(q,hits)
        st.markdown(f'### Evidence Confidence: <span class="badge">{inv["confidence"]}</span>',unsafe_allow_html=True)
        st.markdown("### Historical Root-Cause Findings")
        for x in inv["roots"] or ["No supported root cause found."]:st.write("•",x)
        st.markdown("### Evidence")
        for h in hits:
            with st.expander(f'{h["record_id"]} · {h["score"]:.3f}'):st.text(h["text"])

elif page=="Similar Cases":
    hero("Similar Historical Cases","Retrieve comparable defects, processes, machines and prior corrective actions.")
    q=st.text_area("Describe the new issue",height=120)
    if st.button("Find Similar Cases",type="primary") and q:
        for h in st.session_state.rag.search(q,8):
            m=h["metadata"];st.markdown(f'### {h["record_id"]} <span class="badge">relevance {h["score"]:.3f}</span>',unsafe_allow_html=True)
            st.write(m.get("Problem",""));st.write("**Root Cause:**",m.get("Root_Cause","Not recorded"));st.write("**Corrective Action:**",m.get("Corrective_Action","Not recorded"));st.divider()

elif page=="NCR Records":
    hero("NCR Records","Search, filter, review and export the quality event register.")
    q=st.text_input("Search all fields");out=view
    if q:out=out[out.astype(str).apply(lambda c:c.str.contains(q,case=False,na=False)).any(axis=1)]
    st.dataframe(out,use_container_width=True,hide_index=True,height=560)
    st.download_button("Export Filtered NCRs",out.to_csv(index=False).encode(),"ncr_records.csv","text/csv")

elif page=="CAPA Management":
    hero("CAPA Management","Track corrective/preventive actions, owners, due dates, status and effectiveness.")
    wanted=[x for x in ["NCR_ID","Part","Defect","Root_Cause","Corrective_Action","Preventive_Action","Owner","Due_Date","Status","Effectiveness"] if x in view]
    st.dataframe(view[wanted],use_container_width=True,hide_index=True,height=520)
    st.caption("In production, this view should be backed by your controlled QMS workflow and approval permissions.")

elif page=="Scrap Analysis":
    hero("Scrap Analysis","Prioritize manufacturing loss by defect family and recorded scrap impact.")
    p=pareto(view)
    if not p.empty:
        st.plotly_chart(px.bar(p,x=p.columns[0],y="Impact",title="Scrap Impact by Defect"),use_container_width=True);st.dataframe(p,use_container_width=True,hide_index=True)
    else:st.info("Structured data needs Defect and Scrap_Qty fields for this view.")

elif page=="Analytics & Reports":
    hero("Analytics & Reports","Operational views for daily quality management and continuous improvement.")
    a,b=st.columns(2);dc=col(view,"Defect");pc=col(view,"Process")
    with a:
        if dc:
            x=view[dc].value_counts().reset_index();st.plotly_chart(px.bar(x,x=dc,y="count",title="Events by Defect"),use_container_width=True)
    with b:
        if pc:
            x=view[pc].value_counts().reset_index();st.plotly_chart(px.bar(x,x=pc,y="count",title="Events by Process"),use_container_width=True)
    st.download_button("Download Analysis Dataset",view.to_csv(index=False).encode(),"quality_analysis.csv","text/csv")
