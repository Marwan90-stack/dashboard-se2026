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

@st.cache_data
def fetch_lokasi_tugas():
  url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQkidoA906lx1B1wWo5gvyjjmpmwCJN9XRFBAcgJcXjFcf6nsY25rQc6fRd9fkwq__HZW93MaCFi3h/pub?output=xlsx"
  
  df = pl.read_excel(url)
  df = (
    df
    .select(
      pl.col(["pml", "pcl", "nmkec", "nmdesa", "nmsls", "jenis"])
    )
  )
  
  df = (
    df
    .with_columns(
      pml = pl.col("pml").str.to_titlecase(),
      pcl = pl.col("pcl").str.to_titlecase(),
      nmkec = pl.col("nmkec").str.to_titlecase(),
      nmdesa = pl.col("nmdesa").str.to_titlecase()
      # pl.col("nama_ketua").str.to_titlecase().alias("nama_ketua")
    )
    .rename(
      {
        "pml": "PML",
        "pcl": "PPL",
        "nmkec": "Kecamatan",
        "nmdesa": "Desa",
        "nmsls": "SLS",
        # "nama_ketua": "Ketua SLS",
        "jenis": "Jenis"
      }
    )
  )
    
  return df
  

df_alokasi = fetch_and_clean_data()
df_lokasi = fetch_lokasi_tugas()

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
ppl = st.text_input(label="Cari Nama PPL", icon=":material/search:", placeholder="Ketikan nama PPL")

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
  
pml = st.text_input(label="Cari Nama PML", icon=":material/search:", placeholder="Ketikan nama PML")
  
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


st.text("Alokasi Wilayah Tugas")
# column_options = st.columns(3)

pml_list = (
  df_lokasi
  .select(pl.col("PML"))
  .unique()
  .to_series()
)

# pml_list = [i for i in pml_list]

ppl_list = (
  df_lokasi
  .select(pl.col("PPL"))
  .unique()
  .to_series()
)
# ppl_list = [i for i in ppl_list]
# first_option = ["Semua"]

# pilih_pml = column_options[0].selectbox("Pilih PML", pml_list)
# pilih_ppl = column_options[1].selectbox("Pilih PPL", ppl_list)

radio = st.radio("Cari Berdasarkan:", options=["PML", "PPL"])
pml_ppl = st.text_input("Cari Nama", placeholder="Masukan nama PML atau PPL", icon=":material/search:")

if pml_ppl == None:
  st.dataframe(df_lokasi)
else:
  if radio == "PML":
  # if pml_ppl
    df_lokasi = (
      df_lokasi
      .filter(
        pl.col("PML").str.contains(pml_ppl) #or pl.col("PPL").str.contains(pml_ppl)
      )
    )
    
    st.dataframe(df_lokasi)
  else:
    df_lokasi = (
      df_lokasi
      .filter(
        pl.col("PPL").str.contains(pml_ppl)
      )
    )
    
    st.dataframe(df_lokasi)