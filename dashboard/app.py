import streamlit as st

from components.header import render_header
from pages.executive import render_executive_page
from pages.finance import render_finance_page
from components.filters import render_global_filters
from pages.clinical import render_clinical_page
from pages.pharmacy import render_pharmacy_page
from pages.surgery import render_surgery_page
from pages.readmission import render_readmission_page
from pages.quality import render_quality_page

st.set_page_config(
    page_title="Hospital Data Intelligence Platform",
    page_icon="",
    layout="wide",
)

render_header()
filters = render_global_filters()

page = st.sidebar.radio(
    "Navegação",
    [
        "Executive Overview",
        "Financeiro",
        "Assistencial",
        "Farmácia",
        "Centro Cirúrgico",
        "Readmissão",
        "Data Quality",
    ],
)

if page == "Executive Overview":
    render_executive_page(filters)
elif page == "Financeiro":
    render_finance_page(filters)
elif page == "Assistencial":
    render_clinical_page(filters)
elif page == "Farmácia":
    render_pharmacy_page(filters)
elif page == "Centro Cirúrgico":
    render_surgery_page(filters)
elif page == "Readmissão":
    render_readmission_page(filters)
elif page == "Data Quality":
    render_quality_page(filters)
else:
    st.info(f"Módulo '{page}' será migrado para arquitetura modular nas próximas etapas.")