# 🧠 Motor NLP: Analisador e Resumidor de Documentos (Offline)

Uma aplicação de Inteligência Artificial desenvolvida em Python para processamento de linguagem natural (NLP). O sistema extrai, limpa e resume textos de documentos PDF pesados de forma 100% local.

## 🛡️ Foco em Privacidade e Segurança (Data Privacy)
Diferente de soluções baseadas em APIs em nuvem (como OpenAI/ChatGPT), esta aplicação utiliza a biblioteca `transformers` da Hugging Face para baixar e executar a Rede Neural **diretamente na máquina local**. Isso garante que **documentos corporativos sigilosos, contratos e relatórios financeiros nunca saiam do computador do usuário**, eliminando riscos de vazamento de dados de terceiros.

## ⚙️ Tecnologias Utilizadas (Arsenal)
* **Linguagem:** Python
* **Interface Web:** Streamlit
* **Inteligência Artificial:** PyTorch e Hugging Face Transformers (`facebook/bart-large-cnn`)
* **Processamento de Dados:** PyPDF2 e Regex (para limpeza e compressão de ruídos de texto e limitação de *Context Window*).

## 🚀 Funcionalidades e Engenharia
* **Extração Direta:** Leitura otimizada de PDFs.
* **UX Constraint:** Para evitar o transbordamento da memória de tensores do modelo (Token Overflow), a interface foi projetada com um slider de travamento matemático, limitando a ingestão de dados a blocos de 3 páginas por vez.
* **Data Cleaning Automático:** Uso de Expressões Regulares (`re`) para purificar o texto bruto extraído do PDF antes de enviá-lo para a rede neural.
* **Ajuste de Inferência:** Parâmetros `min_length` e `max_length` otimizados para forçar o modelo a gerar resumos executivos densos e detalhados.

## 💻 Como Rodar Localmente
Como este projeto roda um modelo de Deep Learning, é necessário executá-lo na sua própria máquina.

1. Clone este repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Inicie o servidor local do Streamlit: `python -m streamlit run app_ia.py`
*(Nota: O primeiro uso fará o download do modelo base, o que pode levar alguns minutos dependendo da conexão).*
