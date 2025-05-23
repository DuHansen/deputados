import json
import glob

# Encontra todos os arquivos rembolso_*.json
arquivos = sorted(glob.glob("rembolso_*.json"))

dados_totais = []

for arquivo in arquivos:
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
        dados_totais.extend(dados)
        print(f"✅ Adicionados {len(dados)} itens de {arquivo}")

# Salva no arquivo final
with open("reembolso_total.json", "w", encoding="utf-8") as f:
    json.dump(dados_totais, f, ensure_ascii=False, indent=2)

print(f"\n📦 Arquivo final salvo como reembolso_total.json com {len(dados_totais)} registros.")
