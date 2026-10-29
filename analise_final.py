
import pandas as pd

# Carregar a base tratada
df = pd.read_excel("vendas_tratadas.xlsx")

# Remover vendas com quantidade inválida
df = df[df["quantidade"] > 0].copy()

# Recalcular o total para corrigir divergências
df["valor_total"] = df["quantidade"] * df["valor_unitario"]

# 1. Valor médio por venda
valor_medio = df["valor_total"].mean()

# 2. Categoria com maior faturamento
vendas_categoria = df.groupby("categoria_produto")["valor_total"].sum()
maior_categoria = vendas_categoria.idxmax()
total_categoria = vendas_categoria.max()

# 3. As três cidades com mais vendas
vendas_cidade = (
    df.dropna(subset=["cidade"])
    .groupby("cidade")["id_venda"]
    .nunique()
    .sort_values(ascending=False)
    .head(3)
)

# 4. Idade média dos clientes
idade_media = df["idade_cliente"].mean()

# 5. Cliente com maior valor acumulado em compras
compras_cliente = df.groupby("id_cliente")["valor_total"].sum()
maior_cliente = compras_cliente.idxmax()
total_cliente = compras_cliente.max()

# Exibir os resultados
print("=== RESULTADOS DA ANÁLISE ===")
print(f"Registros utilizados: {len(df)}")
print(f"Valor médio por venda: R$ {valor_medio:.2f}")
print(f"Categoria com maior faturamento: {maior_categoria}")
print(f"Faturamento da categoria: R$ {total_categoria:.2f}")
print("\nTop 3 cidades por número de vendas:")
print(vendas_cidade)
print(f"\nIdade média dos clientes: {idade_media:.2f} anos")
print(f"Cliente com maior valor acumulado: {maior_cliente}")
print(f"Total acumulado desse cliente: R$ {total_cliente:.2f}")

# Salvar a base final utilizada na análise
df.to_excel("vendas_base_final.xlsx", index=False)
print("\nBase final salva em vendas_base_final.xlsx")
