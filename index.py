import asyncio
import json
from playwright.async_api import async_playwright

BASE_URL = "https://jarbas.serenata.ai/dashboard/chamber_of_deputies/reimbursement/?p="
TOTAL_PAGES = 10  # Altere para 47379 se desejar todas as páginas

async def scrape_page(page, index):
    url = f"{BASE_URL}{index}"
    print(f"🔎 Acessando: {url}")
    try:
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)
        except Exception as e:
            print(f"⚠️ Timeout ou falha ao carregar página {index}, ignorando...")
            return []

        await page.wait_for_selector("tr.row1, tr.row2", timeout=10000)
        rows = await page.query_selector_all("tr.row1, tr.row2")
        data = []

        for row in rows:
            cells = await row.query_selector_all("td, th")
            text = [await c.inner_text() for c in cells]

            # Social links
            social_links = await cells[2].query_selector_all("a")
            social = [await a.get_attribute("href") for a in social_links]

            # Jarbas link
            jarbas_a = await cells[1].query_selector("a")
            jarbas_link = await jarbas_a.get_attribute("href") if jarbas_a else None

            # Suspicious
            suspicious_img = await cells[10].query_selector("img")
            suspicious = await suspicious_img.get_attribute("alt") if suspicious_img else "False"

            data.append({
                "document_id": text[0].strip(),
                "jarbas_link": jarbas_link,
                "social_profiles": social,
                "rosies_tweet": text[3].strip(),
                "receipt_link": text[4].strip(),
                "congressperson_name": text[5].strip(),
                "year": text[6].strip(),
                "subquota": text[7].strip(),
                "supplier_info": text[8].strip(),
                "value": text[9].strip(),
                "suspicious": suspicious == "True"
            })

        return data

    except Exception as e:
        print(f"❌ Erro inesperado na página {index}: {e}")
        return []

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i in range(TOTAL_PAGES):
            page_data = await scrape_page(page, i)
            file_name = f"rembolso_{i+1}.json"

            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(page_data, f, ensure_ascii=False, indent=2)

            print(f"💾 Página {i+1} salva em {file_name}")
            await asyncio.sleep(2)  # Evita bloqueio por requisições rápidas

        await browser.close()

    print("✅ Scraping finalizado com arquivos separados por página.")

if __name__ == "__main__":
    asyncio.run(main())
