import pdfplumber
import re
import sys
import os
import pandas as pd

# Regex
DAY_LINE_RE = re.compile(r'^\s*(\d{1,2})\s+([A-ZÇ]{2,4})\s+(.*)$', re.IGNORECASE)
TIME_PAIR_RE = re.compile(r'(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})')
HE_RE = re.compile(r'(-?\d+[,.]\d+|\(\*\))')     
NUM_RE = re.compile(r'\b\d{3}\b')                

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            t = pagina.extract_text()
            if t:
                texto += t + "\n"
    return texto

def limpar_para_numeros(rest):

    temp = TIME_PAIR_RE.sub(" ", rest)
    temp = HE_RE.sub(" ", temp)
    temp = re.sub(r'\(.*?\)', ' ', temp)
    temp = re.sub(r'\s+', ' ', temp)
    return temp.strip()

def processar_cartao_ponto(texto):
    linhas = texto.splitlines()
    registros = []

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        m = DAY_LINE_RE.match(linha)
        if not m:
            continue

        dia_num = m.group(1).zfill(2)
        dia_semana = m.group(2).upper()
        resto = m.group(3).strip()
        dia_completo = f"{dia_num} {dia_semana}"

        # Horários (entrada/saída + intervalos)
        horarios = TIME_PAIR_RE.findall(resto)
        entrada = saida = ""
        intervalos = ["", "", ""]
        if horarios:
            entrada, saida = horarios[0]
            for i in range(1, min(len(horarios), 4)):
                intervalos[i - 1] = f"{horarios[i][0]} - {horarios[i][1]}"

        # HE Diurno / Noturno (aceita números ou (*) )
        he_campos = [h.strip() for h in HE_RE.findall(resto)]
        he_diurno = he_campos[0].replace(',', '.') if len(he_campos) >= 1 else ""
        he_noturno = he_campos[1] if len(he_campos) >= 2 else ""

        # Entrada Saída (ou Descanso / Feriado)
        entrada_saida = ""
        if entrada and saida:
            entrada_saida = f"{entrada} - {saida}"
        elif re.search(r'Descanso', resto, re.IGNORECASE):
            entrada_saida = "Descanso Semanal"
        elif re.search(r'Feriado', resto, re.IGNORECASE):
            entrada_saida = "Feriado"

        # Extrair números finais (até 4 números de 3 dígitos)
        numeros_limp = limpar_para_numeros(resto)
        nums = NUM_RE.findall(numeros_limp)  
        atn = func = insalub = situac = ""
        if len(nums) >= 4:
            atn, func, insalub, situac = nums[-4:]
        elif len(nums) == 3:
            func, insalub, situac = nums[-3:]
        elif len(nums) == 2:
            func, situac = nums[-2:]
        elif len(nums) == 1:
            situac = nums[-1]

        # Conc = último S ou N (se houver)
        conc_match = re.findall(r'\b([SN])\b', resto, re.IGNORECASE)
        conc = conc_match[-1].upper() if conc_match else ""

        registros.append({
            "Dia": dia_completo,
            "Entrada Saída": entrada_saida,
            "Intervalo 1": intervalos[0],
            "Intervalo 2": intervalos[1],
            "Intervalo 3": intervalos[2],
            "HE Diurno": he_diurno,
            "HE Noturno": he_noturno,
            "ATN": atn,
            "Funç": func,
            "Situaç": situac,
            "Insalub": insalub,
            "Conc": conc
        })

    df = pd.DataFrame(registros, columns=[
        "Dia","Entrada Saída","Intervalo 1","Intervalo 2","Intervalo 3",
        "HE Diurno","HE Noturno","ATN","Funç","Situaç","Insalub","Conc"
    ])
    return df

def main():
    if len(sys.argv) < 3:
        print("Uso: python parse_time_card.py <entrada.pdf> <saida.xlsx>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    excel_saida = sys.argv[2]

    if not os.path.exists(pdf_path):
        print(f"Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    texto = extrair_texto_pdf(pdf_path)
    df = processar_cartao_ponto(texto)

    if df.empty:
        print("Nenhum registro encontrado!")
        sys.exit(1)

    os.makedirs(os.path.dirname(excel_saida) or ".", exist_ok=True)
    df.to_excel(excel_saida, index=False)
    print(f"Arquivo gerado com sucesso: {excel_saida}")

if __name__ == "__main__":
    main()
