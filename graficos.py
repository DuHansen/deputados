import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Criar pasta de imagens
os.makedirs("img", exist_ok=True)

# Função utilitária
def parse_valor(valor_str):
    return float(valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip())

# Carregar dados
with open("reembolso_total.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

df = pd.DataFrame(dados)
df["valor_float"] = df["value"].apply(parse_valor)
df["year"] = df["year"].astype(str)

# Gráficos
def salvar_grafico(fig, nome):
    caminho = f"img/{nome}.png"
    fig.savefig(caminho)
    plt.close(fig)
    return caminho

# 1. Top 10 deputados por gasto
fig1, ax1 = plt.subplots(figsize=(10, 6))
df.groupby("congressperson_name")["valor_float"].sum().sort_values(ascending=False).head(10).plot(kind="barh", ax=ax1, color="skyblue")
ax1.set_title("Top 10 Deputados por Valor de Reembolso")
ax1.set_xlabel("Total (R$)")
grafico1 = salvar_grafico(fig1, "top_deputados")

# 2. Gasto por subquota
fig2, ax2 = plt.subplots(figsize=(10, 6))
df.groupby("subquota")["valor_float"].sum().sort_values(ascending=False).head(10).plot(kind="bar", ax=ax2, color="orange")
ax2.set_title("Gasto por Subquota (Top 10)")
ax2.set_ylabel("Total (R$)")
ax2.tick_params(axis='x', rotation=45)
grafico2 = salvar_grafico(fig2, "gasto_subquota")

# 3. Reembolsos suspeitos
fig3, ax3 = plt.subplots(figsize=(6, 4))
df["suspicious"].value_counts().plot(kind="pie", labels=["Não Suspeito", "Suspeito"], autopct="%1.1f%%", colors=["green", "red"], ax=ax3)
ax3.set_title("Proporção de Reembolsos Suspeitos")
ax3.set_ylabel("")
grafico3 = salvar_grafico(fig3, "suspeitos")

# 4. Média por deputado
fig4, ax4 = plt.subplots(figsize=(10, 6))
df.groupby("congressperson_name")["valor_float"].mean().sort_values(ascending=False).head(10).plot(kind="barh", ax=ax4, color="purple")
ax4.set_title("Top 10 Deputados por Média de Reembolso")
ax4.set_xlabel("Média (R$)")
grafico4 = salvar_grafico(fig4, "media_reembolso")

# 5. Quantidade por deputado
fig5, ax5 = plt.subplots(figsize=(10, 6))
df["congressperson_name"].value_counts().head(10).plot(kind="bar", ax=ax5, color="teal")
ax5.set_title("Top 10 por Número de Reembolsos")
ax5.set_ylabel("Quantidade")
ax5.tick_params(axis='x', rotation=45)
grafico5 = salvar_grafico(fig5, "quantidade_deputados")

# 6. Top fornecedores
fig6, ax6 = plt.subplots(figsize=(10, 6))
df["supplier_info"].value_counts().head(10).plot(kind="barh", ax=ax6, color="gray")
ax6.set_title("Top 10 Fornecedores mais Utilizados")
ax6.set_xlabel("Número de Reembolsos")
grafico6 = salvar_grafico(fig6, "top_fornecedores")

# 7. Gasto por ano
fig7, ax7 = plt.subplots(figsize=(8, 5))
df.groupby("year")["valor_float"].sum().sort_index().plot(marker='o', ax=ax7, color="brown")
ax7.set_title("Gasto Total por Ano")
ax7.set_ylabel("Total (R$)")
ax7.set_xlabel("Ano")
grafico7 = salvar_grafico(fig7, "gasto_por_ano")

# PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatório de Reembolsos - Câmara dos Deputados", ln=True, align="C")

def inserir_grafico_pdf(titulo, caminho, largura=180):
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, titulo, ln=True)
    pdf.image(caminho, w=largura)

inserir_grafico_pdf("Top 10 Deputados por Valor de Reembolso", grafico1)
inserir_grafico_pdf("Gasto por Subquota", grafico2)
inserir_grafico_pdf("Proporção de Reembolsos Suspeitos", grafico3, largura=100)
inserir_grafico_pdf("Média de Reembolso por Deputado", grafico4)
inserir_grafico_pdf("Quantidade de Reembolsos por Deputado", grafico5)
inserir_grafico_pdf("Top Fornecedores mais Utilizados", grafico6)
inserir_grafico_pdf("Gasto Total por Ano", grafico7)

pdf.output("relatorio_reembolsos_completo.pdf")
print("✅ Relatório gerado com sucesso: relatorio_reembolsos_completo.pdf")
print("🖼️ Gráficos salvos na pasta 'img/'")
