import streamlit as st 
import polars as pl 
import plotly_express as px

st.set_page_config(
        # page_title="Dashboard Sensus Ekonomi 2026",
        layout="wide"
    )

@st.cache_data
def fetch_and_clean_data():
    # Fetch data from URL here, and then clean it up.
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQkidoA906lx1B1wWo5gvyjjmpmwCJN9XRFBAcgJcXjFcf6nsY25rQc6fRd9fkwq__HZW93MaCFi3h/pub?output=xlsx"
    
    # df = pl.read_excel("data/alokasi-petugas-cleaned.xlsx")
    df = pl.read_excel(url)
    
    selected_columns = ['nmdesa', 'nmsls', 'jenis', 'nmkec', 'kk', 'usaha', 'muatan', 'pcl', 'pml']
    
    df = df.select(pl.col(selected_columns))
    df = (
        df.with_columns(
        nmdesa = pl.col("nmdesa").str.to_titlecase(),
        nmkec = pl.col('nmkec').str.to_titlecase(),
        pcl = pl.col('pcl').str.to_titlecase(),
        pml = pl.col('pml').str.to_titlecase()
      )
      .select(
        pl.col(['nmkec', 'nmdesa', 'nmsls', 'jenis', 'pml', 'pcl', 'kk', 'usaha', 'muatan'])
      )
    )
    
    # df = (
    #   df.with_columns(
    #     (pl.col("muatan")*0.4).ceil().alias("muatan_40"),
    #     (pl.col("usaha")*0.4).ceil().alias("usaha_40"),
        
    #   )
    #   .with_columns(
    #     (pl.col("usaha") - pl.col("usaha_40")).ceil().alias("usaha_60"),
    #     (pl.col("muatan") - pl.col("muatan_40")).ceil().alias("muatan_60")
    #   )
    #   .with_columns(
    #     (pl.col("muatan_60")/30).ceil().alias("target_harian_ruta_termin1"),
    #     (pl.col("usaha_40")/30).ceil().alias("target_harian_usaha_termin1"),
    #     (pl.col("muatan_60")/45).ceil().alias("target_harian_ruta_termin2"),
    #     (pl.col("usaha_60")/45).ceil().alias("target_harian_usaha_termin2")
    #   )
    
    # )
    
    # df = (
    #     df.select(
    #       pl.col('pml', 'pcl', 'target_harian_ruta_termin1', 'target_harian_usaha_termin1', 'target_harian_ruta_termin2', 'target_harian_usaha_termin2')
    #     )
    #   )   
    
    return df
  

df_alokasi = fetch_and_clean_data()

# target_ppl = (
#   df_alokasi
#   .select(pl.col('pcl', 'target_harian_ruta_termin1', 'target_harian_ruta_termin2', 'target_harian_usaha_termin1', 'target_harian_usaha_termin2'))
#   .group_by(pl.col("pcl"))
#   .sum()
# )
target_ppl = (
  df_alokasi
  .select(pl.col('pcl', 'usaha', 'muatan'))
  .group_by(pl.col("pcl"))
  .sum()
  .with_columns(
    (pl.col("muatan")*0.4).alias("muatan_40"),
    (pl.col("usaha")*0.4).alias("usaha_40"),
  )
  .with_columns(
    (pl.col("usaha") - pl.col("usaha_40")).alias("usaha_60"),
    (pl.col("muatan") - pl.col("muatan_40")).alias("muatan_60")
  )
  .with_columns(
    (pl.col("muatan_40")/30).ceil().alias("target_harian_ruta_termin1"),
    (pl.col("usaha_40")/30).ceil().alias("target_harian_usaha_termin1"),
    (pl.col("muatan_60")/45).ceil().alias("target_harian_ruta_termin2"),
    (pl.col("usaha_60")/45).ceil().alias("target_harian_usaha_termin2")
  )
  .select(
    pl.col(
      'pcl', 
      'target_harian_ruta_termin1', 
      'target_harian_ruta_termin2', 
      'target_harian_usaha_termin1', 
      'target_harian_usaha_termin2'
      )
    )
  )


# target_ppl.columns = ['PPL', 'Target Harian RUTA Termin 1', 'Target Harian Ruta Termin 2', 'Target Harian']
st.header("Target Pencacahan Harian Sensus Ekonomi 2026", divider=True)
ppl = st.text_input(label="Cari Nama PPL", icon=":material/search:")

if ppl == None:
  target_ppl = (
    target_ppl
    .rename(
    {
      'pcl' : 'PPL',
      'target_harian_ruta_termin1': 'Target Harian Ruta Termin 1',
      'target_harian_ruta_termin2': 'Target Harian Ruta Termin 2',
      'target_harian_usaha_termin1': 'Target Harian Usaha Termin 1',
      'target_harian_usaha_termin2': 'Target Harian Usaha Termin 2'
      }
    )
  )
  st.dataframe(target_ppl)
else:
  target_ppl = (
    target_ppl.filter(
      pl.col("pcl").str.contains(ppl)
    )
    .rename(
    {
      'pcl' : 'PPL',
      'target_harian_ruta_termin1': 'Target Harian Ruta Termin 1',
      'target_harian_ruta_termin2': 'Target Harian Ruta Termin 2',
      'target_harian_usaha_termin1': 'Target Harian Usaha Termin 1',
      'target_harian_usaha_termin2': 'Target Harian Usaha Termin 2'
      }
    )
  )
  
  st.dataframe(target_ppl)

target_pml = (
  df_alokasi
  .select(pl.col('pml', 'usaha', 'muatan'))
  .group_by(pl.col("pml"))
  .sum()
  .with_columns(
    (pl.col("muatan")*0.4).alias("muatan_40"),
    (pl.col("usaha")*0.4).alias("usaha_40"),
  )
  .with_columns(
    (pl.col("usaha") - pl.col("usaha_40")).alias("usaha_60"),
    (pl.col("muatan") - pl.col("muatan_40")).alias("muatan_60")
  )
  .with_columns(
    (pl.col("muatan_40")/30).ceil().alias("target_harian_ruta_termin1"),
    (pl.col("usaha_40")/30).ceil().alias("target_harian_usaha_termin1"),
    (pl.col("muatan_60")/45).ceil().alias("target_harian_ruta_termin2"),
    (pl.col("usaha_60")/45).ceil().alias("target_harian_usaha_termin2")
  )
  .select(
    pl.col(
      'pml', 
      'target_harian_ruta_termin1', 
      'target_harian_ruta_termin2', 
      'target_harian_usaha_termin1', 
      'target_harian_usaha_termin2'
      )
    )
  )
  
pml = st.text_input(label="Cari Nama PML", icon=":material/search:")
  
if pml == None:
  target_pml = (
    target_pml
    .rename(
    {
      'pml' : 'PML',
      'target_harian_ruta_termin1': 'Target Harian Ruta Termin 1',
      'target_harian_ruta_termin2': 'Target Harian Ruta Termin 2',
      'target_harian_usaha_termin1': 'Target Harian Usaha Termin 1',
      'target_harian_usaha_termin2': 'Target Harian Usaha Termin 2'
      }
    )
  )
  st.dataframe(target_pml)
else:
  target_pml = (
    target_pml.filter(
      pl.col("pml").str.contains(pml)
    )
    .rename(
    {
      'pml' : 'PML',
      'target_harian_ruta_termin1': 'Target Harian Ruta Termin 1',
      'target_harian_ruta_termin2': 'Target Harian Ruta Termin 2',
      'target_harian_usaha_termin1': 'Target Harian Usaha Termin 1',
      'target_harian_usaha_termin2': 'Target Harian Usaha Termin 2'
      }
    )
  )
  
  st.dataframe(target_pml)