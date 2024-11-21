# -*- coding: utf-8 -*-
"""lineup.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sPPoFYnXg-DCHkull_kZkXQtASVnfOnX
"""

#Imports and packages

import pandas as pd     #For this project I will be using Pandas for scrapping and generating DataFrames
import ssl              #The SSL Library will be used for creating a context to disable SSL verification which is required for the Port of Santos website but optional for Port Paranagua
import urllib.request   #Used to open the HTML without SSL verification for use in Pandas
from google.colab import files

#URLs and SSL treatment

context = ssl._create_unverified_context() #Creates the unverified context for SSL

paranagua = 'https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo' #URL for the Port of Paranagua
santos = 'https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/' #URL for the Port of Santos

urlParanagua = urllib.request.urlopen(paranagua, context=context).read()  #Reads the HTML without SSL for the Port of Paranagua
urlSantos = urllib.request.urlopen(santos, context=context).read()        #Reads the HTML without SSL for the Port of Santos

#Creation of Data Frames

paranaguaDFs = pd.read_html(urlParanagua) #Create an array of Data Frames for the Paranagua Port
santosDFs = pd.read_html(urlSantos)       #Create an array of Data Frames for the Santos Port

#Mapping all the Data Frames in the Paranagua Port

atracadosDF = None
programadosDF = None
alReatracacaoDF = None
aoLargoDF = None
esperadosDF = None
apoioDF = None
despachadosDF = None

for i, df in enumerate(paranaguaDFs):
    print(f"Checking DataFrame {i}...")
    if not df.empty:
        # Check each column at level 0
        if 'ATRACADOS' in df.columns.get_level_values(0):
            atracadosDF = df
            atracadosDF.columns = atracadosDF.columns.droplevel(0)
            print("Found ATRACADOS!")
        elif 'PROGRAMADOS' in df.columns.get_level_values(0):
            programadosDF = df
            programadosDF.columns = programadosDF.columns.droplevel(0)
            print("Found PROGRAMADOS!")
        elif 'AO LARGO PARA REATRACAÇÃO' in df.columns.get_level_values(0):
            alReatracacaoDF = df
            alReatracacaoDF.columns = alReatracacaoDF.columns.droplevel(0)
            print("Found AO LARGO PARA REATRACAÇÃO!")
        elif 'AO LARGO' in df.columns.get_level_values(0):
            aoLargoDF = df
            aoLargoDF.columns = aoLargoDF.columns.droplevel(0)
            print("Found AO LARGO!")
        elif 'ESPERADOS' in df.columns.get_level_values(0):
            esperadosDF = df
            esperadosDF.columns = esperadosDF.columns.droplevel(0)
            df.rename(columns={'ETA': 'Chegada'}, inplace=True)
            print("Found ESPERADOS!")
        elif 'APOIO PORTUÁRIO / OUTROS' in df.columns.get_level_values(0):
            apoioDF = df
            apoioDF.columns = apoioDF.columns.droplevel(0)
            print("Found APOIO PORTUÁRIO / OUTROS!")
        elif 'DESPACHADOS' in df.columns.get_level_values(0):
            despachadosDF = df
            despachadosDF.columns = despachadosDF.columns.droplevel(0)
            print("Found DESPACHADOS!")

#Filtering all the data and making the dictionaries for the Port of Paranagua

atracados = atracadosDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
atracados['Porto'] = 'Paranaguá'
atracados['Status'] = 'Atracado'
dictAtracados = atracados.to_dict(orient = 'records')


programados = programadosDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
programados['Porto'] = 'Paranaguá'
programados['Status'] = 'Programado'
dictProgramados = programados.to_dict(orient = 'records')

alReatracacao = alReatracacaoDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
alReatracacao['Porto'] = 'Paranaguá'
alReatracacao['Status'] = 'Ao Largo para Reatracação'
dictAlReatracacao = alReatracacao.to_dict(orient = 'records')

aoLargo = aoLargoDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
aoLargo['Porto'] = 'Paranaguá'
aoLargo['Status'] = 'Ao Largo'
dictAoLargo = aoLargo.to_dict(orient = 'records')


esperados = esperadosDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
esperados['Porto'] = 'Paranaguá'
esperados['Status'] = 'Esperado'
dictEsperados = esperados.to_dict(orient = 'records')

apoio = apoioDF[['Chegada']].copy()
apoio['Mercadoria'] = 'Apoio Portuario'
apoio['Sentido'] = 'Apoio Portuario'
apoio['Previsto'] = 'Apoio Portuario'
apoio['Porto'] = 'Paranaguá'
apoio['Status'] = 'Apoio Portuario'
dictApoio = apoio.to_dict(orient = 'records')

despachados = despachadosDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
despachados['Porto'] = 'Paranaguá'
despachados['Status'] = 'Despachado'
dictDespachados = despachados.to_dict(orient = 'records')

#mapping the Data Frames in the Santos Port

liquidoAGranelDF = None
trigoDF = None
granelDeOrigemVegetalDF = None
graneisSolidosImportacaoDF = None
graneisSolidosExportacaoDF = None
rollInRollOffDF = None
lashDF = None
cabotagemDF = None
conteineresDF = None
prioridadeC3DF = None
prioridadeC5DF = None
semPrioridadeDF = None


for i, df in enumerate(santosDFs):
  if not df.empty:
    if 'LIQUIDO A GRANEL' in df.columns.get_level_values(0):
      liquidoAGranelDF = df
      liquidoAGranelDF.columns = liquidoAGranelDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
      })
      print("Found LiquidoAGranel!")
    elif 'TRIGO' in df.columns.get_level_values(0):
      trigoDF = df
      trigoDF.columns = trigoDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
      })
      print("Found Trigo!")
    elif 'GRANEIS DE ORIGEM VEGETAL' in df.columns.get_level_values(0):
      granelDeOrigemVegetalDF = df
      granelDeOrigemVegetalDF.columns = granelDeOrigemVegetalDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found GranelDeOrigemVegetal!")
    elif 'GRANEIS SOLIDOS - IMPORTACAO' in df.columns.get_level_values(0):
      graneisSolidosImportacaoDF = df
      graneisSolidosImportacaoDF.columns = graneisSolidosImportacaoDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found GraneisSolidosImportacao!")
    elif 'GRANEIS SOLIDOS - EXPORTACAO' in df.columns.get_level_values(0):
      graneisSolidosExportacaoDF = df
      graneisSolidosExportacaoDF.columns = graneisSolidosExportacaoDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found GraneisSolidosExportacao!")
    elif 'ROLL-IN-ROLL-OFF' in df.columns.get_level_values(0):
      rollInRollOffDF = df
      rollInRollOffDF.columns = rollInRollOffDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found RollInRollOff!")
    elif 'LASH' in df.columns.get_level_values(0):
      lashDF = df
      lashDF.columns = lashDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found Lash!")
    elif 'CABOTAGEM' in df.columns.get_level_values(0):
      cabotagemDF = df
      cabotagemDF.columns = cabotagemDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found Cabotagem!")
    elif 'CONTEINERES' in df.columns.get_level_values(0):
      conteineresDF = df
      conteineresDF.columns = conteineresDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found Conteineres!")
    elif 'PRIORIDADE C3' in df.columns.get_level_values(0):
      prioridadeC3DF = df
      prioridadeC3DF.columns = prioridadeC3DF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found PrioridadeC3!")
    elif 'PRIORIDADE C5' in df.columns.get_level_values(0):
      prioridadeC5DF = df
      prioridadeC5DF.columns = prioridadeC5DF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found PrioridadeC5!")
    elif 'SEM PRIORIDADE' in df.columns.get_level_values(0):
      semPrioridadeDF = df
      semPrioridadeDF.columns = semPrioridadeDF.columns.droplevel(0)
      df.rename(columns={'Mercadoria Goods': 'Mercadoria', 'Operaç Operat': 'Sentido', 'Cheg/Arrival d/m/y': 'Chegada', 'Peso Weight': 'Previsto'}, inplace=True)
      df['Sentido'] = df['Sentido'].replace({
        'EMB': 'Exp',         # Standardize 'emb' to 'exp'
        'DESC': 'Imp',        # Standardize 'desc' to 'imp'
        'EMB DESC': 'Imp/Exp' # Standardize 'emb desc' to 'exp/imp'
        })
      print("Found SemPrioridade!")

#Filtering all the data for the port of Santos

liquidoAGranel = liquidoAGranelDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
liquidoAGranel['Porto'] = 'Santos'
liquidoAGranel['Status'] = 'Liquido A Granel'
dictLiquidoAGranel = liquidoAGranel.to_dict(orient = 'records')
print(dictLiquidoAGranel)

trigo = trigoDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
trigo['Porto'] = 'Santos'
trigo['Status'] = 'Trigo'
dictTrigo = trigo.to_dict(orient = 'records')

granelDeOrigemVegetal = granelDeOrigemVegetalDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
granelDeOrigemVegetal['Porto'] = 'Santos'
granelDeOrigemVegetal['Status'] = 'Granel De Origem Vegetal'
dictGranelDeOrigemVegetal = granelDeOrigemVegetal.to_dict(orient = 'records')

graneisSolidosImportacao = graneisSolidosImportacaoDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
graneisSolidosImportacao['Porto'] = 'Santos'
graneisSolidosImportacao['Status'] = 'Graneis Solidos Importacao'
dictGraneisSolidosImportacao = graneisSolidosImportacao.to_dict(orient = 'records')

graneisSolidosExportacao = graneisSolidosExportacaoDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
graneisSolidosExportacao['Porto'] = 'Santos'
graneisSolidosExportacao['Status'] = 'Graneis Solidos Exportacao'
dictGraneisSolidosExportacao = graneisSolidosExportacao.to_dict(orient = 'records')

rollInRollOff = rollInRollOffDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
rollInRollOff['Porto'] = 'Santos'
rollInRollOff['Status'] = 'Roll In Roll Off'
dictRollInRollOff = rollInRollOff.to_dict(orient = 'records')

lash = lashDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
lash['Porto'] = 'Santos'
lash['Status'] = 'Lash'
dictLash = lash.to_dict(orient = 'records')

cabotagem = cabotagemDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
cabotagem['Porto'] = 'Santos'
cabotagem['Status'] = 'Cabotagem'
dictCabotagem = cabotagem.to_dict(orient = 'records')

conteineres = conteineresDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
conteineres['Porto'] = 'Santos'
conteineres['Status'] = 'Conteiners'
dictConteineres = conteineres.to_dict(orient = 'records')

prioridadeC3 = prioridadeC3DF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
prioridadeC3['Porto'] = 'Santos'
prioridadeC3['Status'] = 'Prioridade C3'
dictPrioridadeC3 = prioridadeC3.to_dict(orient = 'records')

prioridadeC5 = prioridadeC5DF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
prioridadeC5['Porto'] = 'Santos'
prioridadeC5['Status'] = 'Prioridade C5'
dictPrioridadeC5 = prioridadeC5.to_dict(orient = 'records')

semPrioridade = semPrioridadeDF[['Mercadoria', 'Sentido', 'Chegada', 'Previsto']].copy()
semPrioridade['Porto'] = 'Santos'
semPrioridade['Status'] = 'Sem Prioridade'
dictSemPrioridade = semPrioridade.to_dict(orient = 'records')

#merge_dict = {**dictAtracados, **dictProgramados, **dictAlReatracacao, **dictAoLargo, **dictEsperados, **dictApoio, **dictDespachados, **dictLiquidoAGranel, **dictTrigo, **dictGranelDeOrigemVegetal, **dictGraneisSolidosExportacao,**dictGraneisSolidosImportacao, **dictRollInRollOff, **dictLash, **dictCabotagem, **dictConteineres, **dictPrioridadeC3, **dictPrioridadeC5, **dictSemPrioridade}
# Assuming your dict variables (dictAtracados, dictProgramados, etc.) are lists of dictionaries
# Example: dictAtracados = [{'key1': 'value1'}, {'key2': 'value2'}]
merged_dict = {}
all_dicts = [dictAtracados, dictProgramados, dictAlReatracacao, dictAoLargo,
             dictEsperados, dictApoio, dictDespachados, dictLiquidoAGranel,
             dictTrigo, dictGranelDeOrigemVegetal, dictGraneisSolidosExportacao,
             dictGraneisSolidosImportacao, dictRollInRollOff, dictLash,
             dictCabotagem, dictConteineres, dictPrioridadeC3,
             dictPrioridadeC5, dictSemPrioridade]

# Flatten each list of dictionaries in all_dicts
flattened_dicts = [item for sublist in all_dicts for item in sublist]

# Convert flattened list of dictionaries to a single DataFrame for convenience
# Here we assume the dictionaries have similar keys, so they can form a coherent table

merged_df = pd.DataFrame(flattened_dicts)
dictAll = merged_df.to_dict(orient = 'records')

# Optionally save to a CSV file
merged_df.to_csv('/content/merged_data.csv', index=False)
files.download('/content/merged_data.csv')

files.download('/content/merged_dict.csv')