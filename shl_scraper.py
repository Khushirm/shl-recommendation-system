import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_shl_catalog():
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  
        page = await browser.new_page()
        await page.goto("https://www.shl.com/solutions/products/product-catalog/", timeout=60000)

        print("Waiting for table to load...")
        await page.wait_for_selector(".custom__table-wrapper", timeout=20000)

        
        await page.screenshot(path="shl_page.png")
        print("Screenshot taken. Check shl_page.png to verify page load.")

        rows = await page.query_selector_all(".custom__table-wrapper table tbody tr")
        print(f"Found {len(rows)} table rows")

        for i, row in enumerate(rows):
            cells = await row.query_selector_all("td")
            print(f"[Row {i}] Found {len(cells)} cells.")

            if len(cells) < 2:
                print(f"Skipping row {i} due to insufficient cells.")
                continue

            try:
                name_cell = cells[0]
                name_text = await name_cell.inner_text()
                link_el = await name_cell.query_selector("a")
                href = await link_el.get_attribute("href") if link_el else "N/A"

                remote_support = await cells[1].inner_text() if len(cells) > 1 else "Unknown"
                adaptive_support = await cells[2].inner_text() if len(cells) > 2 else "Unknown"
                duration = await cells[3].inner_text() if len(cells) > 3 else "Unknown"
                test_type = await cells[4].inner_text() if len(cells) > 4 else "Unknown"

                print(f"→ Row {i}: {name_text.strip()}")

                data.append({
                    "Assessment Name": name_text.strip(),
                    "URL": "https://www.shl.com" + href if href and href.startswith("/") else href,
                    "Remote Testing Support": remote_support.strip(),
                    "Adaptive/IRT Support": adaptive_support.strip(),
                    "Duration": duration.strip(),
                    "Test Type": test_type.strip()
                })

            except Exception as e:
                print(f"Error parsing row {i}: {e}")

        await browser.close()

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv("shl_assessments.csv", index=False)
    print(f"\n Scraped {len(df)} assessments. Saved to shl_assessments.csv")

# Run it
asyncio.run(scrape_shl_catalog())