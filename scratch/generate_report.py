# generate_report.py
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set explicit margins (padding) for a table cell in twentieths of a point (dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()
    
    # 1. Page Margins: standard 4cm left, 3cm top/bottom/right (or 1.5 inches left, 1.18 inches others)
    for section in doc.sections:
        section.top_margin = Inches(1.18) # 3 cm
        section.bottom_margin = Inches(1.18) # 3 cm
        section.left_margin = Inches(1.5) # 4 cm (for binding)
        section.right_margin = Inches(1.18) # 3 cm

    # 2. Base Styles
    # Set default text style to Times New Roman, 12pt, 1.5 line spacing, black text
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Add custom Heading 1, 2, 3 formatting functions
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.italic = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_body(text, bold_prefix=None, indent=0):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if indent > 0:
            p.paragraph_format.left_indent = Inches(indent)
            
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_placeholder(text):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(f"\n[ === {text} === ]\n")
        run.bold = True
        run.italic = True
        run.font.color.rgb = RGBColor(255, 0, 0) # Red color for placeholders
        run.font.size = Pt(11)
        return p

    # ------------------ COVER PAGE ------------------
    cover_p1 = doc.add_paragraph()
    cover_p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p1.paragraph_format.space_before = Pt(36)
    cover_p1.paragraph_format.space_after = Pt(12)
    r1 = cover_p1.add_run("LAPORAN AKHIR PROYEK\n")
    r1.font.size = Pt(14)
    r1.bold = True
    
    cover_p2 = doc.add_paragraph()
    cover_p2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p2.paragraph_format.space_after = Pt(48)
    r2 = cover_p2.add_run("Perancangan Website WarungPudding Sebagai\nMedia Promosi dan Pemesanan Digital UMKM Puding Karakter\ndi Tanjungpinang\n")
    r2.font.size = Pt(14)
    r2.bold = True

    add_placeholder("TEMPEL LOGO UNIVERSITAS MARITIM RAJA ALI HAJI (UMRAH) DISINI")

    cover_p3 = doc.add_paragraph()
    cover_p3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p3.paragraph_format.space_before = Pt(48)
    cover_p3.paragraph_format.space_after = Pt(12)
    r3 = cover_p3.add_run("Disusun oleh:\n")
    r3.font.size = Pt(12)
    r3.bold = True

    # Student info block
    cover_p4 = doc.add_paragraph()
    cover_p4.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p4.paragraph_format.space_after = Pt(48)
    r4 = cover_p4.add_run(
        "1. Rismayanti                   NIM. 2401020041\n"
        "2. Nikita Arzetty Siregar       NIM. 2401020030\n"
        "3. Erlinda Amira Putri S.       NIM. 2401020021\n"
        "4. Dhini Khairunnisa             NIM. 2401020016\n"
    )
    r4.font.size = Pt(12)
    
    cover_p5 = doc.add_paragraph()
    cover_p5.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p5.paragraph_format.space_after = Pt(36)
    r5 = cover_p5.add_run("Dosen Pengampu: Rifaldi Herikson, M.Kom\n")
    r5.font.size = Pt(12)
    r5.bold = True

    cover_p6 = doc.add_paragraph()
    cover_p6.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p6.paragraph_format.space_after = Pt(24)
    r6 = cover_p6.add_run(
        "PROGRAM STUDI TEKNIK INFORMATIKA\n"
        "JURUSAN TEKNIK ELEKTRO DAN INFORMATIKA\n"
        "FAKULTAS TEKNIK DAN TEKNOLOGI KEMARITIMAN\n"
        "UNIVERSITAS MARITIM RAJA ALI HAJI\n"
        "TANJUNGPINANG\n"
        "2026"
    )
    r6.font.size = Pt(12)
    r6.bold = True
    
    doc.add_page_break()

    # ------------------ DAFTAR ISI ------------------
    add_h1("DAFTAR ISI")
    add_body("Halaman")
    add_body("DAFTAR ISI.................................................................................................................... i")
    add_body("DAFTAR GAMBAR............................................................................................................ ii")
    add_body("DAFTAR TABEL............................................................................................................... iii")
    add_body("BAB I PENDAHULUAN.................................................................................................... 1")
    add_body("   1.1 Latar Belakang.......................................................................................................... 1", indent=0.25)
    add_body("   1.2 Tujuan Proyek........................................................................................................... 2", indent=0.25)
    add_body("BAB II HASIL DAN PEMBAHASAN................................................................................... 3")
    add_body("   2.1 Jadwal Proyek dan Pembagian Kerja............................................................................... 3", indent=0.25)
    add_body("   2.2 Deskripsi Proyek................................---------------------------------------------------------- 3", indent=0.25)
    add_body("   2.3 Perancangan Web........................................................................................................... 5", indent=0.25)
    add_body("      2.3.1 Desain Layout Website & Antarmuka........................................................................... 5", indent=0.5)
    add_body("      2.3.2 Alur Navigasi Website............................................................................................ 11", indent=0.5)
    add_body("      2.3.3 Elemen UI (User Interface).................................................................................. 11", indent=0.5)
    add_body("   2.4 Pembuatan Web............................................................................................................. 13", indent=0.25)
    add_body("      2.4.1 Implementasi HTML............................................................................................... 13", indent=0.5)
    add_body("      2.4.2 Implementasi CSS.................................................................................................. 22", indent=0.5)
    add_body("      2.4.3 Implementasi Javascript........................................................................................ 31", indent=0.5)
    add_body("      2.4.4 Hosting dan Deployment Website........................................................................... 35", indent=0.5)
    add_body("BAB III KESIMPULAN DAN SARAN................................................................................... 37")
    add_body("   3.1 Kesimpulan.................................................................................................................. 37", indent=0.25)
    add_body("   3.2 Saran................................------------------------------------------------------------------------------------------ 38", indent=0.25)
    add_body("BAB IV DAFTAR PUSTAKA.................................................................................................. 39")
    
    doc.add_page_break()

    # ------------------ DAFTAR GAMBAR ------------------
    add_h1("DAFTAR GAMBAR")
    
    figures = [
        "Gambar 1. Desain Prototipe Figma - Halaman Katalog Produk",
        "Gambar 2. Screenshot Tampilan Live Web - Halaman Beranda (Homepage)",
        "Gambar 3. Screenshot Tampilan Live Web - Section Kisah Kami (Spot Card & Collage)",
        "Gambar 4. Screenshot Tampilan Live Web - Halaman Katalog Menu",
        "Gambar 5. Screenshot Tampilan Live Web - Halaman Detail Menu",
        "Gambar 6. Screenshot Tampilan Live Web - Halaman Keranjang Belanja",
        "Gambar 7. Screenshot Tampilan Live Web - Halaman Formulir Checkout",
        "Gambar 8. Screenshot Tampilan Live Web - Halaman Lacak Pesanan",
        "Gambar 9. Screenshot Tampilan Live Web - Halaman Admin Dashboard",
        "Gambar 10. Hasil Implementasi HTML Struktur Dasar (File: index.html - Baris 1-12)",
        "Gambar 11. Hasil Implementasi HTML Navbar (File: index.html - Baris 13-43)",
        "Gambar 12. Tampilan Hasil Implementasi Navbar di Browser (File: index.html)",
        "Gambar 13. Hasil Implementasi HTML Hero Section (File: index.html - Baris 44-63)",
        "Gambar 14. Tampilan Hasil Implementasi Hero Section di Browser (File: index.html)",
        "Gambar 15. Hasil Implementasi HTML Section Kisah Kami (File: index.html - Baris 74-120)",
        "Gambar 16. Tampilan Hasil Implementasi Section Kisah Kami (File: index.html)",
        "Gambar 17. Hasil Implementasi HTML Katalog Produk (File: produk.html - Baris 74-82 & Dynamic render)",
        "Gambar 18. Tampilan Hasil Implementasi Katalog Produk di Browser (File: produk.html)",
        "Gambar 19. Hasil Implementasi HTML Detail Produk (File: detail.html - Kerangka Kontrol Kuantitas)",
        "Gambar 20. Tampilan Hasil Implementasi Detail Produk di Browser (File: detail.html)",
        "Gambar 21. Hasil Implementasi HTML Keranjang Belanja (File: keranjang.html - Tabel Transaksi)",
        "Gambar 22. Tampilan Hasil Implementasi Keranjang Belanja (File: keranjang.html)",
        "Gambar 23. Hasil Implementasi HTML Form Checkout (File: checkout.html - Data Input Kurir)",
        "Gambar 24. Tampilan Hasil Implementasi Form Checkout di Browser (File: checkout.html)",
        "Gambar 25. Hasil Implementasi HTML Lacak Pesanan (File: lacak.html - Card Tracking Status)",
        "Gambar 26. Tampilan Hasil Implementasi Lacak Pesanan di Browser (File: lacak.html)",
        "Gambar 27. Hasil Implementasi HTML Dashboard Admin (File: admin/dashboard.html - Struktur Statistik)",
        "Gambar 28. Tampilan Hasil Implementasi Dashboard Admin di Browser (File: admin/dashboard.html)",
        "Gambar 29. Hasil Implementasi CSS Variabel & Root Styles (File: css/style.css - Baris 1-31)",
        "Gambar 30. Hasil Implementasi CSS Custom Card Sizing & Shadows (File: css/style.css - Baris 278-291)",
        "Gambar 31. Hasil Implementasi CSS Button & Shadow Styles (File: css/style.css - Baris 244-276)",
        "Gambar 32. Hasil Implementasi CSS Hero Image & Inner Frame (File: css/style.css - Baris 640-669)",
        "Gambar 33. Hasil Implementasi CSS Kisah Kami Collage & Card (File: css/style.css - Baris 1576-1631)",
        "Gambar 34. Hasil Implementasi CSS Responsive Media Queries (File: css/responsive.css & css/style.css)",
        "Gambar 35. Tampilan Responsif Pada Perangkat Mobile (Smartphone Viewport)",
        "Gambar 36. Hasil Implementasi Javascript LocalStorage Products & Cart Handler (File: js/cart.js & js/main.js)",
        "Gambar 37. Hasil Implementasi Javascript Cart Actions (File: js/cart.js - Update Qty & Delete)",
        "Gambar 38. Hasil Implementasi Javascript Checkout Validation (File: js/cart.js - Order ID Generator)",
        "Gambar 39. Hasil Implementasi Javascript Order Tracking Logic (File: js/main.js & lacak inline script)",
        "Gambar 40. Hasil Implementasi Javascript Navigation Toggle & Scroll Effect (File: js/main.js)",
        "Gambar 41. Konfigurasi Deployment & Hosting Netlify",
        "Gambar 42. Hasil Implementasi Javascript Konfigurasi Firebase (File: js/firebase-config.js)",
        "Gambar 43. Hasil Implementasi Javascript Real-time Sync (File: js/firebase-sync.js)"
    ]
    
    for fig in figures:
        add_body(fig)

    doc.add_page_break()

    # ------------------ DAFTAR TABEL ------------------
    add_h1("DAFTAR TABEL")
    add_body("Table 1. Tabel Jadwal Kegiatan Proyek............................................................................ 3")
    add_body("Table 2. Tabel Pembagian Kerja Anggota Kelompok............................................................. 3")
    
    doc.add_page_break()

    # ================== BAB I PENDAHULUAN ==================
    add_h1("BAB I\nPENDAHULUAN")
    
    add_h2("1.1 Latar Belakang")
    
    add_body(
        "Perkembangan teknologi informasi saat ini mengalami kemajuan yang sangat pesat, terutama dalam "
        "pemanfaatan jaringan internet dan website. Di era digital saat ini, website telah menjadi salah satu media "
        "utama dalam penyampaian informasi, sarana promosi, serta interaksi transaksi langsung antara produsen dan "
        "konsumen. Melalui media website, informasi produk dapat diakses kapan saja dan dari mana saja tanpa batasan "
        "geografis maupun waktu. Oleh karena itu, digitalisasi menjadi langkah krusial untuk meningkatkan daya saing "
        "dan penguatan branding dari suatu unit usaha, khususnya Usaha Mikro, Kecil, dan Menengah (UMKM)."
    )
    
    add_body(
        "Seiring dengan tren digitalisasi tersebut, banyak sektor usaha kuliner yang mulai melirik teknologi web "
        "untuk meningkatkan produktivitas penjualan mereka. Salah satu UMKM kuliner lokal di Tanjungpinang yang "
        "memiliki potensi besar untuk dikembangkan secara digital adalah WarungPudding. WarungPudding menyajikan produk "
        "puding jelly karakter unik, lucu, dan sehat. Produk puding karakter yang ditawarkan sangat digemari oleh anak-anak "
        "maupun orang dewasa untuk keperluan konsumsi harian, hadiah ulang tahun, pesta anak, atau hantaran acara spesial. "
        "Dengan bahan 100% serat alami rumput laut, gula rendah kalori, serta pewarna higienis bersertifikasi food-grade, "
        "WarungPudding memiliki keunggulan kompetitif yang kuat di pasar lokal."
    )
    
    add_body(
        "Namun, saat ini operasional promosi dan pemesanan pada WarungPudding masih memiliki keterbatasan yang cukup "
        "signifikan. Promosi dan pemesanan saat ini masih mengandalkan media sosial konvensional seperti Instagram dan "
        "WhatsApp pribadi. Metode ini memiliki berbagai kelemahan, di antaranya adalah tidak terstrukturnya katalog produk, "
        "potensi kesalahan pencatatan pesanan yang tinggi, sulitnya memantau ketersediaan stok produk secara real-time, "
        "serta ketidakmampuan pelanggan untuk melacak status pengerjaan puding secara mandiri. Selain itu, manajemen "
        "internal untuk mencatat laporan pesanan masuk, mengelola daftar stok bahan baku, dan menyusun laporan keuangan harian "
        "masih dicatat secara manual menggunakan kertas atau spreadsheet sederhana, yang rentan terhadap kehilangan data."
    )
    
    add_body(
        "Berdasarkan permasalahan di atas, dirancanglah sebuah aplikasi web e-commerce terintegrasi khusus untuk "
        "WarungPudding. Website ini dikembangkan dengan konsep desain modern, estetik, dan premium yang menyelaraskan warna-warna "
        "pastel (soft pink dan lavender) khas produk puding karakter yang ramah anak dan kekinian. Sistem ini tidak hanya "
        "menjadi media informasi dan promosi visual yang menarik bagi pelanggan, namun juga dilengkapi sistem pemesanan online, "
        "keranjang belanja dinamis, validasi checkout transaksi, pelacakan nomor pesanan (order tracking), serta sistem admin "
        "dashboard yang komprehensif untuk memudahkan pengelolaan internal UMKM."
    )

    add_h2("1.2 Tujuan Proyek")
    add_body("Adapun tujuan dari pelaksanaan proyek perancangan website WarungPudding ini adalah:")
    add_body("1. Membangun platform website e-commerce yang interaktif, menarik, dan responsif sebagai media promosi digital produk puding karakter lokal Tanjungpinang.", indent=0.25)
    add_body("2. Menyediakan katalog menu online yang dinamis lengkap dengan deskripsi, kategori rasa (Coklat, Strawberry, Matcha, Vanilla, Dinosaurus, Kelinci), harga, dan status ketersediaan stok secara real-time.", indent=0.25)
    add_body("3. Mengimplementasikan sistem keranjang belanja (shopping cart) dan formulir checkout terintegrasi untuk mempercepat dan mempermudah proses pemesanan bagi pelanggan.", indent=0.25)
    add_body("4. Membangun fitur pelacakan pesanan (order tracking) yang memungkinkan pelanggan mengetahui tahapan produksi pesanan mereka (Diproses, Siap, Selesai) secara mandiri.", indent=0.25)
    add_body("5. Mengembangkan dashboard administrasi internal yang memudahkan admin dan karyawan mengelola data produk, memantau riwayat pesanan masuk, memperbarui stok produk, dan memantau laporan pendapatan penjualan.", indent=0.25)
    
    doc.add_page_break()

    # ================== BAB II HASIL DAN PEMBAHASAN ==================
    add_h1("BAB II\nHASIL DAN PEMBAHASAN")
    
    add_h2("2.1 Jadwal Proyek dan Pembagian Kerja")
    add_body(
        "Proyek pengembangan website WarungPudding dilaksanakan selama kurun waktu tiga bulan, dimulai dari tahapan "
        "pengumpulan data, analisis kebutuhan, perancangan antarmuka figma, penulisan kode program (coding), pengujian sistem "
        "hingga hosting/deployment ke server publik. Berikut adalah jadwal detail pelaksanaan kegiatan proyek:"
    )

    # Table 1: Project Schedule
    table1 = doc.add_table(rows=6, cols=13)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.style = 'Table Grid'
    
    headers1 = ['Kegiatan', 'April W1', 'W2', 'W3', 'W4', 'Mei W1', 'W2', 'W3', 'W4', 'Juni W1', 'W2', 'W3', 'W4']
    for i, h in enumerate(headers1):
        cell = table1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_margins(cell)

    activities = [
        ("Mengumpulkan Informasi & Data UMKM", [True, True, False, False, False, False, False, False, False, False, False, False]),
        ("Merancang Desain UI/UX (Figma)", [False, True, True, True, False, False, False, False, False, False, False, False]),
        ("Pembuatan Kode Program (HTML/CSS)", [False, False, False, True, True, True, True, False, False, False, False, False]),
        ("Implementasi Database & JS Logic", [False, False, False, False, False, True, True, True, True, False, False, False]),
        ("Pengujian Sistem & Deployment", [False, False, False, False, False, False, False, False, True, True, True, True])
    ]
    
    for row_idx, (act, schedule) in enumerate(activities, start=1):
        table1.cell(row_idx, 0).text = act
        set_cell_margins(table1.cell(row_idx, 0))
        for col_idx, active in enumerate(schedule, start=1):
            cell = table1.cell(row_idx, col_idx)
            cell.text = "■" if active else ""
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)

    add_body("\nBerikut adalah pembagian tugas dan kerja dari masing-masing anggota kelompok dalam pengembangan proyek website ini:")

    # Table 2: Team Work Division
    table2 = doc.add_table(rows=5, cols=4)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.style = 'Table Grid'
    
    headers2 = ['No', 'Nama Anggota', 'Posisi Tim', 'Deskripsi Kerja / Tanggung Jawab']
    for i, h in enumerate(headers2):
        cell = table2.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_margins(cell)

    team = [
        ("1", "Rismayanti", "Ketua Kelompok / Developer", "Mengkoordinasi tim, mengembangkan implementasi struktur HTML, penulisan script JavaScript, interaksi keranjang belanja, dashboard admin, dan hosting."),
        ("2", "Nikita Arzetty Siregar", "UI/UX Designer", "Merancang layout antarmuka (wireframing) di Figma, menyiapkan aset grafis gambar puding, memilih skema warna pastel, dan menyusun tipografi."),
        ("3", "Erlinda Amira Putri Sudarmono", "Frontend Designer", "Menerjemahkan rancangan Figma ke dalam stylesheet CSS, membangun layout responsif dengan Flexbox & Grid, mengoptimalkan animasi visual."),
        ("4", "Dhini Khairunnisa", "Technical Writer / QA", "Menyusun dokumentasi teknis, melakukan pengujian fungsionalitas tombol, validasi formulir input, dan menulis laporan akhir proyek.")
    ]
    
    for row_idx, t in enumerate(team, start=1):
        for col_idx, text in enumerate(t):
            cell = table2.cell(row_idx, col_idx)
            cell.text = text
            if col_idx < 3:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)

    add_h2("2.2 Deskripsi Proyek")
    add_body(
        "Website WarungPudding dirancang sebagai solusi promosi, e-commerce, dan manajemen digital yang "
        "komprehensif untuk memfasilitasi kebutuhan operasional internal UMKM dan layanan pelanggan secara online. "
        "Desain antarmuka website disesuaikan dengan identitas brand puding karakter yang dinamis, bersih, dan premium. "
        "Website ini menggunakan skema warna pastel harmonis yang didominasi oleh warna lavender lembut (#E6CCFF) "
        "dan pink lembut (#FFB6C1), dipadukan dengan tipografi modern yang berkelas."
    )

    add_body("Website WarungPudding terbagi menjadi dua bagian utama, yaitu Halaman Pelanggan (Customer Area) dan Halaman Pengelola (Admin Dashboard Area):")
    add_body("1. Halaman Pelanggan (Customer Area):", indent=0.25)
    add_body("a. Halaman Beranda (Homepage): Menampilkan logo brand, menu navigasi mengambang (glassmorphism), banner hero berisi slogan utama dengan dekorasi teks stiker 'Kekinian!', galeri gambar puding karakter unggulan yang atraktif, panel keunggulan produk (Kisah Kami), petunjuk alur pemesanan produk, dan widget kontak media sosial terintegrasi.", indent=0.5)
    add_body("b. Halaman Katalog Produk: Menyediakan antarmuka pencarian cepat (live search) dan filter kategori rasa atau jenis karakter puding secara instan tanpa perlu memuat ulang halaman (SPA feel). Setiap kartu menu menampilkan badge status stok.", indent=0.5)
    add_body("c. Halaman Detail Produk: Menyediakan informasi terperinci mengenai komposisi puding, harga, stok aktif, kontrol kuantitas jumlah pesanan, dan tombol interaktif tambah ke keranjang.", indent=0.5)
    add_body("d. Halaman Keranjang Belanja: Menampilkan tabel daftar pesanan puding yang telah ditambahkan oleh pelanggan, mendukung pembaruan kuantitas produk secara dinamis, dan kalkulasi subtotal harga pesanan.", indent=0.5)
    add_body("e. Halaman Checkout: Menyediakan formulir pengisian data pelanggan (nama, alamat lengkap, nomor WhatsApp aktif) dan opsi pengiriman (ambil di stand bazar GANET atau dikirim via kurir lokal) sebelum pesanan diproses.", indent=0.5)
    add_body("f. Halaman Lacak Pesanan: Memungkinkan pelanggan memasukkan Kode Pesanan (Order ID) unik mereka untuk memantau status pesanan (Diproses, Siap, Selesai) secara real-time.", indent=0.5)
    add_body("g. Halaman Login: Pintu gerbang login berproteksi validasi untuk pengelola stand bazar masuk ke sistem dashboard.", indent=0.5)

    add_body("2. Halaman Pengelola (Admin Dashboard Area):", indent=0.25)
    add_body("a. Dashboard Utama: Menampilkan ringkasan statistik (total transaksi, total pendapatan penjualan rupiah, jumlah jenis menu puding aktif, dan jumlah pesanan yang sedang diproses).", indent=0.5)
    add_body("b. Halaman Kelola Produk (Admin): Menyediakan formulir CRUD (Create, Read, Update, Delete) data menu puding, mengunggah foto puding baru, memperbarui deskripsi rasa, mengubah kategori, mengubah harga, dan menyetel jumlah stok.", indent=0.5)
    add_body("c. Halaman Kelola Pesanan (Karyawan Stand): Panel bagi karyawan stand bazar GANET untuk melihat daftar pesanan masuk, memvalidasi alamat pengiriman, dan memperbarui status pesanan dari 'Diproses' menjadi 'Siap Kirim/Ambil' dan 'Selesai' setelah transaksi tuntas.", indent=0.5)
    add_body("d. Halaman Kelola Stok: Mempermudah pembaruan stok puding harian secara cepat.", indent=0.5)

    add_h2("2.3 Perancangan Web")
    
    add_h3("2.3.1 Desain Layout Website & Antarmuka")
    add_body(
        "Perancangan tata letak layout website WarungPudding dilakukan menggunakan wireframing dan prototyping "
        "di Figma. Sesuai dengan batasan perancangan, tahapan desain prototipe Figma difokuskan secara khusus "
        "untuk merancang halaman inti yaitu Halaman Katalog Produk (Product Grid). Sedangkan halaman penunjang "
        "lainnya dirancang secara langsung menggunakan browser (rapid web prototyping) dengan mengacu pada panduan "
        "gaya pastel yang telah disepakati. Berikut adalah tampilan desain katalog produk di Figma beserta "
        "screenshot tangkapan layar (screenshot) tampilan antarmuka web yang diakses secara langsung (live web):"
    )
    
    add_placeholder("TEMPEL SCREENSHOT DESAIN PROTOTIPE FIGMA - HALAMAN KATALOG PRODUK")
    add_body("Gambar 1. Desain Prototipe Figma - Halaman Katalog Produk", indent=0.25)
    
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - HALAMAN BERANDA (HOMEPAGE)")
    add_body("Gambar 2. Screenshot Tampilan Live Web - Halaman Beranda (Homepage)", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - SECTION KISAH KAMI (SPOT CARD & COLLAGE)")
    add_body("Gambar 3. Screenshot Tampilan Live Web - Section Kisah Kami", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - HALAMAN KATALOG MENU")
    add_body("Gambar 4. Screenshot Tampilan Live Web - Halaman Katalog Menu", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - HALAMAN DETAIL MENU")
    add_body("Gambar 5. Screenshot Tampilan Live Web - Halaman Detail Menu", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - HALAMAN KERANJANG BELANJA")
    add_body("Gambar 6. Screenshot Tampilan Live Web - Halaman Keranjang Belanja", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - HALAMAN FORMULIR CHECKOUT")
    add_body("Gambar 7. Screenshot Tampilan Live Web - Halaman Formulir Checkout", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - HALAMAN LACAK PESANAN")
    add_body("Gambar 8. Screenshot Tampilan Live Web - Halaman Lacak Pesanan", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LIVE WEB - HALAMAN ADMIN DASHBOARD")
    add_body("Gambar 9. Screenshot Tampilan Live Web - Halaman Admin Dashboard", indent=0.25)

    add_h3("2.3.2 Alur Navigasi Website")
    add_body(
        "Alur navigasi website dirancang agar meminimalkan friksi bagi pelanggan saat melakukan transaksi. "
        "Pelanggan dapat menjelajahi halaman web dengan mudah melalui navbar menu. Berikut adalah skema alurnya:"
    )
    add_body("- Beranda (Home): Halaman awal promosi, pengenalan brand, dan panduan alur order.", indent=0.25)
    add_body("- Produk (Katalog): Pelanggan mencari puding karakter, menyaring berdasarkan kategori, lalu masuk ke detail produk.", indent=0.25)
    add_body("- Detail Produk: Menentukan kuantitas pesanan, lalu klik 'Tambah Ke Keranjang'.", indent=0.25)
    add_body("- Keranjang Belanja: Menampilkan tabel rincian pesanan. Pelanggan dapat meninjau belanjaan mereka, kemudian klik 'Lanjutkan Checkout'.", indent=0.25)
    add_body("- Checkout: Pelanggan mengisi data pengiriman lengkap. Saat tombol 'Buat Pesanan' diklik, sistem mengosongkan keranjang, menghasilkan Order ID acak, menyimpan data transaksi ke LocalStorage, dan menampilkan nota pesanan.", indent=0.25)
    add_body("- Lacak Pesanan: Pelanggan menyalin Order ID mereka dan menempelkannya di input lacak pesanan untuk memantau pengerjaan oleh admin stand.", indent=0.25)

    add_h3("2.3.3 Elemen UI (User Interface)")
    add_body("Desain elemen antarmuka website WarungPudding dikembangkan dengan panduan gaya (style guide) berikut:")
    add_body("1. Warna Utama (Brand Colors):", indent=0.25)
    add_body("a. Pink Soft (#FFB6C1) & Pink Gradient: Digunakan sebagai warna latar belakang primer elemen interaktif, tombol utama, serta logo utama.", indent=0.5)
    add_body("b. Lavender (#E6CCFF) & Lavender Gradient: Digunakan sebagai warna sekunder pada tombol pilihan, latar belakang badge mengambang, serta warna bayangan.", indent=0.5)
    add_body("c. Purple Accent (#9B59B6) & Purple Dark (#6C3483): Digunakan untuk memberikan penegasan warna pada teks judul (headings), tautan aktif, dan tombol penutup.", indent=0.5)
    add_body("d. Background Light (#FAFAFC): Latar belakang utama halaman web yang dipadukan dengan efek radial gradient warna pastel agar nyaman dipandang mata.", indent=0.5)
    
    add_body("2. Tipografi (Typography):", indent=0.25)
    add_body("a. Font Judul (Headings): Menggunakan font Google 'Outfit' sans-serif dengan ketebalan 800 (Extra Bold) untuk memberikan kesan modern, tegas, namun elegan.", indent=0.5)
    add_body("b. Font Isi Konten (Body Text): Menggunakan font 'Plus Jakarta Sans' dengan ketebalan 400 (Regular) dan 500 (Medium) untuk menjamin tingkat keterbacaan yang tinggi.", indent=0.5)

    add_body("3. Gaya Tombol & Kartu (Card & Button Styles):", indent=0.25)
    add_body("a. Border & Shadows: Menghindari warna solid hitam pekat, melainkan menggunakan warna pastel lavender ungu tua (#D1A3FF) setebal 2px untuk border, dan offset shadow 8px 8px warna lavender muda (#E6CCFF) untuk memberikan kesan 3D neo-brutalist yang lembut.", indent=0.5)
    add_body("b. Border-Radius: Menggunakan rounded corners (border-radius: 20px) pada semua kartu produk dan panel kisah kami agar selaras dengan citra produk puding karakter yang menggemaskan.", indent=0.5)

    add_h2("2.4 Pembuatan Web")
    
    add_h3("2.4.1 Implementasi HTML")
    add_body(
        "Implementasi HTML (HyperText Markup Language) berfungsi sebagai pondasi penataan kerangka dasar website. "
        "Berikut ini dijabarkan modul-modul file HTML beserta potongan kodenya yang telah diimplementasikan:"
    )

    # We list code modules specifically with file paths and descriptions
    add_body("1. Modul Struktur Dasar & Meta Tags (File: index.html - Baris 1 s/d 12)", bold_prefix="a. ")
    add_body("Mengatur metadata SEO, viewport responsive, tautan CSS Google Fonts, FontAwesome, dan stylesheets.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML STRUKTUR DASAR (index.html: 1-12)")
    
    add_body("2. Modul Navigasi Utama (File: index.html - Baris 13 s/d 43)", bold_prefix="b. ")
    add_body("Menyediakan menu navigasi mengambang (Navbar) responsif yang memuat tautan halaman Beranda, Katalog Produk, Lacak Pesanan, Keranjang Belanja, dan tombol Login.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML NAVBAR (index.html: 13-43)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN NAVBAR DI BROWSER")

    add_body("3. Modul Banner Utama / Hero Section (File: index.html - Baris 44 s/d 63)", bold_prefix="c. ")
    add_body("Menampilkan slogan utama 'Puding Karakter Lucu, Enak & Kekinian!' dengan stiker, tombol ajakan bertindak (CTA), serta wadah gambar utama (.hero-image) dan badge harga/lokasi.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML HERO SECTION (index.html: 44-63)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN HERO SECTION DI BROWSER")

    add_body("4. Modul Kisah Kami / About Us (File: index.html - Baris 74 s/d 120)", bold_prefix="d. ")
    add_body("Menyusun profil singkat WarungPudding di stand bazar GANET, collage dua gambar kelinci & dino pink, serta tiga buah mini card statistik penjualan (10+ Varian, 100% Alami, 4.9 Rating).", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML SECTION KISAH KAMI (index.html: 74-120)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN SECTION KISAH KAMI DI BROWSER")

    add_body("5. Modul Katalog Grid Dinamis (File: produk.html - Baris 74 s/d 82 & Render Script)", bold_prefix="e. ")
    add_body("Menyediakan container grid kosong (#productContainer) yang akan diinjeksi daftar kartu puding secara dinamis oleh JavaScript, dilengkapi dengan search input dan tombol filter kategori.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML KATALOG PRODUK (produk.html: 74-82)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN KATALOG PRODUK DI BROWSER")

    add_body("6. Modul Detail Produk (File: detail.html)", bold_prefix="f. ")
    add_body("Halaman untuk menampilkan nama produk, harga, deskripsi, status stok, input kuantitas pesanan, serta tombol tambah ke keranjang.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML DETAIL PRODUK (detail.html)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN DETAIL PRODUK DI BROWSER")

    add_body("7. Modul Keranjang Belanja (File: keranjang.html)", bold_prefix="g. ")
    add_body("Struktur tabel rincian item belanjaan, kuantitas order, tombol edit/hapus, serta ringkasan total biaya pesanan.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML KERANJANG BELANJA (keranjang.html)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN KERANJANG BELANJA DI BROWSER")

    add_body("8. Modul Formulir Checkout (File: checkout.html)", bold_prefix="h. ")
    add_body("Menampung formulir input data pemesan (nama, alamat, WhatsApp) dan metode pengiriman stand/kurir.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML FORM CHECKOUT (checkout.html)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN FORM CHECKOUT DI BROWSER")

    add_body("9. Modul Lacak Status Pesanan (File: lacak.html)", bold_prefix="i. ")
    add_body("Menyediakan input Kode Pesanan (Order ID) dan wadah visual untuk menampilkan diagram status pengerjaan puding (Diproses, Siap, Selesai).", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML LACAK PESANAN (lacak.html)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN LACAK PESANAN DI BROWSER")

    add_body("10. Modul Dashboard Admin (File: admin/dashboard.html)", bold_prefix="j. ")
    add_body("Menampilkan antarmuka manajemen internal seperti statistik penjualan, kelola produk, update stok puding, dan pelaporan keuangan stand.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE HTML DASHBOARD ADMIN (admin/dashboard.html)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN DASHBOARD ADMIN DI BROWSER")

    add_h3("2.4.2 Implementasi CSS")
    add_body(
        "Penulisan stylesheet CSS (Cascading Style Sheets) menggunakan file css/style.css sebagai pengatur utama "
        "estetika layout, tipografi, warna pastel, penyesuaian efek shadow 3D neo-brutalist lembut, dan animasi. "
        "File css/responsive.css khusus menangani tata letak adaptif (media queries) pada gadget."
    )

    add_body("1. Modul Root Styles & CSS Variables (File: css/style.css - Baris 1 s/d 31)", bold_prefix="a. ")
    add_body("Mendefinisikan variabel warna pastel (--pink-soft, --lavender, --purple-accent) serta font heading (Outfit) dan body (Plus Jakarta Sans).", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE CSS ROOT (css/style.css: 1-31)")

    add_body("2. Modul Custom Card Sizing & Shadows (File: css/style.css - Baris 278 s/d 291)", bold_prefix="b. ")
    add_body("Mendefinisikan gaya kartu membulat (border-radius: 20px) dengan ketebalan border 2px solid pastel (#D1A3FF) dan bayangan offset soft lavender (#E6CCFF).", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE CSS CARD STYLES (css/style.css: 278-291)")

    add_body("3. Modul Button Styles (File: css/style.css - Baris 244 s/d 276)", bold_prefix="c. ")
    add_body("Mengatur gaya tombol utama (.btn-primary), tombol sekunder (.btn-secondary), dan outline (.btn-outline) menggunakan bayangan offset pastel dinamis.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE CSS BUTTON STYLES (css/style.css: 244-276)")

    add_body("4. Modul Hero Image Inner Frame (File: css/style.css - Baris 640 s/d 669)", bold_prefix="d. ")
    add_body("Mengatur container gambar hero (.hero-image) dan sub-container overflow clip (.hero-image-inner) agar gambar puding dino terpotong rapi dalam sudut border-radius tanpa memotong badge melayang.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE CSS HERO IMAGE FRAME (css/style.css: 640-669)")

    add_body("5. Modul Kisah Kami Collage & Card (File: css/style.css - Baris 1576 s/d 1631)", bold_prefix="e. ")
    add_body("Mendefinisikan tata letak collage tumpang tindih untuk dua gambar (.collage-img-main dan .collage-img-sub) serta wadah kaca spot card (.about-card).", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE CSS KISAH KAMI (css/style.css: 1576-1631)")

    add_body("6. Modul Responsive CSS Media Queries (File: css/responsive.css & css/style.css)", bold_prefix="f. ")
    add_body("Berisi query max-width: 1024px, 768px, dan 480px untuk menyesuaikan grid menjadi 2 kolom atau 1 kolom, mengecilkan ukuran padding card, serta menumpuk stats list secara vertikal di layar smartphone.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE CSS RESPONSIVE (css/responsive.css)")
    add_placeholder("TEMPEL SCREENSHOT TAMPILAN MOBILE WEB")

    add_h3("2.4.3 Implementasi Javascript")
    add_body(
        "Bahasa pemrograman JavaScript (JS) digunakan untuk menggerakkan seluruh logika interaktif pada website "
        "secara client-side. Sistem database menggunakan Firebase Realtime Database sebagai penyimpanan terpusat "
        "di cloud, dikombinasikan dengan sinkronisasi hibrida LocalStorage API agar data produk dan pesanan tetap dapat "
        "diakses dengan cepat dan disinkronkan secara instan lintas-perangkat."
    )

    add_body("1. Modul Inisialisasi Produk & Tambah Keranjang (File: js/cart.js & js/main.js)", bold_prefix="a. ")
    add_body("Membuat database produk lokal di LocalStorage (jika belum ada) dan menyediakan fungsi global addToCart(id) untuk menambahkan produk puding karakter ke data array keranjang belanja.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE JS LOCALSTORAGE PRODUCTS (js/cart.js)")

    add_body("2. Modul Manajemen Keranjang Belanja (File: js/cart.js)", bold_prefix="b. ")
    add_body("Mengatur fungsi renderCart() untuk menulis tabel barang di keranjang, fungsi updateQuantity() untuk menambah/mengurangi jumlah puding, dan fungsi deleteItem() untuk menghapus item.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE JS CART ACTIONS (js/cart.js)")

    add_body("3. Modul Validasi Form Checkout & Order Generator (File: js/cart.js)", bold_prefix="c. ")
    add_body("Memvalidasi formulir nama, alamat, nomor WhatsApp, memproses data keranjang belanja, menghasilkan Order ID acak (misal WP-76495), menyimpan transaksi ke LocalStorage 'orders', serta mengunggah data pesanan ke Firebase cloud.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE JS CHECKOUT & ORDER ID (js/cart.js)")

    add_body("4. Modul Pelacakan Pesanan Real-Time (File: lacak.html & js/main.js)", bold_prefix="d. ")
    add_body("Mencari data pesanan di LocalStorage berdasarkan Order ID yang dimasukkan pelanggan, membandingkan status pesanan aktif (Diproses, Siap, Selesai), dan memperbarui bagan alur status secara visual.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE JS ORDER TRACKING (lacak.html)")

    add_body("5. Modul Interaksi Navbar & Burger Menu (File: js/main.js)", bold_prefix="e. ")
    add_body("Mengatur efek transparansi navbar blur saat digulir (window.scrollY > 50) serta mengontrol buka-tutup slide menu navigasi mobile pada layar smartphone.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE JS NAVBAR ACTIONS (js/main.js)")

    add_body("6. Modul Konfigurasi Firebase (File: js/firebase-config.js)", bold_prefix="f. ")
    add_body("Mengatur konfigurasi kredensial API key Firebase Realtime Database dan menginisialisasi modul database secara terpusat.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE JS KONFIGURASI FIREBASE (js/firebase-config.js)")

    add_body("7. Modul Sinkronisasi Hibrida Real-Time (File: js/firebase-sync.js)", bold_prefix="g. ")
    add_body("Mendengarkan data produk dan pesanan dari database cloud Firebase dan secara real-time menyinkronkannya ke LocalStorage lokal serta mengirim event kustom untuk me-render ulang antarmuka tanpa reload.", indent=0.25)
    add_placeholder("TEMPEL SCREENSHOT KODE JS SINKRONISASI FIREBASE (js/firebase-sync.js)")

    add_h3("2.4.4 Hosting dan Deployment Website")
    add_body(
        "Setelah tahapan pengujian frontend dan validasi fungsionalitas tombol tuntas, seluruh kode file project web "
        "diunggah ke platform hosting static web Netlify. Deployment diatur otomatis menggunakan repositori GitHub. "
        "Website WarungPudding berhasil online dan dapat diakses publik melalui tautan server:"
    )
    add_body("URL Akses Website: https://warungpudding.netlify.app/ (Simulasi)", indent=0.25)

    add_placeholder("TEMPEL SCREENSHOT PANEL NETLIFY DEPLOYMENT SUCCESS")
    add_body("Gambar 41. Konfigurasi Deployment & Hosting Netlify", indent=0.25)

    doc.add_page_break()

    # ================== BAB III KESIMPULAN DAN SARAN ==================
    add_h1("BAB III\nKESIMPULAN DAN SARAN")
    
    add_h2("3.1 Kesimpulan")
    add_body(
        "Berdasarkan tahapan analisis, perancangan antarmuka figma, penulisan kode program (HTML, CSS, JS), "
        "pengujian, hingga tahapan hosting, maka dapat ditarik beberapa kesimpulan penting sebagai berikut:"
    )
    add_body(
        "1. Proyek perancangan website WarungPudding berhasil diselesaikan dan dideploy secara publik sebagai media "
        "promosi kuliner lokal puding karakter di Tanjungpinang yang estetik, modern, dan bernilai premium.",
        indent=0.25
    )
    add_body(
        "2. Skema desain visual bernuansa pastel lembut (soft pink dan lavender) dengan implementasi gaya kartu dan tombol "
        "neo-brutalist berbayangan offset yang halus (tanpa warna hitam pekat) berhasil mewujudkan kesan ramah anak, bersih, "
        "higienis, dan premium pada seluruh halaman web.",
        indent=0.25
    )
    add_body(
        "3. Sistem belanja online berbasis integrasi real-time database Firebase Realtime Database terbukti mampu memfasilitasi "
        "kebutuhan e-commerce WarungPudding secara aman, persisten, dan sinkron lintas-perangkat secara otomatis.",
        indent=0.25
    )
    add_body(
        "4. Layanan pelacakan pesanan (order tracking) yang interaktif mempermudah komunikasi pelanggan dengan stand "
        "bazar GANET, sehingga pelanggan dapat mengetahui status kesiapan pengerjaan puding secara mandiri.",
        indent=0.25
    )
    add_body(
        "5. Panel admin dashboard internal mempermudah pengelola stand bazar GANET dalam manajemen produk CRUD, memperbarui stok "
        "puding harian secara cepat, dan memantau rincian grafik laporan pendapatan UMKM secara sistematis.",
        indent=0.25
    )

    add_h2("3.2 Saran")
    add_body("Untuk pengembangan aplikasi website WarungPudding yang lebih optimal di masa mendatang, disarankan beberapa hal berikut:")
    add_body(
        "1. Integrasi Sistem Otentikasi Pengguna (Firebase Auth): Mengembangkan sistem otentikasi login admin dan karyawan "
        "menggunakan layanan Firebase Authentication guna menjamin keamanan hak akses akun pengelola secara terstandar.",
        indent=0.25
    )
    add_body(
        "2. Integrasi WhatsApp API Gateway: Mengintegrasikan notifikasi pesanan otomatis langsung ke nomor WhatsApp pelanggan saat "
        "status pesanan diubah oleh karyawan stand bazar GANET, guna meningkatkan kenyamanan pelanggan.",
        indent=0.25
    )
    add_body(
        "3. Payment Gateway Integration: Menambahkan opsi pembayaran non-tunai (cashless) secara otomatis menggunakan gerbang pembayaran "
        "lokal (seperti Midtrans atau Xendit) yang mendukung pembayaran instan via e-wallet (GoPay, OVO, ShopeePay) dan QRIS.",
        indent=0.25
    )
    add_body(
        "4. Peta Geolocation Lokasi Stand: Mengintegrasikan API Google Maps secara langsung di halaman kontak untuk mempermudah "
        "pelanggan mencari koordinat rute jalan menuju stand bazar GANET di Tanjungpinang.",
        indent=0.25
    )

    doc.add_page_break()

    # ================== BAB IV DAFTAR PUSTAKA ==================
    add_h1("BAB IV\nDAFTAR PUSTAKA")
    
    add_body("Figma. (2026). Figma Design and Prototyping Tool. Retrieved from Figma Website: https://www.figma.com/")
    add_body("Flanagan, D. (2020). JavaScript: The Definitive Guide (7th ed.). O'Reilly Media.")
    add_body("MDN Web Docs. (2026). LocalStorage Web API and Client-Side Storage Documentation. Retrieved from Mozilla Developer Network: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage")
    add_body("UMKM Indonesia. (2025). Strategi Digitalisasi dan Penguatan Promosi UMKM Kuliner Lokal. Jurnal Ekonomi dan Kewirausahaan, 14(2), 112-125.")
    add_body("W3Schools. (2026). HTML5 Semantics and CSS Grid Layout Tutorials. Retrieved from W3Schools Online Web Tutorials: https://www.w3schools.com/")
    add_body("World Wide Web Consortium (W3C). (2025). Web Content Accessibility Guidelines (WCAG) 2.2. Retrieved from W3C Website: https://www.w3.org/WAI/standards-guidelines/wcag/")

    # 4. Save document
    filename = r"c:\RISMA\KULIAH\Semester 4\per web\LaporanProyek_WarungPudding_v2.docx"
    try:
        doc.save(filename)
        print(f"Document saved successfully as: {filename}")
    except PermissionError:
        filename_v3 = r"c:\RISMA\KULIAH\Semester 4\per web\LaporanProyek_WarungPudding_v3.docx"
        doc.save(filename_v3)
        print(f"Permission denied on {filename} (probably open in Word). Saved as: {filename_v3}")

if __name__ == "__main__":
    create_report()
