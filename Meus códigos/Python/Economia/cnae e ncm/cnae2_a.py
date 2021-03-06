# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 09:44:12 2020

@author: pedro-salj
"""

#############################
##### CONFIGURAÇÃO GERAL ####
#############################
globals().clear()
""" Mudar diretório """
import os
from pathlib import Path
import getpass
if getpass.getuser() == "pedro":
    caminho_base = Path(r'D:\Códigos, Dados, Documentação e Cheat Sheets')
elif getpass.getuser() == "pedro-salj":
    caminho_base = Path(r'C:\Users\pedro-salj\Desktop\Pedro Nakashima\Códigos, Dados, Documentação e Cheat Sheets')

""" Mudar diretório para dados Siconfi"""
caminho_wd = caminho_base / 'Dados' / 'cnae e ncm'
os.chdir(caminho_wd)

######################################################################################
# CNAE 2.3 ###########################################################################
######################################################################################

def g_tabelões_cnaes():
    
    import pandas as pd
    dtype = {'Seção':'str','Divisão':'str','Grupo':'str','Classe':'str','subclasse':'str'}
    cnae = pd.read_excel('CNAE23_Subclasses_EstruturaDetalhada.xlsx',
                           sheet_name='estrutura',
                           skiprows=3,
                           dtype='str')
    
    cnae.rename(mapper={'Unnamed: 5':'Descrição'},axis=1,inplace=True)
    
    # Cria coluna com a versão
    cnae['Versão'] = '2.3'
    
    # Preenche para baixo
    cnae['Seção'].fillna(method='ffill', inplace=True)
    cnae['Divisão'].fillna(method='ffill', inplace=True)
    cnae['Grupo'].fillna(method='ffill', inplace=True)
    cnae['Classe'].fillna(method='ffill', inplace=True)
    cnae['Subclasse'].fillna(method='ffill', inplace=True)
    
    # Tira pontuação dos códigos
    cnae['Subclasse'] = cnae['Subclasse'].str.replace('-','').str.replace('/','')
    cnae['Classe'] = cnae['Classe'].str.replace('.','').str.replace('-','')
    cnae['Grupo'] = cnae['Grupo'].str.replace('.','')
    cnae['Descrição'] = cnae['Descrição'].str.replace('\n',' ')
    
    # Tira os espaços antes e depois dos códigos
    cnae['Seção'] = cnae['Seção'].str.strip()
    cnae['Divisão'] = cnae['Divisão'].str.strip()
    cnae['Grupo'] = cnae['Grupo'].str.strip()
    cnae['Classe'] = cnae['Classe'].str.strip()
    cnae['Subclasse'] = cnae['Subclasse'].str.strip()
    
    # Seleciona colunas
    cnae_Seção = cnae[['Versão', 'Seção', 'Descrição']]
    cnae_Divisão = cnae[['Versão', 'Divisão', 'Descrição']]
    cnae_Grupo = cnae[['Versão', 'Grupo', 'Descrição']]
    cnae_Classe = cnae[['Versão', 'Classe', 'Descrição']]
    cnae_Subclasse = cnae[['Versão', 'Subclasse', 'Descrição']]
    
    # Pega o primeiro
    cnae_Seção = cnae_Seção.groupby('Seção').first()
    cnae_Divisão = cnae_Divisão.dropna()
    cnae_Divisão = cnae_Divisão.groupby('Divisão').first()
    cnae_Grupo = cnae_Grupo.dropna()
    cnae_Grupo = cnae_Grupo.groupby('Grupo').first()
    cnae_Classe = cnae_Classe.dropna()
    cnae_Classe = cnae_Classe.groupby('Classe').first()
    cnae_Subclasse = cnae_Subclasse.dropna()
    cnae_Subclasse = cnae_Subclasse.groupby('Subclasse').first()
    
    # Reseta index
    cnae_Seção.reset_index(inplace=True)
    cnae_Divisão.reset_index(inplace=True)
    cnae_Grupo.reset_index(inplace=True)
    cnae_Classe.reset_index(inplace=True)
    cnae_Subclasse.reset_index(inplace=True)
    
    # Pega a correspondência: Divisão -> Seção (passo somente na versão 2.3)
    cnae_seção_corresp= cnae[['Subclasse', 'Classe', 'Grupo', 'Divisão', 'Seção']]
    cnae_seção_corresp.dropna(inplace=True)
    cnae_seção_corresp = cnae_seção_corresp.groupby('Divisão').head(1)
    cnae_seção_corresp = cnae_seção_corresp[['Divisão','Seção']]
    
    # Cria o DF maior
    todas_Seção = cnae_Seção.copy()
    todas_Divisão = cnae_Divisão.copy()
    todas_Grupo = cnae_Grupo.copy()
    todas_Classe = cnae_Classe.copy()
    todas_Subclasse = cnae_Subclasse.copy()
    
    ######################################################################################
    # CNAE 2.2 ###########################################################################
    ######################################################################################
    
    import pandas as pd
    dtype = {'Seção':'str','Divisão':'str','Grupo':'str','Classe':'str','subclasse':'str'}
    cnae = pd.read_excel('CNAE22_Subclasses_EstruturaDetalhada.xlsx',
                           sheet_name='estrutura',
                           skiprows=3,
                           dtype='str')
    
    #print(cnae.dtypes)
    cnae.drop(['Unnamed: 0'],axis=1,inplace=True)
    cnae.rename(mapper={'Unnamed: 1':'Seção','Unnamed: 2':'Divisão','Unnamed: 3':'Grupo','Unnamed: 4':'Classe','Unnamed: 5':'Subclasse','Denominação':'Descrição'},axis=1,inplace=True)
    cnae.drop([0],axis=0,inplace=True)
    
    # Deleta linhas lixo
    cond1 = ~ cnae['Seção'].str.contains('continuação', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('2.2', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('2.0', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('Seção', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('conclusão', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cnae = cnae.iloc[:-2] # deleta últimas duas linhas
    
    # Cria coluna com a versão
    cnae['Versão'] = '2.2'
    
    # Preenche para baixo
    cnae['Seção'].fillna(method='ffill', inplace=True)
    cnae['Divisão'].fillna(method='ffill', inplace=True)
    cnae['Grupo'].fillna(method='ffill', inplace=True)
    cnae['Classe'].fillna(method='ffill', inplace=True)
    cnae['Subclasse'].fillna(method='ffill', inplace=True)
    
    # Tira pontuação dos códigos
    cnae['Subclasse'] = cnae['Subclasse'].str.replace('-','').str.replace('/','')
    cnae['Classe'] = cnae['Classe'].str.replace('.','').str.replace('-','')
    cnae['Grupo'] = cnae['Grupo'].str.replace('.','')
    cnae['Descrição'] = cnae['Descrição'].str.replace('\n',' ')
    
    # Tira os espaços antes e depois dos códigos
    cnae['Seção'] = cnae['Seção'].str.strip()
    cnae['Divisão'] = cnae['Divisão'].str.strip()
    cnae['Grupo'] = cnae['Grupo'].str.strip()
    cnae['Classe'] = cnae['Classe'].str.strip()
    cnae['Subclasse'] = cnae['Subclasse'].str.strip()
    
    # Seleciona colunas
    cnae_Seção = cnae[['Versão', 'Seção', 'Descrição']]
    cnae_Divisão = cnae[['Versão', 'Divisão', 'Descrição']]
    cnae_Grupo = cnae[['Versão', 'Grupo', 'Descrição']]
    cnae_Classe = cnae[['Versão', 'Classe', 'Descrição']]
    cnae_Subclasse = cnae[['Versão', 'Subclasse', 'Descrição']]
    
    # Pega o primeiro
    cnae_Seção = cnae_Seção.groupby('Seção').first()
    cnae_Divisão = cnae_Divisão.dropna()
    cnae_Divisão = cnae_Divisão.groupby('Divisão').first()
    cnae_Grupo = cnae_Grupo.dropna()
    cnae_Grupo = cnae_Grupo.groupby('Grupo').first()
    cnae_Classe = cnae_Classe.dropna()
    cnae_Classe = cnae_Classe.groupby('Classe').first()
    cnae_Subclasse = cnae_Subclasse.dropna()
    cnae_Subclasse = cnae_Subclasse.groupby('Subclasse').first()
    
    # Reseta index
    cnae_Seção.reset_index(inplace=True)
    cnae_Divisão.reset_index(inplace=True)
    cnae_Grupo.reset_index(inplace=True)
    cnae_Classe.reset_index(inplace=True)
    cnae_Subclasse.reset_index(inplace=True)
    
    #cnae_Subclasse['len'] = cnae_Subclasse['Subclasse'].str.len()
    #print(cnae_Subclasse['len'].value_counts())
    
    # Adiciona ao DF maior
    todas_Seção = todas_Seção.append(cnae_Seção)
    todas_Divisão = todas_Divisão.append(cnae_Divisão)
    todas_Grupo = todas_Grupo.append(cnae_Grupo)
    todas_Classe = todas_Classe.append(cnae_Classe)
    todas_Subclasse = todas_Subclasse.append(cnae_Subclasse)
    
    ######################################################################################
    # CNAE 2.1 ###########################################################################
    ######################################################################################
    
    import pandas as pd
    dtype = {'Seção':'str','Divisão':'str','Grupo':'str','Classe':'str','subclasse':'str'}
    cnae = pd.read_excel('CNAE21_Subclasses_EstruturaDetalhada.xlsx',
                           sheet_name='estrutura',
                           skiprows=3,
                           dtype='str')
    
    #print(cnae.dtypes)
    cnae.drop(['Unnamed: 0'],axis=1,inplace=True)
    cnae.rename(mapper={'código CNAE 2.0':'Seção','Unnamed: 2':'Divisão','Unnamed: 3':'Grupo','Unnamed: 4':'Classe','Unnamed: 5':'Subclasse','Denominação':'Descrição'},axis=1,inplace=True)
    cnae.drop([0],axis=0,inplace=True)
    
    # Deleta linhas lixo
    cond1 = ~ cnae['Seção'].str.contains('continuação', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('2.2', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('2.0', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('Seção', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('conclusão', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cnae = cnae.iloc[:-2] # deleta últimas duas linhas
    
    # Cria coluna com a versão
    cnae['Versão'] = '2.1'
    
    # Preenche para baixo
    cnae['Seção'].fillna(method='ffill', inplace=True)
    cnae['Divisão'].fillna(method='ffill', inplace=True)
    cnae['Grupo'].fillna(method='ffill', inplace=True)
    cnae['Classe'].fillna(method='ffill', inplace=True)
    cnae['Subclasse'].fillna(method='ffill', inplace=True)
    
    # Tira pontuação dos códigos
    cnae['Subclasse'] = cnae['Subclasse'].str.replace('-','').str.replace('/','')
    cnae['Classe'] = cnae['Classe'].str.replace('.','').str.replace('-','')
    cnae['Grupo'] = cnae['Grupo'].str.replace('.','')
    cnae['Descrição'] = cnae['Descrição'].str.replace('\n',' ')
    
    # Tira os espaços antes e depois dos códigos
    cnae['Seção'] = cnae['Seção'].str.strip()
    cnae['Divisão'] = cnae['Divisão'].str.strip()
    cnae['Grupo'] = cnae['Grupo'].str.strip()
    cnae['Classe'] = cnae['Classe'].str.strip()
    cnae['Subclasse'] = cnae['Subclasse'].str.strip()
    
    # Seleciona colunas
    cnae_Seção = cnae[['Versão', 'Seção', 'Descrição']]
    cnae_Divisão = cnae[['Versão', 'Divisão', 'Descrição']]
    cnae_Grupo = cnae[['Versão', 'Grupo', 'Descrição']]
    cnae_Classe = cnae[['Versão', 'Classe', 'Descrição']]
    cnae_Subclasse = cnae[['Versão', 'Subclasse', 'Descrição']]
    
    # Pega o primeiro
    cnae_Seção = cnae_Seção.groupby('Seção').first()
    cnae_Divisão = cnae_Divisão.dropna()
    cnae_Divisão = cnae_Divisão.groupby('Divisão').first()
    cnae_Grupo = cnae_Grupo.dropna()
    cnae_Grupo = cnae_Grupo.groupby('Grupo').first()
    cnae_Classe = cnae_Classe.dropna()
    cnae_Classe = cnae_Classe.groupby('Classe').first()
    cnae_Subclasse = cnae_Subclasse.dropna()
    cnae_Subclasse = cnae_Subclasse.groupby('Subclasse').first()
    
    # Reseta index
    cnae_Seção.reset_index(inplace=True)
    cnae_Divisão.reset_index(inplace=True)
    cnae_Grupo.reset_index(inplace=True)
    cnae_Classe.reset_index(inplace=True)
    cnae_Subclasse.reset_index(inplace=True)
    
    # Adiciona ao DF maior
    todas_Seção = todas_Seção.append(cnae_Seção)
    todas_Divisão = todas_Divisão.append(cnae_Divisão)
    todas_Grupo = todas_Grupo.append(cnae_Grupo)
    todas_Classe = todas_Classe.append(cnae_Classe)
    todas_Subclasse = todas_Subclasse.append(cnae_Subclasse)
    
    ######################################################################################
    # CNAE 2.0 ###########################################################################
    ######################################################################################
    
    import pandas as pd
    dtype = {'Seção':'str','Divisão':'str','Grupo':'str','Classe':'str','subclasse':'str'}
    cnae = pd.read_excel('CNAE20_Subclasses_EstruturaDetalhada.xlsx',
                           sheet_name='estrutura',
                           skiprows=3,
                           dtype='str')
    
    #print(cnae.dtypes)
    cnae.drop(['Unnamed: 0'],axis=1,inplace=True)
    cnae.rename(mapper={'código CNAE 2.0':'Seção','Unnamed: 2':'Divisão','Unnamed: 3':'Grupo','Unnamed: 4':'Classe','Unnamed: 5':'Subclasse','Denominação':'Descrição'},axis=1,inplace=True)
    cnae.drop([0],axis=0,inplace=True)
    
    # Deleta linhas lixo
    cond1 = ~ cnae['Seção'].str.contains('continuação', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('2.2', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('2.0', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('Seção', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cond1 = ~ cnae['Seção'].str.contains('conclusão', regex=False, na=False)
    cnae = cnae.loc[cond1,:]
    cnae = cnae.iloc[:-2] # deleta últimas duas linhas
    
    # Cria coluna com a versão
    cnae['Versão'] = '2.0'
    
    # Preenche para baixo
    cnae['Seção'].fillna(method='ffill', inplace=True)
    cnae['Divisão'].fillna(method='ffill', inplace=True)
    cnae['Grupo'].fillna(method='ffill', inplace=True)
    cnae['Classe'].fillna(method='ffill', inplace=True)
    cnae['Subclasse'].fillna(method='ffill', inplace=True)
    
    # Tira pontuação dos códigos
    cnae['Subclasse'] = cnae['Subclasse'].str.replace('-','').str.replace('/','')
    cnae['Classe'] = cnae['Classe'].str.replace('.','').str.replace('-','')
    cnae['Grupo'] = cnae['Grupo'].str.replace('.','')
    cnae['Descrição'] = cnae['Descrição'].str.replace('\n',' ')
    
    # Tira os espaços antes e depois dos códigos
    cnae['Seção'] = cnae['Seção'].str.strip()
    cnae['Divisão'] = cnae['Divisão'].str.strip()
    cnae['Grupo'] = cnae['Grupo'].str.strip()
    cnae['Classe'] = cnae['Classe'].str.strip()
    cnae['Subclasse'] = cnae['Subclasse'].str.strip()
    
       #cnae['len'] = cnae['Subclasse'].str.len()
       #print(cnae['len'].value_counts())
    
    # Seleciona colunas
    cnae_Seção = cnae[['Versão', 'Seção', 'Descrição']]
    cnae_Divisão = cnae[['Versão', 'Divisão', 'Descrição']]
    cnae_Grupo = cnae[['Versão', 'Grupo', 'Descrição']]
    cnae_Classe = cnae[['Versão', 'Classe', 'Descrição']]
    cnae_Subclasse = cnae[['Versão', 'Subclasse', 'Descrição']]
    
    # Pega o primeiro
    cnae_Seção = cnae_Seção.groupby('Seção').first()
    cnae_Divisão = cnae_Divisão.dropna()
    cnae_Divisão = cnae_Divisão.groupby('Divisão').first()
    cnae_Grupo = cnae_Grupo.dropna()
    cnae_Grupo = cnae_Grupo.groupby('Grupo').first()
    cnae_Classe = cnae_Classe.dropna()
    cnae_Classe = cnae_Classe.groupby('Classe').first()
    cnae_Subclasse = cnae_Subclasse.dropna()
    cnae_Subclasse = cnae_Subclasse.groupby('Subclasse').first()
    
    # Reseta index
    cnae_Seção.reset_index(inplace=True)
    cnae_Divisão.reset_index(inplace=True)
    cnae_Grupo.reset_index(inplace=True)
    cnae_Classe.reset_index(inplace=True)
    cnae_Subclasse.reset_index(inplace=True)
    
    #cnae_Subclasse['len'] = cnae_Subclasse['Subclasse'].str.len()
    #print(cnae_Subclasse['len'].value_counts())
    
    # Adiciona ao DF maior
    todas_Seção = todas_Seção.append(cnae_Seção)
    todas_Divisão = todas_Divisão.append(cnae_Divisão)
    todas_Grupo = todas_Grupo.append(cnae_Grupo)
    todas_Classe = todas_Classe.append(cnae_Classe)
    todas_Subclasse = todas_Subclasse.append(cnae_Subclasse)
    
    #todas_Subclasse['len'] = todas_Subclasse['Subclasse'].str.len()
    #print(todas_Subclasse['len'].value_counts())
    
    
    # Pega a útlima versão
    todas_Seção.sort_values(by=['Seção','Versão'],ascending=[True,False],inplace=True)
    todas_Seção = todas_Seção.groupby(['Seção']).head(1)
    
    todas_Divisão.sort_values(by=['Divisão','Versão'],ascending=[True,False],inplace=True)
    todas_Divisão = todas_Divisão.groupby(['Divisão']).head(1)
    
    todas_Grupo.sort_values(by=['Grupo','Versão'],ascending=[True,False],inplace=True)
    todas_Grupo = todas_Grupo.groupby(['Grupo']).head(1)
    
    todas_Classe.sort_values(by=['Classe','Versão'],ascending=[True,False],inplace=True)
    todas_Classe = todas_Classe.groupby(['Classe']).head(1)
    
    todas_Subclasse.sort_values(by=['Subclasse','Versão'],ascending=[True,False],inplace=True)
    todas_Subclasse = todas_Subclasse.groupby(['Subclasse']).head(1)
    
    # Renomeia colunas
    todas_Seção.rename(mapper={'Seção':'cnae_seção_cod','Descrição':'cnae_seção_desc'},axis=1,inplace=True)
    todas_Divisão.rename(mapper={'Divisão':'cnae_divisão_cod','Descrição':'cnae_divisão_desc'},axis=1,inplace=True)
    todas_Grupo.rename(mapper={'Grupo':'cnae_grupo_cod','Descrição':'cnae_grupo_desc'},axis=1,inplace=True)
    todas_Classe.rename(mapper={'Classe':'cnae_classe_cod','Descrição':'cnae_classe_desc'},axis=1,inplace=True)
    todas_Subclasse.rename(mapper={'Subclasse':'cnae_subclasse_cod','Descrição':'cnae_subclasse_desc'},axis=1,inplace=True)
    
    # Gera DF de correspondências
    df_corresp = todas_Subclasse.copy()
    df_corresp.drop(['Versão','cnae_subclasse_desc'],axis=1,inplace=True)
    df_corresp['cnae_classe_cod'] = df_corresp['cnae_subclasse_cod'].str.slice(0,5)
    df_corresp['cnae_grupo_cod'] = df_corresp['cnae_subclasse_cod'].str.slice(0,3)
    df_corresp['cnae_divisão_cod'] = df_corresp['cnae_subclasse_cod'].str.slice(0,2)
    df_corresp = df_corresp.merge(cnae_seção_corresp,how='left',left_on='cnae_divisão_cod',right_on='Divisão')
    df_corresp.drop(['Divisão'],axis=1,inplace=True)
    df_corresp.rename(mapper={'Seção':'cnae_seção_cod'},axis=1,inplace=True)
    
    # Retorna DFs
    return df_corresp, todas_Seção, todas_Divisão, todas_Grupo, todas_Classe, todas_Subclasse

df_corresp, df_Seção, df_Divisão, df_Grupo, df_Classe, df_Subclasse = g_tabelões_cnaes()

######################################################################################
######################################################################################
######################################################################################

df_Subclasse.sort_values(by=['Versão'],ascending=[True],inplace=True)

df_corresp = df_corresp.groupby(['cnae_subclasse_cod']).head(1)
df_corresp = df_corresp.merge(df_Subclasse,how='left',left_on='cnae_subclasse_cod',right_on='cnae_subclasse_cod')
df_corresp = df_corresp.merge(df_Classe,how='left',left_on='cnae_classe_cod',right_on='cnae_classe_cod')

cond1 = df_corresp['Versão_x'] != df_corresp['Versão_y']
filtro = df_corresp.loc[cond1,:]

linhas_problemáticas = filtro.copy()












df_corresp.sort_values(by=['Versão'],ascending=[True],inplace=True)










print(df_corresp_2['Versão'].value_counts())


print(df_Subclasse['Versão'].value_counts())
print(df_Classe['Versão'].value_counts())
print(df_Grupo['Versão'].value_counts())
print(df_Divisão['Versão'].value_counts())
print(df_Seção['Versão'].value_counts())

print(df_Grupo['cnae_grupo_cod'].nunique())
######################################################################################
######################################################################################
######################################################################################

# Exporta para csv
df_corresp.to_csv('cnae_corresp.csv', sep='|', decimal=',', index=False)
df_Seção.to_csv('cnae_seção_desc.csv', sep='|', decimal=',', index=False)
df_Divisão.to_csv('cnae_divisão_desc.csv', sep='|', decimal=',', index=False)
df_Grupo.to_csv('cnae_grupo_desc.csv', sep='|', decimal=',', index=False)
df_Classe.to_csv('cnae_classe_desc.csv', sep='|', decimal=',', index=False)
df_Subclasse.to_csv('cnae_subclasse_desc.csv', sep='|', decimal=',', index=False)


import pandas as pd
pasta = caminho_base / 'Dados' / 'cnae e ncm'
arq_nome = 'cnae_corresp.csv'
#dtype_corresp = {'cnae23_Subclasse_cod7':'str','cnae23_Classe_cod5':'str','cnae23_Grupo_cod3':'str','cnae23_Divisão_cod2':'str','cnae23_Seção_cod1':'str'}
df_cnae_corresp = pd.read_csv(pasta / arq_nome,
                              delimiter = '|',
                              decimal=',')

df_cnae_corresp2 = df_cnae_corresp.groupby(['cnae_subclasse_cod']).first().reset_index()

print(df_cnae_corresp.dtypes)

print(df_cnae_corresp['cnae_subclasse_cod'].nunique())
print(df_cnae_corresp['cnae_classe_cod'].nunique())






# Renomeia colunas
cnae2_Subclasse.rename(mapper={'Descrição':'cnae2_Subclasse_desc'},axis=1,inplace=True)
cnae2_Classe.rename(mapper={'Descrição':'cnae2_Classe_desc'},axis=1,inplace=True)
cnae2_Grupo.rename(mapper={'Descrição':'cnae2_Grupo_desc'},axis=1,inplace=True)
cnae2_Divisão.rename(mapper={'Descrição':'cnae2_Divisão_desc'},axis=1,inplace=True)
cnae2_Seção.rename(mapper={'Descrição':'cnae2_Seção_desc'},axis=1,inplace=True)


# Renomeia colunas
cnae2.rename(mapper={'Subclasse':'cnae2_Subclasse_cod7'},axis=1,inplace=True)
cnae2.rename(mapper={'Classe':'cnae2_Classe_cod5'},axis=1,inplace=True)
cnae2.rename(mapper={'Grupo':'cnae2_Grupo_cod3'},axis=1,inplace=True)
cnae2.rename(mapper={'Divisão':'cnae2_Divisão_cod2'},axis=1,inplace=True)
cnae2.rename(mapper={'Seção':'cnae2_Seção_cod1'},axis=1,inplace=True)

cnae2['cnae2_Seção_cod1'].fillna(method='ffill', inplace=True)
cnae2['cnae2_Divisão_cod2'].fillna(method='ffill', inplace=True)
cnae2['cnae2_Grupo_cod3'].fillna(method='ffill', inplace=True)
cnae2['cnae2_Classe_cod5'].fillna(method='ffill', inplace=True)
cnae2['cnae2_Subclasse_cod7'].fillna(method='ffill', inplace=True)
cnae2['cnae2_Subclasse_cod7'] = cnae2['cnae2_Subclasse_cod7'].str.replace('-','').str.replace('/','')
cnae2['cnae2_Classe_cod5'] = cnae2['cnae2_Classe_cod5'].str.replace('.','').str.replace('-','')
cnae2['cnae2_Grupo_cod3'] = cnae2['cnae2_Grupo_cod3'].str.replace('.','')

cnae2_Seção = cnae2[['cnae2_Seção_cod1', 'Descrição']]
cnae2_Divisão = cnae2[['cnae2_Divisão_cod2', 'Descrição']]
cnae2_Grupo = cnae2[['cnae2_Grupo_cod3', 'Descrição']]
cnae2_Classe = cnae2[['cnae2_Classe_cod5', 'Descrição']]
cnae2_Subclasse = cnae2[['cnae2_Subclasse_cod7', 'Descrição']]

# Renomeia colunas
cnae2_Subclasse.rename(mapper={'Descrição':'cnae2_Subclasse_desc'},axis=1,inplace=True)
cnae2_Classe.rename(mapper={'Descrição':'cnae2_Classe_desc'},axis=1,inplace=True)
cnae2_Grupo.rename(mapper={'Descrição':'cnae2_Grupo_desc'},axis=1,inplace=True)
cnae2_Divisão.rename(mapper={'Descrição':'cnae2_Divisão_desc'},axis=1,inplace=True)
cnae2_Seção.rename(mapper={'Descrição':'cnae2_Seção_desc'},axis=1,inplace=True)


cnae2_Seção = cnae2_Seção.groupby('cnae2_Seção_cod1').first()
cnae2_Divisão = cnae2_Divisão.dropna()
cnae2_Divisão = cnae2_Divisão.groupby('cnae2_Divisão_cod2').first()
cnae2_Grupo = cnae2_Grupo.dropna()
cnae2_Grupo = cnae2_Grupo.groupby('cnae2_Grupo_cod3').first()
cnae2_Classe = cnae2_Classe.dropna()
cnae2_Classe = cnae2_Classe.groupby('cnae2_Classe_cod5').first()
cnae2_Subclasse = cnae2_Subclasse.dropna()
cnae2_Subclasse = cnae2_Subclasse.groupby('cnae2_Subclasse_cod7').first()

cnae2_Seção.reset_index(inplace=True)
cnae2_Divisão.reset_index(inplace=True)
cnae2_Grupo.reset_index(inplace=True)
cnae2_Classe.reset_index(inplace=True)
cnae2_Subclasse.reset_index(inplace=True)


# Exporta para csv
cnae2_Seção.to_csv('cnae2_Seção_desc.csv', sep=';', decimal=',', index=False)
cnae2_Divisão.to_csv('cnae2_Divisão_desc.csv', sep=';', decimal=',', index=False)
cnae2_Grupo.to_csv('cnae2_Grupo_desc.csv', sep=';', decimal=',', index=False)
cnae2_Classe.to_csv('cnae2_Classe_desc.csv', sep=';', decimal=',', index=False)
cnae2_Subclasse.to_csv('cnae2_Subclasse_desc.csv', sep=';', decimal=',', index=False)
del cnae2_Seção, cnae2_Divisão, cnae2_Grupo, cnae2_Classe, cnae2_Subclasse


cnae2_subclasses = cnae2[['cnae2_Subclasse_cod7', 'cnae2_Classe_cod5', 'cnae2_Grupo_cod3', 'cnae2_Divisão_cod2', 'cnae2_Seção_cod1']]


cnae2_subclasses.dropna(inplace=True)
cnae2_subclasses = cnae2_subclasses.groupby('cnae2_Subclasse_cod7').first()
cnae2_subclasses.reset_index(inplace=True)
cnae2_subclasses.sort_values(by='cnae2_Subclasse_cod7', inplace=True)

cnae2_classes = cnae2[['cnae2_Classe_cod5', 'cnae2_Grupo_cod3', 'cnae2_Divisão_cod2', 'cnae2_Seção_cod1']]
cnae2_classes.dropna(inplace=True)
cnae2_classes = cnae2_classes.groupby('cnae2_Classe_cod5').first()
cnae2_classes.reset_index(inplace=True)
cnae2_classes.sort_values(by='cnae2_Classe_cod5', inplace=True)


cnae2_grupos = cnae2[['cnae2_Grupo_cod3', 'cnae2_Divisão_cod2', 'cnae2_Seção_cod1']]
cnae2_grupos.dropna(inplace=True)
cnae2_grupos = cnae2_grupos.groupby('cnae2_Grupo_cod3').first()
cnae2_grupos.reset_index(inplace=True)
cnae2_grupos.sort_values(by='cnae2_Grupo_cod3', inplace=True)

cnae2_divisões = cnae2[['cnae2_Divisão_cod2', 'cnae2_Seção_cod1']]
cnae2_divisões.dropna(inplace=True)
cnae2_divisões = cnae2_divisões.groupby('cnae2_Divisão_cod2').first()
cnae2_divisões.reset_index(inplace=True)
cnae2_divisões.sort_values(by='cnae2_Divisão_cod2', inplace=True)

cnae2_subclasses.to_csv('cnae2_Subclasse_corresp.csv', sep=';', decimal=',', index=False)
cnae2_classes.to_csv('cnae2_Classe_corresp.csv', sep=';', decimal=',', index=False)
cnae2_grupos.to_csv('cnae2_Grupo_corresp.csv', sep=';', decimal=',', index=False)
cnae2_divisões.to_csv('cnae2_Divisão_corresp.csv', sep=';', decimal=',', index=False)



######################################################################################
# CNAE 2.0 ###########################################################################
######################################################################################

import pandas as pd
cnae20 = pd.read_excel('CNAE20_Subclasses_EstruturaDetalhada.xlsx', sheet_name='Est. Detalhada CNAE 2.0 - subcl')

print(cnae20.columns)

cnae20 = cnae20.drop(['Unnamed: 0'], axis=1)

cnae20 = cnae20.rename(columns={'2.2 Estrutura detalhada da CNAE 2.0: seções, divisões, grupos, classes e subclasses':'seção',
                                'Unnamed: 2':'divisão',
                                'Unnamed: 3':'grupo',
                                'Unnamed: 4':'classe',
                                'Unnamed: 5':'subclasse',
                                'Unnamed: 6':'descrição'})

cnae20 = cnae20.iloc[4:,]

cnae20.index = range(len(cnae20))

# Deleta linhas lixo
cond1 = ~ cnae20['seção'].str.contains('continuação', regex=False, na=False)
cnae20 = cnae20.loc[cond1,:]
cond1 = ~ cnae20['seção'].str.contains('2.2', regex=False, na=False)
cnae20 = cnae20.loc[cond1,:]
cond1 = ~ cnae20['seção'].str.contains('2.0', regex=False, na=False)
cnae20 = cnae20.loc[cond1,:]
cond1 = ~ cnae20['seção'].str.contains('Seção', regex=False, na=False)
cnae20 = cnae20.loc[cond1,:]
cond1 = ~ cnae20['seção'].str.contains('conclusão', regex=False, na=False)
cnae20 = cnae20.loc[cond1,:]

del cond1

print(cnae20.dtypes)
cnae20['seção'].fillna(method='ffill', inplace=True)
cnae20['divisão'].fillna(method='ffill', inplace=True)
cnae20['grupo'].fillna(method='ffill', inplace=True)
cnae20['classe'].fillna(method='ffill', inplace=True)
cnae20['subclasse'].fillna(method='ffill', inplace=True)


cnae20['subclasse'] = cnae20['subclasse'].str.replace('-','').str.replace('/','')
cnae20['classe'] = cnae20['classe'].str.replace('.','').str.replace('-','')
cnae20['grupo'] = cnae20['grupo'].str.replace('.','')

cnae20 = cnae20.iloc[:-2]

cnae20 = cnae20.astype('str')


cnae20_seção = cnae20[['seção', 'descrição']]
cnae20_divisão = cnae20[['divisão', 'descrição']]
cnae20_grupo = cnae20[['grupo', 'descrição']]
cnae20_classe = cnae20[['classe', 'descrição']]
cnae20_subclasse = cnae20[['subclasse', 'descrição']]

cnae20_seção = cnae20_seção.groupby('seção').first()

cnae20_divisão = cnae20_divisão.dropna()
cnae20_divisão = cnae20_divisão.groupby('divisão').first()

cnae20_grupo = cnae20_grupo.dropna()
cnae20_grupo = cnae20_grupo.groupby('grupo').first()

cnae20_classe = cnae20_classe.dropna()
cnae20_classe = cnae20_classe.groupby('classe').first()

cnae20_subclasse = cnae20_subclasse.dropna()
cnae20_subclasse = cnae20_subclasse.groupby('subclasse').first()

cnae20_seção.reset_index(inplace=True)
cnae20_divisão.reset_index(inplace=True)
cnae20_grupo.reset_index(inplace=True)
cnae20_classe.reset_index(inplace=True)
cnae20_subclasse.reset_index(inplace=True)

# Renomeia colunas
cnae20_subclasse.rename(mapper={'subclasse':'cnae2_subclasse_cod7','descrição':'cnae2_subclasse_desc'},axis=1,inplace=True)
cnae20_classe.rename(mapper={'classe':'cnae2_classe_cod5','descrição':'cnae2_classe_desc'},axis=1,inplace=True)
cnae20_grupo.rename(mapper={'grupo':'cnae2_grupo_cod3','descrição':'cnae2_grupo_desc'},axis=1,inplace=True)
cnae20_divisão.rename(mapper={'divisão':'cnae2_divisão_cod2','descrição':'cnae2_divisão_desc'},axis=1,inplace=True)
cnae20_seção.rename(mapper={'seção':'cnae2_seção_cod1','descrição':'cnae2_seção_desc'},axis=1,inplace=True)


# Exporta para csv
cnae20_seção.to_csv('cnae20_seção_desc.csv', sep=';', decimal=',', index=False)
cnae20_divisão.to_csv('cnae20_divisão_desc.csv', sep=';', decimal=',', index=False)
cnae20_grupo.to_csv('cnae20_grupo_desc.csv', sep=';', decimal=',', index=False)
cnae20_classe.to_csv('cnae20_classe_desc.csv', sep=';', decimal=',', index=False)
cnae20_subclasse.to_csv('cnae20_subclasse_desc.csv', sep=';', decimal=',', index=False)





del cnae20_seção, cnae20_divisão, cnae20_grupo, cnae20_classe, cnae20_subclasse

cnae20_subclasses = cnae20[['subclasse', 'classe', 'grupo', 'divisão', 'seção']]
cnae20_subclasses.dropna(inplace=True)
cnae20_subclasses = cnae20_subclasses.groupby('subclasse').first()
cnae20_subclasses.reset_index(inplace=True)
cnae20_subclasses.sort_values(by='subclasse', inplace=True)

cnae20_classes = cnae20[['classe', 'grupo', 'divisão', 'seção']]
cnae20_classes.dropna(inplace=True)
cnae20_classes = cnae20_classes.groupby('classe').first()
cnae20_classes.reset_index(inplace=True)
cnae20_classes.sort_values(by='classe', inplace=True)

cnae20_grupos = cnae20[['grupo', 'divisão', 'seção']]
cnae20_grupos.dropna(inplace=True)
cnae20_grupos = cnae20_grupos.groupby('grupo').first()
cnae20_grupos.reset_index(inplace=True)
cnae20_grupos.sort_values(by='grupo', inplace=True)

cnae20_divisões = cnae20[['divisão', 'seção']]
cnae20_divisões.dropna(inplace=True)
cnae20_divisões = cnae20_divisões.groupby('divisão').first()
cnae20_divisões.reset_index(inplace=True)
cnae20_divisões.sort_values(by='divisão', inplace=True)

cnae20_subclasses.to_csv('cnae20_subclasse_corresp.csv', sep=';', decimal=',', index=False)
cnae20_classes.to_csv('cnae20_classe_corresp.csv', sep=';', decimal=',', index=False)
cnae20_grupos.to_csv('cnae20_grupo_corresp.csv', sep=';', decimal=',', index=False)
cnae20_divisões.to_csv('cnae20_divisão_corresp.csv', sep=';', decimal=',', index=False)


print(cnae20_divisões.dtypes)



print(cnae20_divisões.dtypes)




