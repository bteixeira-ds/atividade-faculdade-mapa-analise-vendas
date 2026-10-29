
import pandas as pd

# 1. Carregar a base de vendas
df = pd.read_excel("vendas.xlsx", sheet_name="Base_Vendas")

print("=== DIAGNÓSTICO INICIAL ===")

# 2. Quantidade de registros e atributos
print("\nDimensões da base:")
print("Registros:", df.shape[0])
print("Atributos:", df.shape[1])

# 3. Tipos de dados
print("\nTipos de dados:")
print(df.dtypes)

# 4. Valores ausentes
print("\nValores ausentes por coluna:")
print(df.isna().sum())

# 5. Registros duplicados
print("\nLinhas integralmente duplicadas:")
print(df.duplicated().sum())

print("\nIdentificadores de venda repetidos:")
print(df["id_venda"].duplicated().sum())

# 6. Valores suspeitos
print("\nIdades abaixo de zero ou acima de 100:")
print(
    df.loc[
        (df["idade_cliente"] < 0)
        | (df["idade_cliente"] > 100),
        ["id_venda", "idade_cliente"]
    ]
)

print("\nQuantidades iguais ou menores que zero:")
print(
    df.loc[
        df["quantidade"] <= 0,
        ["id_venda", "quantidade"]
    ]
)

# 7. Conferir valores monetários
print("\nTipos dos valores monetários:")
print(df[["valor_unitario", "valor_total"]].dtypes)

print("\nCategorias de cidades:")
print(sorted(df["cidade"].dropna().unique()))

print("\n=== FIM DO DIAGNÓSTICO ===")
