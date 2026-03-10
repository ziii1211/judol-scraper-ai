import asyncio
import re  # Modul bawaan Python untuk Regex
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Membuka browser...")
        # Kita set headless=False agar kita bisa melihat dan menggeser puzzle secara manual
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()
        
        target_url = "https://1wommr.com/?p=7cha" # URL targetmu
        print(f"Menuju ke target: {target_url}")
        
        try:
            # 1. Masuk ke halaman utama
            await page.goto(target_url, wait_until="networkidle", timeout=30000)
            judul = await page.title()
            print(f"Berhasil masuk! Judul Halaman: {judul}")
            
            # --- PROSES LOGIN OTOMATIS ---
            print("\n[*] Membuka pop-up login...")
            
            # Mencari tombol yang mengandung kata "Log in", "Login", atau "Masuk" dan klik
            tombol_buka_login = page.locator("text=/Log in|Login|Masuk/i").first
            if await tombol_buka_login.is_visible():
                await tombol_buka_login.click()
                # Tunggu 2 detik biarkan animasi pop-up form login muncul sempurna
                await page.wait_for_timeout(2000) 
            
            print("[*] Mencoba mengisi form login...")
            
            # Karena pakai nomor HP/Email, kita ambil elemen kotak input "text" atau "email" atau "tel" yang pertama muncul
            kotak_user = page.locator('input[type="text"], input[type="email"], input[type="tel"]').first
            
            # MASUKKAN NOMOR HP / EMAIL SAMARANMU DI SINI
            await kotak_user.fill('+6285651424932') 
            
            # Mengisi Password (otomatis nyari kotak khusus password)
            kotak_pass = page.locator('input[type="password"]').first
            await kotak_pass.fill('apaajasaja24')
            
            # Trik Jitu: Tekan ENTER langsung di kotak password biar otomatis submit
            print("[*] Menekan tombol Enter...")
            await kotak_pass.press('Enter')
            
            # --- TAMBAHAN UNTUK BYPASS PUZZLE (HUMAN-IN-THE-LOOP) ---
            print("\n[!] PERHATIAN: JIKA MUNCUL PUZZLE GESER, SILAKAN GESER MANUAL SEKARANG DI BROWSER!")
            print("[*] Bot memberikan waktu maksimal 60 detik untuk kamu menyelesaikan puzzle...")
            
            try:
                # Bot akan diam dan memantau. Dia menunggu sampai berhasil masuk ke dashboard dan jaringan tenang.
                await page.wait_for_load_state("networkidle", timeout=60000) 
            except Exception:
                print("[!] Waktu tunggu habis atau halaman belum selesai loading sepenuhnya. Lanjut memindai...")
            
           print("[+] Asumsi sudah berhasil masuk ke dalam akun!")
            
            # --- MENUJU HALAMAN DEPOSIT ---
            print("\n[*] Mencari tombol Deposit...")
            
            # Bot akan mencari tombol yang tulisannya "Deposit", "Isi Saldo", atau "Top Up"
            tombol_deposit = page.locator("text=/Deposit|Isi Saldo|Top Up/i").first
            
            if await tombol_deposit.is_visible():
                print("[*] Tombol Deposit ditemukan! Mengklik...")
                await tombol_deposit.click()
                
                # Tunggu 5 detik agar halaman deposit / pop-up deposit terbuka sepenuhnya
                print("[*] Menunggu halaman deposit dimuat...")
                await page.wait_for_timeout(5000) 
            else:
                print("[!] Tombol Deposit tidak ditemukan secara otomatis di layar.")
                print("[!] Silakan klik tombol Deposit secara MANUAL di browser sekarang!")
                # Beri waktu 10 detik buat kamu ngeklik manual kalau bot gagal nemu tombolnya
                await page.wait_for_timeout(10000)

            # --- MULAI PEMINDAIAN REGEX ---
            body_text = await page.locator("body").inner_text()
            
            # Trik Tambahan: Kadang bandar nulis nomor pakai spasi (misal: 0812 3456 7890)
            # Kita bersihkan dulu spasinya khusus untuk teks yang mau di-scan
            teks_bersih = body_text.replace(" ", "").replace("-", "")

            print("\n" + "="*40)
            print("🔍 MEMULAI PEMINDAIAN REGEX DI HALAMAN DEPOSIT")
            print("="*40)

            # Regex untuk Nomor HP Indonesia (E-Wallet)
            hp_pattern = r"(?:08|\+?628)\d{7,11}"
            nomor_hp_ditemukan = re.findall(hp_pattern, teks_bersih) # Scan dari teks_bersih

            # Regex untuk Nomor Rekening Bank (10-15 digit angka)
            rek_pattern = r"\b\d{10,15}\b"
            nomor_rek_ditemukan = re.findall(rek_pattern, teks_bersih) # Scan dari teks_bersih

            # Menghapus duplikat
            nomor_hp_ditemukan = list(set(nomor_hp_ditemukan))
            nomor_rek_ditemukan = list(set(nomor_rek_ditemukan))
            
            print(f"[*] Nomor HP / E-Wallet Ditemukan ({len(nomor_hp_ditemukan)}):")
            for hp in nomor_hp_ditemukan:
                print(f"    -> {hp}")

            print(f"[*] Kemungkinan Nomor Rekening Ditemukan ({len(nomor_rek_ditemukan)}):")
            for rek in nomor_rek_ditemukan:
                print(f"    -> {rek}")

            print("="*40 + "\n")

        except Exception as e:
            print(f"\n[!] Yah error bro: {e}")
        
        finally:
            print("[*] Menutup browser...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())