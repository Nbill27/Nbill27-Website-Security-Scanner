🔍 𝗪𝗲𝗯𝘀𝗶𝘁𝗲 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝗦𝗰𝗮𝗻𝗻𝗲𝗿

🚀 Website Security Scanner adalah alat sederhana berbasis Python untuk melakukan scanning keamanan dasar pada website. Alat ini membantu mendeteksi path sensitif, header keamanan, kerentanan XSS/SQLi, SSL/TLS, dan potensi kebocoran email.

🎯 Fitur

✅ Cek Status HTTP → Menampilkan kode status HTTP dan waktu respon.

✅ Analisis SSL/TLS → Mengecek validitas sertifikat SSL dan penerbitnya.

✅ Pemeriksaan Header Keamanan → Memastikan website memiliki header penting seperti CSP, X-Frame-Options, dll.

✅ Deteksi Path Sensitif → Mengecek apakah terdapat folder admin atau file konfigurasi yang bisa diakses publik.

✅ Cek XSS & SQLi Dasar → Melakukan uji coba sederhana untuk melihat apakah website rentan terhadap serangan injeksi.

✅ Deteksi Kebocoran Email → Mencari email yang mungkin bocor pada halaman website.

📥 Cara Instalasi
 Persyaratan:

Python 3.x

Modul Python tambahan: requests, bs4, colorama, whois

🔹 Instalasi Dependensi:
Jalankan perintah berikut untuk menginstal dependensi
pip install -r requirements.txt

🚀 Cara Penggunaan
Gunakan perintah berikut untuk menjalankan scanner: python scanner.py https://example.com

🔍 Memulai scan keamanan untuk: https://example.com

=== HASIL PEMERIKSAAN ===


=== Status HTTP ===

🛡 Status HTTP: 200

⏱ Waktu respon: 0.89s

📡 Server: Apache



=== SSL/TLS ===

🔒 SSL Valid hingga: 2025-01-01

📅 Sisa hari: 300

🏢 Penerbit: Let's Encrypt



=== Header Keamanan ===

🛡 Content-Security-Policy: ❌

🛡 X-Content-Type-Options: ✅

🛡 X-Frame-Options: ✅


=== Path Sensitif ===

⚠️ Ditemukan: https://example.com/admin

⚠️ Ditemukan: https://example.com/.env


=== Kerentanan ===

✅ Tidak ditemukan XSS/SQLi


=== Kebocoran Email ===

✅ Tidak ada email terpapar

💡 Catatan & Disclaimer

⚠️ Gunakan dengan etika dan tanggung jawab! Alat ini hanya untuk tujuan edukasi dan audit keamanan website milik sendiri atau yang memiliki izin eksplorasi keamanan.

🔴 Melakukan scanning tanpa izin dapat melanggar hukum di beberapa negara!

🌟 𝗞𝗼𝗻𝘁𝗿𝗶𝗯𝘂𝘀𝗶

🎯 Jika kamu punya ide atau ingin menambahkan fitur baru, silakan buat Pull Request atau ajukan Issue!
