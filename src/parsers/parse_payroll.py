import pdfplumber
import re
import pandas as pd
import sys
import os



def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            t = pagina.extract_text()
            if t:
                texto += t + "\n"
    return texto



def separar_blocos_por_mes(texto):
    partes = re.split(r'(M[eê]s\/Ano\s*:\s*\d{2}\/\d{4})', texto, flags=re.IGNORECASE)
    blocos = []
    i = 1
    while i < len(partes):
        header = partes[i]
        corpo = partes[i + 1] if i + 1 < len(partes) else ""
        match = re.search(r'(\d{2})\/(\d{4})', header)
        if match:
            mes, ano = match.groups()
            blocos.append((mes, ano, corpo))
        i += 2
    return blocos



def extrair_totais_e_bases(linhas):
    totals = {
        "Total Vencimentos": "",
        "Total Descontos": "",
        "Salário Antecipado em Férias": "",
        "Saldo Devedor": "",
        "Base INSS": "",
        "Líquido a Receber": "",
        "Base IRRF": "",
        "Base FGTS": "",
        "FGTS a Depositar": ""
    }

    for idx, l in enumerate(linhas):
        l_norm = re.sub(r'\s{2,}', ' ', l).strip()

        
        if re.search(r'\bTOTAL\b', l_norm, re.IGNORECASE):
            nums = re.findall(r'[\d,.]+', l_norm)
            if len(nums) >= 2:
                totals["Total Vencimentos"], totals["Total Descontos"] = nums[-2:]
            elif idx + 1 < len(linhas):
                nums2 = re.findall(r'[\d,.]+', linhas[idx + 1])
                if len(nums2) >= 2:
                    totals["Total Vencimentos"], totals["Total Descontos"] = nums2[-2:]

        
        if re.match(r'^\s*13\.', l_norm):
            if idx + 1 < len(linhas):
                next_line = linhas[idx + 1]
                nums = re.findall(r'[\d,.]+', next_line)
                if len(nums) >= 4:
                    totals["Salário Antecipado em Férias"] = nums[0]
                    totals["Saldo Devedor"] = nums[1]
                    totals["Base INSS"] = nums[2]
                    totals["Líquido a Receber"] = nums[3]

        
        if re.search(r'Base C[áa]lculo IRRF', l_norm, re.IGNORECASE):
            nums = re.findall(r'[\d,.]+', l_norm)
            if nums:
                totals["Base IRRF"] = nums[-1]
            elif idx + 1 < len(linhas):
                nums2 = re.findall(r'[\d,.]+', linhas[idx + 1])
                if nums2:
                    totals["Base IRRF"] = nums2[-1]

        if re.search(r'Base C[áa]lculo FGTS', l_norm, re.IGNORECASE):
            nums = re.findall(r'[\d,.]+', l_norm)
            if nums:
                totals["Base FGTS"] = nums[-1]
            elif idx + 1 < len(linhas):
                nums2 = re.findall(r'[\d,.]+', linhas[idx + 1])
                if nums2:
                    totals["Base FGTS"] = nums2[-1]

        if re.search(r'FGTS a ser Depositado', l_norm, re.IGNORECASE):
            nums = re.findall(r'[\d,.]+', l_norm)
            if nums:
                totals["FGTS a Depositar"] = nums[-1]
            elif idx + 1 < len(linhas):
                nums2 = re.findall(r'[\d,.]+', linhas[idx + 1])
                if nums2:
                    totals["FGTS a Depositar"] = nums2[-1]

    return totals



# Extrai lançamentos (códigos/descrições/valores)

def extrair_lancamentos(linhas):
    registros = []
    padrao_linha = re.compile(r'^(?!\d+\.)\s*([\/A-Z]?\d{2,5})\s+(.+?)\s+([\d.,]+)?\s+([\d.,]+)$')

    for l in linhas:
        l_clean = re.sub(r'\s{2,}', ' ', l).strip()
        if not l_clean:
            continue

        # ignora linhas de totais / bases / mensagens
        if any(p in l_clean.lower() for p in [
            "salário antecipado", "saldo devedor", "base cálculo", "base calculo",
            "líquido", "total", "mensagens", "fls", "rateio", "acumulado"
        ]):
            continue

        m = padrao_linha.match(l_clean)
        if m:
            codigo = m.group(1).strip()
            descricao = m.group(2).strip()
            qtde = m.group(3) or ""
            valor = m.group(4) or ""
            tipo = "Desconto" if (codigo.startswith("5") or codigo.startswith("M") or codigo.startswith("/")) else "Provento"
            registros.append({
                "Código": codigo,
                "Descrição": descricao,
                "Qtde": qtde,
                "Valor": valor,
                "Tipo": tipo
            })

    return registros



def processar_bloco(mes, ano, bloco_texto):
    linhas = [l for l in (ln.strip() for ln in bloco_texto.splitlines()) if l]
    totals = extrair_totais_e_bases(linhas)
    lancamentos = extrair_lancamentos(linhas)

    df = pd.DataFrame(lancamentos)
    if df.empty:
        return df

    
    df["Mês"] = mes
    df["Ano"] = ano
    for k, v in totals.items():
        df[k] = v

    colunas = [
        "Mês", "Ano", "Código", "Descrição", "Qtde", "Valor", "Tipo",
        "Total Vencimentos", "Total Descontos",
        "Salário Antecipado em Férias", "Saldo Devedor",
        "Base INSS", "Base IRRF", "Base FGTS",
        "FGTS a Depositar", "Líquido a Receber"
    ]

    # Reordenar (garante colunas fixas)
    df = df.reindex(columns=colunas, fill_value="")
    return df



def processar_pdf_uma_aba(caminho_pdf, caminho_saida_xlsx):
    texto = extrair_texto_pdf(caminho_pdf)
    blocos = separar_blocos_por_mes(texto)

    if not blocos:
        raise RuntimeError("Nenhum bloco detectado (Mês/Ano) no PDF.")

    lista_df = []
    for mes, ano, bloco in blocos:
        df = processar_bloco(mes, ano, bloco)
        if not df.empty:
            lista_df.append(df)

    if not lista_df:
        raise RuntimeError("Nenhum lançamento encontrado no PDF.")

    df_total = pd.concat(lista_df, ignore_index=True)

    os.makedirs(os.path.dirname(caminho_saida_xlsx) or ".", exist_ok=True)
    with pd.ExcelWriter(caminho_saida_xlsx, engine="openpyxl") as writer:
        df_total.to_excel(writer, sheet_name="Holerites", index=False)

    print(f"Planilha criada com sucesso: {caminho_saida_xlsx}")



def main():
    if len(sys.argv) < 3:
        print("Uso: python parse_holerite_final.py <entrada.pdf> <saida.xlsx>")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    if not os.path.exists(entrada):
        print(f" Arquivo não encontrado: {entrada}")
        sys.exit(1)

    try:
        processar_pdf_uma_aba(entrada, saida)
    except Exception as e:
        print(" Erro:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
