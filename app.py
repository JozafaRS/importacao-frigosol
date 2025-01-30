import streamlit as st
import upload as up
import pandas as pd
import os

def processar_confrigo(arquivo):
    st.markdown(f'### -> {arquivo.name}')
    progresso = st.progress(0, 'Lendo arquivo...')

    try: 
        data_frame = pd.read_excel(arquivo)
    except:
        progresso.empty()
        st.error('Erro ao abrir arquivo')
        return
    
    progresso.progress(1/5, 'Validando planilha...')

    try:
        up.validar_planilha(data_frame)
    except Exception as e:
        progresso.empty()
        st.error(f'Planilha inválida. Erro: {e}')
        return

    progresso.progress(2/5, 'Filtrando Registros...')

    try:
        novos_dados = up.filtrar_novos_dados_confrigo(data_frame)
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao se conectar ao banco de dados. Error: {e}')
        return

    if novos_dados.empty:
        progresso.empty()
        st.warning('Não há dados novos na planilha')
        return
        
    progresso.progress(3/5, 'Formatando Planilha...')
    try: 
        df_formatado = up.formatar_df_confrigo(novos_dados)
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao formatar planilha: {e}')
        return

    progresso.progress(4/5, 'Enviando Dados...')

    try:
        #up.adicionar_registros_confrigo(df_formatado)
        progresso.progress(5/5, 'Finalizado!')
        progresso.empty()
        st.success(f'Base de dados atualizada com sucesso! {len(df_formatado)} registros adicionados')
    except Exception as e:
        progresso.empty()
        st.warning(f'Houve um erro ao enviar dados. Erro: {e}')
        return

def processar_frigosol(arquivo):
    st.markdown(f'### -> {arquivo.name}')
    progresso = st.progress(0, 'Lendo arquivo...')

    try: 
        data_frame = pd.read_excel(arquivo)
    except:
        progresso.empty()
        st.error('Erro ao abrir arquivo')
        return
    
    progresso.progress(1/5, 'Validando planilha...')

    try:
        up.validar_planilha(data_frame)
    except Exception as e:
        progresso.empty()
        st.error(f'Planilha inválida. Erro: {e}')
        return

    progresso.progress(2/5, 'Filtrando Registros...')

    try:
        novos_dados = up.filtrar_novos_dados_frigosol(data_frame)
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao se conectar ao banco de dados. Error: {e}')
        return

    if novos_dados.empty:
        progresso.empty()
        st.warning('Não há dados novos na planilha')
        return
        
    progresso.progress(3/5, 'Formatando Planilha...')
    try: 
        df_formatado = up.formatar_df_frigosol(novos_dados)
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao formatar planilha: {e}')
        return

    progresso.progress(4/5, 'Enviando Dados...')

    try:
        #up.adicionar_registros_frigosol(df_formatado)
        progresso.progress(5/5, 'Finalizado!')
        progresso.empty()
        st.success(f'Base de dados atualizada com sucesso! {len(df_formatado)} registros adicionados')
    except Exception as e:
        progresso.empty()
        st.warning(f'Houve um erro ao enviar dados. Erro: {e}')
        return

def page_upload():
    st.write("# FRIGOSOL")
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.header("Enviar dados para Banco")
        st.divider()
        arquivo_confrigo = st.file_uploader('Planilha Confrigo', ['xlsx', 'xls'])
        arquivo_frigosol = st.file_uploader('Planilha Frigosol', ['xlsx', 'xls'])
        botao = st.button('Enviar')

    with col2:
        st.header('Logs')
        st.divider()

        if (arquivo_frigosol or arquivo_confrigo) and botao:
            if arquivo_confrigo:
                processar_confrigo(arquivo_confrigo)
            
            if arquivo_frigosol:
                processar_frigosol(arquivo_frigosol)
                

def main():
    st.set_page_config(layout='wide', page_title="Frigosol")
    page_upload()

if __name__ == "__main__":
    main()