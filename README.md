# Desafio Técnico - Quick Filler

## Descrição
Este projeto foi desenvolvido como parte do processo seletivo da Quick Filler.  
O objetivo é processar documentos em PDF (cartões de ponto e holerites) e extrair seus dados

Foram implementados dois scripts principais:
- `parse_time_card.py` → Responsável por processar o Cartão de Ponto.
- `parse_holerite_final.py` → Responsável por processar o Holerite.



## Estrutura do Projeto
```
desafio-programador/
│
├── inputs/ # PDFs de entrada
│ ├── Exemplos de cartão (pdf e xlsx)
│ ├── Exemplos de holertes (pdf e xlsx)
│
├── outputs/ # Planilhas geradas
│ ├── cartao_ponto1.xlsx
│ ├── holerite_01.xlsx
│
├── src/
│ └── parsers/
│ ├── parse_time_card.py # Parser do cartão de ponto
│ └── parse_holerite_final.py # Parser do holerite
│
├── requirements.txt # Dependências do projeto
├── README.md # Este arquivo
└── SOLUCAO.md # Documento técnico explicando a abordagem

```

## Pré-requisitos

- **Python 3.10 ou superior**
- **pip** instalado e configurado



## Instalação

1. **Clonar o repositório**
   
   ```
   git clone https://github.com/WallingtonAB/desafio-programador.git
   cd desafio-programador
   ```
   
**Criar ambiente virtual**

   ```
python -m venv venv
   ```

Ativar o ambiente virtual

**Windows:**

   ```
venv\Scripts\activate
   ```

**Linux / macOS:**

   ```
source venv/bin/activate
   ```

**Instalar dependências**

   ```
pip install -r requirements.txt

   ```

**Como Executar**

**Cartão de Ponto**
Executa a extração do PDF e gera a planilha transcrita:

   ```
python src/parsers/parse_time_card.py inputs/Exemplo-Cartao-Ponto-01.pdf outputs/cartao_ponto_transcrito.xlsx
   ```
**Holerite**
Executa a extração do PDF e gera a planilha transcrita:

   ```
python src/parsers/parse_holerite_final.py inputs/Exemplo-Holerite-01.pdf outputs/holerite_transcrito.xlsx
   ```

Após a execução, os arquivos .xlsx serão gerados dentro da pasta outputs/.

**Estrutura das Planilhas**

Cartão de Ponto
| Dia | Entrada Saída | Intervalo 1 | Intervalo 2 | Intervalo 3 | HE Diurno | HE Noturno | ATN | Funç | Situaç | Insalub | Conc |

Holerite
| Mês | Ano | Código | Descrição | Qtde | Valor | Tipo | Total Vencimentos | Total Descontos | Salário Antecipado em Férias | Saldo Devedor | Base INSS | Base IRRF | Base FGTS | FGTS a Depositar | Líquido a Receber |


**Dependências Principais**
Biblioteca -	Finalidade
pdfplumber -	Extração de texto de PDFs
pandas     -	Manipulação de dados e criação de planilhas
openpyxl   -	Escrita de arquivos .xlsx
