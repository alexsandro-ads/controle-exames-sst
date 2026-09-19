import io
import pandas as pd
import streamlit as st


# Função auxiliar para converter o DataFrame em formato Excel na memória
def converter_df_para_excel(df):
  output = io.BytesIO()
  with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Exames_SST')
  processed_data = output.getvalue()
  return processed_data


# Exemplo de botão no Streamlit para exportar dados
# Supondo que 'df_exames' seja o DataFrame exibido na tela:
if 'df_exames' in locals() and not df_exames.empty:
  excel_data = converter_df_para_excel(df_exames)

  st.download_button(
      label='📥 Baixar Relatório em Excel',
      data=excel_data,
      file_name='relatorio_exames_sst.xlsx',
      mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  )