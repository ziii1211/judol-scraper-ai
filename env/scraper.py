import asyncio
from playwright.async_api import async_playwright

async def main():
    # Memulai session Playwright
    async with async_playwright() as p:
        print("Membuka browser...")
        # headless=False artinya kita bisa lihat browsernya terbuka secara visual
        # Nanti saat jalan beneran, ubah jadi True biar jalan di background
        browser = await p.chromium.launch(headless=False) 
        
        # Buka tab baru
        page = await browser.new_page()
        
        target_url = "https://1wommr.com/?p=7cha" # Nanti kita ganti dengan URL target
        print(f"Menuju ke target: {target_url}")
        
        # Pergi ke URL dan tunggu sampai halaman selesai loading
        await page.goto(target_url, wait_until="networkidle")
        
        # Mengambil judul halaman
        judul = await page.title()
        print(f"Berhasil masuk! Judul Halaman: {judul}")
        
        # Mengambil seluruh teks yang ada di body (untuk bahan ekstraksi nanti)
        body_text = await page.locator("body").inner_text()
        print("Cuplikan teks di halaman:")
        print("-" * 30)
        print(body_text[:200]) # Print 200 karakter pertama saja
        print("-" * 30)
        
        # Tutup browser
        await browser.close()

# Menjalankan fungsi asynchronous
if __name__ == "__main__":
    asyncio.run(main())