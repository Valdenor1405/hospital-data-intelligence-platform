import streamlit as st


def render_header():
    st.markdown(
        """
        <div style="
            padding: 18px 24px;
            border-radius: 14px;
            background: linear-gradient(90deg, #0f172a, #1e293b);
            border: 1px solid #334155;
            margin-bottom: 24px;
        ">
            <h1 style="margin: 0; color: #f8fafc;">
                Hospital Data Intelligence Platform
            </h1>
            <p style="margin: 6px 0 0 0; color: #cbd5e1;">
                Enterprise Data Engineering • Analytics • AI • MLOps
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )