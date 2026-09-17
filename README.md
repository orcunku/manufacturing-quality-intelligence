# Quality Intelligence v2
👉 [Open the Live Streamlit Application](https://manufacturing-quality-intelligence-jl5hnhssgzhttwgzkanvxg.streamlit.app/)

Modern Streamlit NCR / CAPA / Scrap Root-Cause Analysis for manufacturing demos.

## Deploy on Streamlit Community Cloud
1. Upload all project files to the root of your GitHub repository.
2. Confirm `streamlit_app.py` and `requirements.txt` are at repository root.
3. In Streamlit Community Cloud create/redeploy the app.
4. Main file: `streamlit_app.py`.
5. No secrets or paid API are required.
6. Open **Data Management** and click **Load sample factory dataset**.

## Factory-oriented modules
Dashboard, New Investigation, Quality RAG, Similar Cases, NCR Records, CAPA Management, Scrap Analysis, Analytics & Reports, Data Management.

## Important production note
This is a decision-support prototype. Root causes, containment, corrective/preventive actions, dispositions and CAPA closure must be verified and approved by authorized quality personnel. Production deployment should add persistent database storage, SSO/RBAC, audit trail, electronic approvals, QMS/MES/ERP integrations, site permissions, backups, cybersecurity controls, controlled taxonomies, validation and retrieval-quality testing.

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
