
import pandas as pd
import unicodedata
import re

# 1. Carregar a base original
df = pd.read_excel("vendas.xlsx", sheet_name="Base_Vendas")

print("Base original:", df.shape)

# 2. Remover apenas linhas integralmente duplicadas
duplicados = df.duplicated().sum()
df = df.drop_duplicates().copy()

print("Linhas integralmente duplicadas removidas:", duplicados)

# 3. Padronizar os nomes das cidades
def normalizar_texto(texto):
    texto = str(texto).strip().upper()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )
    texto = re.sub(r"\s+", " ", texto)
    return texto

mapa_cidades = {
    "ARACAJU": "Aracaju",
    "BELO HORIZONTE": "Belo Horizonte",
    "CURITIBA": "Curitiba",
    "FORTALEZA": "Fortaleza",
    "JOAO PESSOA": "João Pessoa",
    "MACEIO": "Maceió",
    "NATAL": "Natal",
    "PORTO ALEGRE": "Porto Alegre",
    "RECIFE": "Recife",
    "RIO DE JANEIRO": "Rio de Janeiro",
    "RIO JANEIRO": "Rio de Janeiro",
    "SALVADOR": "Salvador",
    "SAO PAULO": "São Paulo",
    "SAOPAULO": "São Paulo"
}

df["cidade"] = df["cidade"].apply(
    lambda x: (
        mapa_cidades.get(normalizar_texto(x), pd.NA)
        if pd.notna(x) else pd.NA
    )
)

print("\nCidades após padronização:")
print(sorted(df["cidade"].dropna().unique()))

# 4. Converter valores monetários para números
def converter_moeda(valor):
    if pd.isna(valor):
        return pd.NA

    if isinstance(valor, (int, float)):
        return float(valor)

    texto = str(valor).strip()
    texto = texto.replace("R$", "").replace(" ", "")

    if "," in texto:
        texto = texto.replace(".", "")
        texto = texto.replace(",", ".")

    return pd.to_numeric(texto, errors="coerce")

for coluna in ["valor_unitario", "valor_total"]:
    df[coluna] = df[coluna].apply(converter_moeda)

# 5. Converter colunas numéricas
for coluna in ["idade_cliente", "quantidade"]:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# 6. Tratar idades inválidas
df.loc[
    (df["idade_cliente"] < 0) |
    (df["idade_cliente"] > 100),
    "idade_cliente"
] = pd.NA

# Preencher idades ausentes com a mediana
mediana_idade = df["idade_cliente"].median()
df["idade_cliente"] = df["idade_cliente"].fillna(mediana_idade)

# 7. Investigar quantidades inválidas
print("\nRegistros com quantidade zero ou negativa:")
print(df.loc[df["quantidade"] <= 0])

# 8. Verificar vendas com valores inconsistentes
df["total_calculado"] = (
    df["quantidade"] * df["valor_unitario"]
)

inconsistencias = df.loc[
    df["valor_total"].notna()
    & df["total_calculado"].notna()
    & ((df["valor_total"] - df["total_calculado"]).abs() > 0.01)
]

print("\nVendas com total diferente de quantidade x valor unitário:")
print(inconsistencias[
    ["id_venda", "quantidade", "valor_unitario",
     "valor_total", "total_calculado"]
])

# 9. Conferir identificadores repetidos
print("\nIdentificadores de venda repetidos após remover cópias exatas:")
print(
    df.loc[df["id_venda"].duplicated(keep=False)]
    .sort_values("id_venda")
)

# 10. Conferir a qualidade após os tratamentos
print("\nDimensões após tratamento inicial:", df.shape)
print("\nValores ausentes restantes:")
print(df.isna().sum())

# 11. Salvar uma cópia tratada
df.to_excel("vendas_tratadas.xlsx", index=False)

print("\nArquivo vendas_tratadas.xlsx salvo!")
