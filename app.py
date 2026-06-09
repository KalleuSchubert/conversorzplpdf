import streamlit as st
import requests
from datetime import datetime
import zipfile
import io

# Configuração da página web
st.set_page_config(page_title="Conversor ZPL para PDF", page_icon="🖨️")

st.title("🖨️ Conversor Online de ZPL para PDF")
st.write("Converta seus códigos ZPL colando o texto ou enviando um arquivo ZIP com várias etiquetas.")

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

# --- SISTEMA DE ABAS (Colar Texto vs Enviar ZIP) ---
aba1, aba2 = st.tabs(["📝 Colar Texto ZPL", "📦 Enviar Arquivo .ZIP"])

zpl_final_para_converter = ""

with aba1:
    codigo_texto = st.text_area("Código ZPL (Cole aqui):", height=200, placeholder="^XA\n^FO50,50^A0N,50,50^FDExemplo^FS\n^XZ")

with aba2:
    st.info("Envie um arquivo .zip contendo os seus arquivos .txt com os códigos ZPL. O sistema vai juntar tudo em um único PDF.")
    arquivo_zip_enviado = st.file_uploader("Selecione o arquivo .ZIP", type=["zip"])

# Botão para processar
if st.button("Gerar PDF", type="primary"):
    
    # Lógica para descobrir de onde vem o ZPL (da aba de texto ou da aba do ZIP)
    if arquivo_zip_enviado is not None:
        try:
            # Abre o ZIP na memória
            with zipfile.ZipFile(arquivo_zip_enviado) as z:
                # Passa por cada arquivo dentro do ZIP
                for nome_arquivo in z.namelist():
                    # Pega apenas arquivos .txt ou .zpl (ignora pastas e arquivos do sistema)
                    if nome_arquivo.endswith(".txt") or nome_arquivo.endswith(".zpl"):
                        with z.open(nome_arquivo) as f:
                            # Lê o texto e adiciona na variável final
                            conteudo = f.read().decode('utf-8', errors='ignore')
                            zpl_final_para_converter += conteudo + "\n"
        except Exception as e:
            st.error(f"Erro ao ler o arquivo ZIP: {e}")
            
    elif codigo_texto.strip():
        zpl_final_para_converter = codigo_texto.strip()

    # Validação antes de enviar para a API
    if not zpl_final_para_converter.strip():
        st.warning("Por favor, insira o código ZPL ou envie um arquivo ZIP válido contendo arquivos de texto.")
    else:
        with st.spinner("Processando e gerando PDF..."):
            url = f"http://api.labelary.com/v1/printers/8dpmm/labels/{largura}x{altura}/"
            headers = {"Accept": "application/pdf"}
            
            try:
                resposta = requests.post(url, headers=headers, data=zpl_final_para_converter.encode('utf-8'))
                
                if resposta.status_code == 200:
                    st.success("PDF gerado com sucesso!")
                    
                    data_hora_atual = datetime.now().strftime("%d-%m-%Y_%H-%M")
                    nome_do_arquivo = f"etiquetas_{data_hora_atual}.pdf"
                    
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
