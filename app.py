import streamlit as st
import requests
from datetime import datetime

# Configuração da página web
st.set_page_config(page_title="Conversor ZPL para PDF", page_icon="🖨️")

st.title("🖨️ Conversor Online de ZPL para PDF")
st.write("Cole o seu código ZPL abaixo para gerar o PDF correspondente instantaneamente.")

# --- SEÇÃO DE DOAÇÃO / PIX ---
st.markdown("---")
st.success("💡 **Apoie este projeto!** Esta ferramenta é 100% gratuita. Se ela te ajudou a economizar tempo, considere apoiar para mantermos o site no ar!")

# Substitua os textos abaixo pelos seus dados
PIX_COPIA_E_COLA = "00020101021126780014BR.GOV.BCB.PIX2556pix-qr.mercadopago.com/instore/ol/v2/CyFD582SSDPmFBHr1NL5204000053039865802BR592560.883.693 KALLEU HENRIQU6009SAO PAULO62080504mpis63040B06"
SUA_CHAVE_CNPJ = "60883693000130"

col_pix1, col_pix2 = st.columns([1, 3])
with col_pix1:
    st.image(f"https://quickchart.io/qr?text={PIX_COPIA_E_COLA}&size=150", width=150)
with col_pix2:
    st.write(f"🔑 **Chave Pix (CNPJ):** `{SUA_CHAVE_CNPJ}`")
    st.write("📱 **Ou use o Pix Copia e Cola:**")
    st.code(PIX_COPIA_E_COLA, language="text")
st.markdown("---")

# Campos para o usuário configurar o tamanho da etiqueta
col1, col2 = st.columns(2)
with col1:
    largura = st.number_input("Largura (polegadas)", min_value=1, max_value=12, value=4)
with col2:
    altura = st.number_input("Altura (polegadas)", min_value=1, max_value=12, value=6)

# Campo de texto grande para inserir o ZPL
codigo_zpl = st.text_area("Código ZPL (Cole aqui):", height=250, placeholder="^XA\n^FO50,50^A0N,50,50^FDExemplo^FS\n^XZ")

# Botão para processar
if st.button("Gerar PDF", type="primary"):
    if not codigo_zpl.strip():
        st.warning("Por favor, insira um código ZPL válido primeiro.")
    else:
        with st.spinner("Processando e gerando PDF..."):
            # A URL atualizada sem o /0/ no final para aceitar múltiplas etiquetas
            url = f"http://api.labelary.com/v1/printers/8dpmm/labels/{largura}x{altura}/"
            headers = {"Accept": "application/pdf"}
            
            try:
                resposta = requests.post(url, headers=headers, data=codigo_zpl.encode('utf-8'))
                
                if resposta.status_code == 200:
                    st.success("PDF gerado com sucesso!")
                    
                    # --- GERAÇÃO DO NOME COM DATA E HORA ---
                    # Formato: etiquetas_DD-MM-AAAA_HH-MM.pdf
                    data_hora_atual = datetime.now().strftime("%d-%m-%Y_%H-%M")
                    nome_do_arquivo = f"etiquetas_{data_hora_atual}.pdf"
                    
                    # Cria o botão de download com o nome dinâmico
                    st.download_button(
                        label="📥 Baixar Arquivo PDF",
                        data=resposta.content,
                        file_name=nome_do_arquivo,
                        mime="application/pdf"
                    )
                else:
                    st.error(f"Erro na API do Labelary: {resposta.text}")
                    
            except Exception as e:
                st.error(f"Ocorreu um erro de conexão: {e}")
