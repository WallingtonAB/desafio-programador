# SOLUÇÃO TÉCNICA – Desafio Quick Filler
**Introdução**

Este projeto foi desenvolvido como parte do processo seletivo técnico da Quick Filler.
Meu objetivo principal foi aprender na prática e aplicar conceitos vistos no meu curso de Data Science, utilizando Python como linguagem base para que eu fosse possivel eu aprender e explorar extração e estruturação de dados a partir de documentos PDF.

Durante o desenvolvimento, utilizei pesquisas na internet, consultas à documentação oficial de bibliotecas e diversos exemplos técnicos e algumas soluções com AI para compreender como manipular textos, tabelas e expressões regulares.


**Motivação e Processo de Aprendizado**

Como ainda estou em fase de aprendizado em programação python e atualmente estudo Data Science, escolhi Python por ser uma linguagem muito utilizada em processamento de dados e análise de informações.
Meu foco foi entender de forma prática como as bibliotecas podem ser combinadas para transformar dados não estruturados (como PDFs) em informações úteis e organizadas.

**Ao longo do desafio, estudei temas como:**

Leitura e extração de texto com pdfplumber;

Expressões regulares para identificar padrões de texto;

Manipulação de tabelas com pandas;

Escrita e exportação de planilhas com openpyxl;



**Pensamento e Estrutura da Solução**
**Etapa 1 – Análise do Problema**

O desafio pedia a leitura de dois tipos de documentos em PDF:

Cartão de ponto, com registros diários de horários e horas extras;

Holerite, com dados financeiros e totais de vencimentos e descontos.

O requisito era converter essas informações em planilhas .xlsx com estrutura igual às planilhas modelo fornecidas.

```
parse_time_card.py → voltado para o tratamento de dados de ponto;

parse_holerite_final.py → voltado para os dados financeiros e totais.

```
**Etapa 2 – Escolha das Ferramentas**

pdfplumber foi escolhida por ser simples e confiável na extração de texto de PDFs baseados em texto (não imagem).

re (expressões regulares) foi usada para identificar padrões de datas, números, códigos e colunas dentro das linhas extraídas.

pandas foi usada para montar os DataFrames e exportar as planilhas Excel.

openpyxl foi utilizada como engine para salvar os arquivos .xlsx.

Essas bibliotecas são amplamente utilizadas em análise de dados.

**Etapa 3 – Design do Código**

**Cartão de Ponto (parse_time_card.py)**

O script identifica e extrai:

Dia e dia da semana (ex: "03 SEG");

Horários de entrada e saída;

Intervalos;

Horas extras diurnas e noturnas;

Campos adicionais como ATN, Funç, Situaç, Insalub e Conc.

A lógica foi construída com expressões regulares e com o objetivo de adaptar-se a pequenas variações de formatação nos PDFs.

**Holerite (parse_holerite_final.py)**

Este script é mais complexo, pois o documento possui múltiplas seções.(por isso não consegui fazer 100% preciso)
O raciocínio usado foi:

Dividir o PDF em blocos com base na ocorrência de “Mês/Ano:”.

Extrair para cada bloco os lançamentos (códigos, descrições, valores e quantidades).


**O script foi planejado para:**

Lidar com mais de um mês dentro do mesmo PDF;

Manter linhas vazias (sem perder informações parciais);


** Etapa 4 – Exportação dos Resultados **

Após a leitura e processamento, cada script exporta os dados para a pasta outputs/:

cartao_ponto_transcrito.xlsx

holerite_transcrito.xlsx

As planilhas foram testadas e comparadas com os exemplos fornecidos, mantendo o maximo possivel a mesma estrutura e formato de colunas.



# Conclusão

Esta solução foi desenvolvida com o objetivo de aprender e aplicar conhecimentos de Python e análise de dados que ainda sou iniciante, ao mesmo tempo em que cumpre todos os requisitos técnicos do desafio da Quick Filler.

Durante o desenvolvimento, pesquisei soluções, tutoriais, teste com IA(copilot do proprio vscode) e exemplos disponíveis online, adaptando-os à estrutura solicitada pela empresa e aprimorando meu entendimento sobre processamento de texto e automação de tarefas.

A escolha de Python foi proposital, por ser uma linguagem amplamente utilizada em Data Science e eu precisar aprender, área na qual estou me especializando.
