import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from os import environ
import sqlalchemy

load_dotenv(find_dotenv())

URL_DB = environ.get('URL_DB')

def validar_planilha(data_frame: pd.DataFrame) -> None:
    colunas_esperadas = ['NFS_DATA_EMISSAO', 'NFS_NRO_NF', 'NFS_CLIENTE', 'NFS_RAZAO',
       'NFS_VENDEDOR', 'VEND_NOME', 'NFP_PRODUTO', 'NFP_PRODUTO_DESCRICAO',
       'NFP_UNIDADE_PRODUTO', 'NFP_PRECO_UNITARIO', 'NFP_RATEIO_DESC_TOTAL',
       'PRODUTO_GRUPO', 'GRUPO_DESCRICAO', 'PRODUTO_SUBGRUPO',
       'PRODUTO_CLASS_FISCAL', 'NAT_COD', 'NAT_DESC', 'SUBGRUPO_DESCRICAO',
       'NFP_PECAS', 'NFP_QTDE_PRODUTO', 'NFP_TOTAL_PRODUTO', 'DEDUCAO',
       'MEDIA', 'VALOR_COMISSAO', 'NFS_DH_RECBTO_NFE', 'CIDADE']
    
    if data_frame.empty:
        raise ValueError('Planilha Vazia')

    if list(data_frame.columns) != colunas_esperadas:
        raise TypeError('Colunas Incompatíveis')
    
    if not pd.api.types.is_datetime64_any_dtype(data_frame['NFS_DATA_EMISSAO']):
        raise TypeError('A coluna Data Compra não é do tipo datetime.')

    if not pd.api.types.is_datetime64_any_dtype(data_frame['NFS_DH_RECBTO_NFE']):
        raise TypeError('A coluna Data Devolução não é do tipo datetime.')
    
def formatar_df_confrigo(df_original: pd.DataFrame) -> pd.DataFrame:
    data_frame = df_original.copy()
    data_frame['PECAS'] = data_frame.apply(calcular_pecas, axis=1)
    data_frame['VEND_NOME'] = data_frame['VEND_NOME'].apply(lambda x: str(x).replace("_x000D_", "").strip())
    data_frame.loc[data_frame['VEND_NOME'] == 'VALTER ROBERTO ROCHA DE SOUZA', 'VEND_NOME'] = "GÉSSICA VASCONCELOS"
    
    return data_frame

def calcular_pecas(linha):
    if linha['NFP_PRODUTO'] in [6858, 20834, 16391, 6859, 20834]:
        return linha['NFP_PECAS'] / 2
    elif linha['NFP_PRODUTO'] in [8754, 7405, 6876, 6879, 16417, 6877]:
        return linha['NFP_PECAS']
    else:
        return 0

def formatar_df_frigosol(df_original: pd.DataFrame) -> pd.DataFrame:
    data_frame = df_original.copy()
    data_frame['VEND_NOME'] = data_frame['VEND_NOME'].apply(lambda x: str(x).replace("_x000D_", "").strip())
    
    return data_frame

def filtrar_novos_dados_confrigo(data_frame: pd.DataFrame) -> pd.DataFrame:
    conn = sqlalchemy.create_engine(URL_DB)
    query = 'SELECT NFS_NRO_NF FROM vendas_confrigo;'
    pedidos_registrados = pd.read_sql_query(query, conn)

    df_filtrado = data_frame[~data_frame['NFS_NRO_NF'].isin(pedidos_registrados['NFS_NRO_NF'])]
    
    return df_filtrado

def filtrar_novos_dados_frigosol(data_frame: pd.DataFrame) -> pd.DataFrame:
    conn = sqlalchemy.create_engine(URL_DB)
    query = 'SELECT NFS_NRO_NF FROM vendas_frigosol;'
    pedidos_registrados = pd.read_sql_query(query, conn)

    df_filtrado = data_frame[~data_frame['NFS_NRO_NF'].isin(pedidos_registrados['NFS_NRO_NF'])]
    
    return df_filtrado

def filtrar_novos_dados(data_frame: pd.DataFrame, tabela: str, campo: str = "NFS_NRO_NF"):
    conn = sqlalchemy.create_engine(URL_DB)
    query = f'SELECT {campo} FROM {tabela};'
    pedidos_registrados = pd.read_sql_query(query, conn)

    df_filtrado = data_frame[~data_frame[campo].isin(pedidos_registrados[campo])]
    
    return df_filtrado

def adicionar_registros_confrigo(novos_dados: pd.DataFrame) -> None:
    url_db = environ.get('URL_DB')
    conn = sqlalchemy.create_engine(url_db)  
    novos_dados.to_sql('vendas_confrigo', conn, if_exists='append', index=False)

def adicionar_registros_frigosol(novos_dados: pd.DataFrame) -> None:
    url_db = environ.get('URL_DB')
    conn = sqlalchemy.create_engine(url_db)  
    novos_dados.to_sql('vendas_frigosol', conn, if_exists='append', index=False)

def adicionar_registros(data_frame: pd.DataFrame, nome_tabela: str):
    conn = sqlalchemy.create_engine(URL_DB)  
    data_frame.to_sql(nome_tabela, conn, if_exists='append', index=False)