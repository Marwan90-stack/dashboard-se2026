def main():
    import polars as pl 
    import streamlit as st 
    import plotly_express as px 
    
    dashboard_page = st.Page("dashboard.py", title="Dashboard", icon=":material/dashboard:")
    table_page = st.Page("table.py", title="Tabel", icon=":material/table:")

    pg = st.navigation([dashboard_page, table_page])
    st.set_page_config(page_title="Dashboard Sensus Ekonomi 2026", page_icon=":material/home:")
    pg.run()
    
    # st.set_page_config(
    #     page_title="Dashboard Sensus Ekonomi 2026",
    #     layout="wide"
    # )
    
    # st.header("Dashboard SE2026 BPS Kabupaten Kepulauan Tanimbar")
    # st.title("Dashboard SE2026 BPS Kabupaten Kepulauan Tanimbar")
    
    with st.bottom:
        st.text("Built by Marwan with ☕️", text_alignment="right")
    


if __name__ == "__main__":
    main()
