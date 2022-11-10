import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

pd.options.display.max_columns = None


def year_range(year:pd.Series):
  if year>=2004 and year <= 2007:
    return '2004-2007'
  if year>=2008 and year <= 2011:
    return '2008-2011'
  if year>=2012 and year <= 2015:
    return '2012-2015'
  if year>=2016 and year <= 2019:
    return '2016-2019'
  if year>=2020 and year <= 2023:
    return '2020-2023'
  return 'sin_datos'

def get_causa(txt):
    txt = str(txt)
    matches = ['asesinato', 'sicariato', 'homicidio']
    if any(x in txt.lower() for x in matches):
        return 'homicidio_asesinato'

    matches = ['drogas','narcotráfico', 'Narcotráfico y homicidio']
    if any(x in txt.lower() for x in matches):
        return 'drogas_ilegales'

    matches = ["robo", "asalto", "asaltos", "atraco", "atracar", "asalto"]
    if any(x in txt.lower() for x in matches):
        return 'robo_asalto'

    matches = ['delincuencia', 'secuestro', 'prófugo', 'fuga', 'prófugo', 'riña', 'agresión', 'delitos', 'abuso'
    'cuatrero', 'fuga', 'delito', 'delitos', 'complicidad', 'violar', 'violencia', 'violacion', 'violación', 'conflicto', 'tiroteo','violador', 'terrorismo']
    if any(x in txt.lower() for x in matches):
        return 'delincuencia'

    matches = ['no detenerse', 'discusión', 'intento', 'sospechosos', 'sospechosa', 'sospechoso', 'ruido', 'antecedentes', 
    'ilegal', 'ilegales', 'sustracción', 'protestar', 'invasión', 'deuda']
    if any(x in txt.lower() for x in matches):
        return 'sospecha'

    matches = ['ninguno', 'no especificado', 'no se especifica', 'no precisado']
    if any(x in txt.lower() for x in matches):
        return 'no_especificado'

    return 'otro'

def create_id_txt(txt):
  txt = str(txt)
  txt = txt.lower()
  txt = txt.replace(' ', '')
  txt = txt.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
  return txt


def get_df_by_period(df, qty='cantidad', dimension='region'):
  df_provicia_year = df.groupby([dimension, 'year_range']).size().reset_index(name=qty)
  df1 = df_provicia_year[   df_provicia_year['year_range'] == '2004-2007']
  df2 = df_provicia_year[   df_provicia_year['year_range'] == '2008-2011']
  df3 = df_provicia_year[   df_provicia_year['year_range'] == '2012-2015']
  df4 = df_provicia_year[   df_provicia_year['year_range'] == '2016-2019']
  df5 = df_provicia_year[   df_provicia_year['year_range'] == '2020-2023']
  return df1, df2, df3, df4, df5

def region_preproc(df0):
  df_region = df0[['Provincia', 'Región']].copy()
  df_region.columns = ['id_provincia', 'region']
  df_region['id_provincia'] = df_region.id_provincia.apply(create_id_txt)
  df_region.loc[df_region.id_provincia == 'santodomingo', 'region'] = 'Santo Domingo'
  df_region.loc[df_region.id_provincia == 'distritonacional', 'region'] = 'Distrito Nacional'
  df_region = pd.concat([df_region, pd.DataFrame({'id_provincia':['sin_dato'], 'region':['sin_dato']})], axis=0)
  return df_region

def load_from_gdrive(url, ftype='csv'):
  path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
  if ftype == 'csv':
    df = pd.read_csv(path)
  if ftype == 'excel':
    df = pd.read_excel(path)
  print(f'rows:{df.shape[0]} columns:{df.shape[1]}')
  return df

def poblacion_preproc(df):
  df_poblacion1 = df.fillna(0).copy()
  df_poblacion1.columns = ['provincia', 'capital', 'superficie_km2', 'poblacion', 'densidad']
  df_poblacion1.poblacion = df_poblacion1.poblacion.astype(int)
  df_poblacion1['id_provincia'] = df_poblacion1.provincia.apply(create_id_txt)
  df_poblacion2 = df_poblacion1.groupby(['id_provincia'])['poblacion'].sum()
  df_poblacion2 = df_poblacion2[df_poblacion2>0]
  df_poblacion2 = pd.DataFrame(df_poblacion2).reset_index()
  df_poblacion2.columns = ['id_provincia', 'poblacion_provincia']
  print(f'df_poblacion -> rows:{df_poblacion2.shape[0]} columns:{df_poblacion2.shape[1]}')
  return df_poblacion2
  

def plot_hbar(df, qty='cantidad', dimension='region', width=999,height=333):
  df1, df2, df3, df4, df5 = get_df_by_period(df, qty=qty, dimension=dimension)

  fig = make_subplots(rows=1, cols=5, specs=[[{}, {}, {}, {}, {}]], 
                      shared_xaxes='rows',
                      shared_yaxes=True, 
                      #horizontal_spacing=0, 
                      
                      subplot_titles=('2004-2007', '2008-2011', '2012-2015', '2016-2019', '2020-2023')
                      )

  fig.append_trace(go.Bar(
                      x=df1[qty],
                      y=df1[dimension], 
                      text=df1["cantidad"].map('{:,.0f}'.format), #Display the numbers with thousands separators in hover-over tooltip 
                      textposition='inside',
                      orientation='h', 
                      width=0.7, 
                      showlegend=False, 
                      marker_color='#4472c4'), 
                      1, 1) # 1,1 represents row 1 column 1 in the plot grid

  fig.append_trace(go.Bar(
                      x=df2[qty],
                      y=df2[dimension], 
                      text=df2["cantidad"].map('{:,.0f}'.format), #Display the numbers with thousands separators in hover-over tooltip 
                      textposition='inside',
                      orientation='h', 
                      width=0.7, 
                      showlegend=False, 
                      marker_color='#ed7d31'), 
                      1, 2) # 1,2 represents row 1 column 2 in the plot grid

  fig.append_trace(go.Bar(
                      name="2004-2007",
                      x=df3[qty],
                      y=df3[dimension], 
                      text=df3["cantidad"].map('{:,.0f}'.format), #Display the numbers with thousands separators in hover-over tooltip 
                      textposition='inside',
                      orientation='h', 
                      width=0.7, 
                      showlegend=False, 
                      marker_color='#ed7d31'), 
                      1, 3) # 1,2 represents row 1 column 2 in the plot grid

  fig.append_trace(go.Bar(
                      x=df4[qty],
                      y=df4[dimension], 
                      text=df4["cantidad"].map('{:,.0f}'.format), #Display the numbers with thousands separators in hover-over tooltip 
                      textposition='inside',
                      orientation='h', 
                      width=0.7, 
                      showlegend=False, 
                      marker_color='#ed7d31'), 
                      1, 4) # 1,2 represents row 1 column 2 in the plot grid

  fig.append_trace(go.Bar(
                      x=df5[qty],
                      y=df5[dimension], 
                      text=df5["cantidad"].map('{:,.0f}'.format), #Display the numbers with thousands separators in hover-over tooltip 
                      textposition='inside',
                      orientation='h', 
                      width=0.7, 
                      showlegend=False, 
                      marker_color='#ed7d31'), 
                      1, 5) # 1,2 represents row 1 column 2 in the plot grid

  fig.update_layout(autosize=False,width=width,height=height,)
  fig.show()


def plot_tendencia(df, periodo='muerto_el_year'):
  df_year = pd.DataFrame(df[periodo].value_counts().reset_index())
  df_year.columns = ['year', 'qty']
  df_year = df_year.sort_values('year')

  fig = px.bar(df_year, x='year', y='qty', width=999, height=400,
              text_auto=True, 
              #text_auto='.2s'
                )
  if periodo == 'muerto_el_year':
    text_tittle = "Tendencia de muertes por año"
  if periodo == 'year_range':
    text_tittle = "Tendencia de muertes por periodo"

  fig.update_layout(
      title={'text': text_tittle, 'y':0.92,'x':0.5,'xanchor': 'center', 'yanchor': 'top'},
      font_family="Courier New",
      font_color="black",
      title_font_family="Times New Roman",
      title_font_color="black",
      #legend_title_font_color="green",
      #xaxis_title="X Axis Title",
      yaxis_title="Cantidad Total",
      xaxis=dict( title='Años', tickmode='linear'),
      #legend_title="Legend Title",
      font=dict(
          family="Courier New, monospace",
          size=12,
          color="RebeccaPurple"
      )


  )
  #fig.update_xaxes(
      #tickangle = 0,
      #title_text = "Month",
                  #title_font = {"size": 18},
          #title_standoff = 22 # cercania entre x_label y el eje_x)

  fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
  fig.update_xaxes(title_font_family="Arial")

  fig.show()

def plot_hbar_s(df, dim, qty, width=555, height=888, title='Muertes por Provincias'):
  fig = px.bar(df, x=df[qty], y=df[dim], 
               text=df[qty], #.map('{:,.00000f}'.format), #Display the numbers with thousands separators in hover-over tooltip 
               #textposition='inside',
               #color='day', 
               orientation='h',
              #hover_data=["tip", "size"],
              width=width, height=height,
              title=title)
  fig.show()

  