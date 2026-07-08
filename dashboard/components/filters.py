import streamlit as st

from services.duckdb_service import query


def render_global_filters():
    hospitals = query("SELECT hospital FROM dim_hospital ORDER BY hospital")["hospital"].tolist()
    convenios = query("SELECT convenio FROM dim_convenio ORDER BY convenio")["convenio"].tolist()
    especialidades = query("SELECT DISTINCT especialidade_medica FROM dim_medico ORDER BY especialidade_medica")["especialidade_medica"].tolist()

    st.markdown("###Filtros Globais")

    c1, c2, c3 = st.columns(3)

    selected_hospital = c1.selectbox("Hospital", ["Todos"] + hospitals)
    selected_convenio = c2.selectbox("Convênio", ["Todos"] + convenios)
    selected_especialidade = c3.selectbox("Especialidade", ["Todas"] + especialidades)

    filters = {
        "hospital": selected_hospital,
        "convenio": selected_convenio,
        "especialidade": selected_especialidade,
    }

    return filters


def build_filter_where(filters):
    conditions = []

    if filters.get("hospital") and filters["hospital"] != "Todos":
        conditions.append(f"dh.hospital = '{filters['hospital']}'")

    if filters.get("convenio") and filters["convenio"] != "Todos":
        conditions.append(f"dc.convenio = '{filters['convenio']}'")

    if filters.get("especialidade") and filters["especialidade"] != "Todas":
        conditions.append(f"dm.especialidade_medica = '{filters['especialidade']}'")

    if conditions:
        return " WHERE " + " AND ".join(conditions)

    return ""