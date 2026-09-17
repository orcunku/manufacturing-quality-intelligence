import streamlit as st
CSS="""<style>
#MainMenu,footer{visibility:hidden}.block-container{padding-top:1.2rem;max-width:1500px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0b2035,#102e4a)}
[data-testid="stSidebar"] *{color:#eef6ff}
[data-testid="stSidebar"] input{color:#15243b}
.hero{background:linear-gradient(110deg,#102b46,#1767a5);padding:27px 30px;border-radius:18px;color:white;margin-bottom:18px;box-shadow:0 10px 28px rgba(10,39,67,.14)}
.hero h1{color:white;margin:0;font-size:2rem}.hero p{color:#dcecff;margin:.4rem 0 0}
.kpi{background:white;border:1px solid #e1e8f0;border-radius:14px;padding:17px 18px;min-height:118px;box-shadow:0 4px 16px rgba(17,44,73,.05)}
.kl{font-size:.75rem;color:#6c7d91;font-weight:800;text-transform:uppercase}.kv{font-size:1.75rem;color:#102b46;font-weight:800;margin-top:5px}.ks{font-size:.76rem;color:#7b8ba0}
.card{background:white;border:1px solid #e1e8f0;border-radius:14px;padding:18px;box-shadow:0 4px 16px rgba(17,44,73,.05)}
.step{border-left:3px solid #1677ff;background:#f7faff;padding:10px 13px;margin:7px 0;border-radius:0 9px 9px 0}
.badge{background:#e8f3ff;color:#1767a5;border-radius:999px;padding:4px 9px;font-size:.75rem;font-weight:800}
.stButton>button{border-radius:9px;font-weight:700}
</style>"""
def setup():
    st.set_page_config(page_title="Quality Intelligence",page_icon="⚙️",layout="wide")
    st.markdown(CSS,unsafe_allow_html=True)
def hero(a,b): st.markdown(f'<div class="hero"><h1>{a}</h1><p>{b}</p></div>',unsafe_allow_html=True)
def kpi(a,b,c=""): st.markdown(f'<div class="kpi"><div class="kl">{a}</div><div class="kv">{b}</div><div class="ks">{c}</div></div>',unsafe_allow_html=True)
