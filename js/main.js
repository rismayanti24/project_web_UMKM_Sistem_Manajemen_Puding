// js/main.js

// Event listener yang berjalan setelah dokumen HTML selesai dimuat secara penuh (DOM ready)
document.addEventListener('DOMContentLoaded', () => {
    // 1. Efek Skrol Navbar (Navbar Scroll Effect)
    // Mencari elemen navbar di halaman web
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        // Mendengarkan event scroll pada window (halaman digulir ke atas/bawah)
        window.addEventListener('scroll', () => {
            // Jika posisi gulir vertikal lebih dari 50 piksel
            if (window.scrollY > 50) {
                // Tambahkan kelas CSS 'scrolled' (membuat navbar blur/transparan glassmorphism)
                navbar.classList.add('scrolled');
            } else {
                // Hapus kelas 'scrolled' jika kembali ke bagian paling atas
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 2. Tombol Navigasi Seluler (Hamburger Menu Toggle)
    // Mencari tombol hamburger dan kontainer menu navigasi
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        // Mendengarkan klik pada tombol hamburger
        navToggle.addEventListener('click', () => {
            // Mengaktifkan/menonaktifkan kelas CSS 'active' pada menu (slide-in menu mobile)
            navMenu.classList.toggle('active');
            // Mencari ikon di dalam tombol navigasi
            const icon = navToggle.querySelector('i');
            // Mengganti ikon hamburger (fa-bars) menjadi silang (fa-times) saat aktif, atau sebaliknya
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // 3. Memperbarui Angka Indikator Keranjang Belanja (Cart Badge)
    updateCartBadge();

    // 4. Utilitas Jendela Dialog/Modal (Modal Utilities)
    // Fungsi global untuk membuka modal berdasarkan ID modal yang diberikan
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        // Menambahkan kelas 'active' agar modal muncul di layar
        if (modal) modal.classList.add('active');
    };

    // Fungsi global untuk menutup modal berdasarkan ID modal
    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        // Menghapus kelas 'active' agar modal tersembunyi kembali
        if (modal) modal.classList.remove('active');
    };

    // 5. Pembersihan data pesanan palsu/tidak valid (Cleanup stale dummy orders)
    // Mengambil data pesanan dari LocalStorage
    const existingOrders = JSON.parse(localStorage.getItem('wp_orders')) || [];
    if (existingOrders.length > 0) {
        // Menyaring data dan hanya menyisakan pesanan asli yang memiliki properti 'tanggal'
        const cleanOrders = existingOrders.filter(o => o.tanggal); 
        // Jika ada pesanan dummy yang terhapus, simpan kembali data terbersih ke LocalStorage
        if (cleanOrders.length !== existingOrders.length) {
            localStorage.setItem('wp_orders', JSON.stringify(cleanOrders));
        }
    }

    // 6. Efek Animasi Muncul Saat Skrol (Scroll Reveal Observer)
    // Mencari semua elemen yang memiliki kelas CSS 'reveal'
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length > 0) {
        // Membuat detektor perpotongan viewport (Intersection Observer)
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                // Jika elemen mulai terlihat di layar (minimal 15% bagian elemen terlihat)
                if (entry.isIntersecting) {
                    // Tambahkan kelas CSS 'active' untuk memicu animasi masuk CSS
                    entry.target.classList.add('active');
                    // Hentikan pemantauan elemen agar animasi hanya berjalan sekali saja
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 }); // Batas threshold kenyamanan 15%
        // Daftarkan semua elemen reveal ke pemantauan observer
        revealElements.forEach(el => observer.observe(el));
    }

    // 7. Karusel Produk Unggulan Dinamis (Dynamic Featured Products Carousel)
    // Mencari elemen track karusel di halaman beranda
    const track = document.getElementById('carouselTrack');
    // Memastikan track karusel ada dan fungsi getProducts() tersedia
    if (track && typeof getProducts === 'function') {
        // Mengambil daftar seluruh produk dari fungsi helper
        const products = getProducts();
        // ID produk puding unggulan yang ingin ditampilkan di slider beranda
        const featuredIds = ['p1', 'p2', 'p7', 'p8'];
        // Mengambil data lengkap produk berdasarkan daftar ID di atas
        const featuredProducts = featuredIds.map(id => products.find(p => p.id === id)).filter(Boolean);
        
        let htmlContent = '';
        // Menduplikasi daftar produk agar karusel dapat berjalan melingkar tanpa terputus (infinite loop)
        const doubleFeatured = [...featuredProducts, ...featuredProducts];
        
        // Membangun string HTML kartu produk unggulan secara dinamis
        doubleFeatured.forEach(p => {
            // Memeriksa ketersediaan stok produk
            const available = p.stok > 0;
            htmlContent += `
                <div class="carousel-card">
                    <div class="card product-card">
                        <div class="product-image-container">
                            <!-- Foto produk puding dengan fallback gambar placeholder jika foto gagal dimuat -->
                            <img src="${p.gambar}" alt="${p.nama}" class="product-image" onerror="this.src='https://placehold.co/300x200/E6CCFF/9B59B6?text=Puding'">
                            <!-- Menampilkan label overlay 'Habis' jika stok puding kosong (0) -->
                            ${!available ? '<div class="unavailable-overlay"><span>Habis</span></div>' : ''}
                        </div>
                        <div class="product-info">
                            <h3 class="product-title">${p.nama}</h3>
                            <p class="product-price">${formatRupiah(p.harga)}</p>
                            <!-- Tombol untuk beralih ke halaman detail spesifik produk berdasarkan ID -->
                            <a href="detail.html?id=${p.id}" class="btn btn-secondary mt-auto" style="font-size: 0.85rem;">Lihat Detail</a>
                        </div>
                    </div>
                </div>
            `;
        });
        // Menginjeksi kode HTML kartu produk yang telah disusun ke dalam wadah karusel
        track.innerHTML = htmlContent;
    }
});

// Fungsi untuk memperbarui badge angka jumlah item di keranjang belanja
function updateCartBadge() {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        // Mengambil daftar item keranjang dari LocalStorage
        const cart = JSON.parse(localStorage.getItem('wp_cart')) || [];
        // Menjumlahkan kuantitas (qty) dari seluruh item di keranjang
        const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
        // Menuliskan jumlah item ke teks badge
        badge.textContent = totalItems;
        // Menampilkan badge jika jumlah item > 0, dan menyembunyikannya jika kosong
        badge.style.display = totalItems > 0 ? 'flex' : 'none';
    }
}

// Fungsi utilitas global untuk memformat angka nominal ke rupiah (Rp. X.XXX)
function formatRupiah(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0 // Tidak menyertakan angka sen (,00) di belakang nominal
    }).format(amount);
}

// Fungsi utilitas global untuk menghasilkan string ID unik acak 9 karakter
function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

// Fungsi utilitas global untuk menampilkan pesan toast melayang di layar
function showToast(message, type = 'success') {
    // Mencari wadah kontainer toast di dokumen
    let container = document.getElementById('toast-container');
    // Jika kontainer belum ada, buat kontainer baru secara dinamis dan tempelkan ke body
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    // Membuat elemen toast baru
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Menentukan ikon font-awesome berdasarkan tipe toast (sukses atau error)
    const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    
    // Mengisi konten HTML toast
    toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
    
    // Menambahkan toast baru ke dalam wadah kontainer
    container.appendChild(toast);
    
    // Menghapus toast secara otomatis setelah 3 detik
    setTimeout(() => {
        // Memutar animasi keluar (slide keluar ke arah berlawanan)
        toast.style.animation = 'slideIn 0.3s ease reverse';
        // Menghapus elemen HTML toast dari dokumen setelah animasi selesai (300 milidetik)
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
