import streamlit as st
import PyPDF2
from transformers import pipeline
import re  # <-- NOVO: Biblioteca de Expressões Regulares para limpar textos

# 1. Configuração da Interface Web
st.set_page_config(page_title="Resumidor de PDF com IA", layout="centered")

st.title("🧠 Motor de IA: Resumo de Documentos")
st.markdown("Faça o upload de um arquivo PDF e a nossa Inteligência Artificial fará a leitura e o resumo automático do conteúdo.")
st.divider()

@st.cache_resource
def carregar_ia():
    return pipeline("summarization", model="facebook/bart-large-cnn")

# 3. A Zona de Interação com o Usuário
arquivo_pdf = st.file_uploader("Arraste o seu contrato ou relatório em PDF aqui", type=["pdf"])

if arquivo_pdf is not None:
    # A. Extração de Texto e Controle de Páginas
    leitor = PyPDF2.PdfReader(arquivo_pdf)
    total_paginas = len(leitor.pages)
    
    st.info(f"O documento possui {total_paginas} páginas.")
    
    # ======== A SUA ENGENHARIA DE INTERFACE ========
    # O usuário escolhe apenas a página de início. 
    # O limite máximo do slider impede que ele passe do fim do livro.
    limite_maximo_slider = max(1, total_paginas - 2)
    
    pagina_inicio = st.slider(
        "Selecione a página inicial (A IA fará a leitura de um bloco fixo de 3 páginas)", 
        min_value=1, 
        max_value=limite_maximo_slider, 
        value=1
    )
    
    # O sistema calcula automaticamente o fim (travado em 3 páginas)
    pagina_fim = min(pagina_inicio + 2, total_paginas)
    # ================================================
    
    with st.spinner(f"Extraindo texto (Páginas {pagina_inicio} a {pagina_fim})..."):
        texto_completo = ""
        for i in range(pagina_inicio - 1, pagina_fim):
            pagina = leitor.pages[i]
            texto_extraido = pagina.extract_text()
            if texto_extraido:
                texto_completo += texto_extraido + " "
                
        # ======== O TRUQUE DE LIMPEZA DE DADOS (REGEX) ========
        # Transforma múltiplos espaços, quebras de linha e tabulações em apenas 1 espaço simples.
        # Isso impede o "token overflow" (estouro de memória).
        texto_limpo = re.sub(r'\s+', ' ', texto_completo).strip()
        # ======================================================
            
    st.subheader(f"📄 Texto Bruto Extraído (Páginas {pagina_inicio} a {pagina_fim})")
    # Agora mostramos o texto limpo na tela para você ver a diferença
    st.text_area("Amostra do texto após a limpeza de ruídos:", texto_limpo[:1000] + "...", height=150)
    
    # B. O Processamento Neural (NLP)
    if st.button("Ativar IA e Gerar Resumo"):
        with st.spinner("A Inteligência Artificial está lendo e criando o resumo. Aguarde..."):
            resumidor = carregar_ia()
            
            # Pegamos o texto já limpo e comprimido
            texto_para_ia = texto_limpo[:2500] 
            
            try:
                # Expandimos a janela: a IA agora é obrigada a gerar no mínimo 100 tokens, e pode ir até 300.
                resultado = resumidor(texto_para_ia, max_length=300, min_length=100, do_sample=False, truncation=True)
                
                st.success("Análise Concluída com Sucesso!")
                st.subheader("🎯 Resumo Executivo:")
                st.info(resultado[0]['summary_text'])
                
            except Exception as e:
                st.error(f"Erro na matriz de processamento: {e}")