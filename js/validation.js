// js/validation.js
// Pustaka utilitas validasi formulir untuk aplikasi WarungPudding

/**
 * Validasi input nomor telepon/WhatsApp
 * @param {string} phone - Nomor telepon masukan dari pengguna
 * @returns {boolean} Mengembalikan true jika valid, false jika tidak valid
 */
function validatePhone(phone) {
    // Pola ekspresi reguler (Regex) nomor telepon Indonesia:
    // Mendukung awalan: 08xx, +62xx, atau 62xx, diikuti oleh 7-11 digit angka
    const phoneRegex = /^(\+62|62|0)8[1-9][0-9]{7,11}$/;
    // Menghapus spasi dan tanda hubung sebelum mencocokkan ke regex
    return phoneRegex.test(phone.replace(/[\s-]/g, ''));
}

/**
 * Validasi input nama lengkap (minimal 3 karakter)
 * @param {string} name - Nama lengkap masukan pengguna
 * @returns {boolean} Mengembalikan true jika nama >= 3 karakter
 */
function validateName(name) {
    // Menghapus spasi di awal & akhir kalimat (trim), lalu hitung panjang string
    return name.trim().length >= 3;
}

/**
 * Validasi input alamat pengiriman (minimal 10 karakter)
 * @param {string} address - Alamat lengkap pengiriman
 * @returns {boolean} Mengembalikan true jika alamat >= 10 karakter
 */
function validateAddress(address) {
    // Menghindari masukan alamat kosong atau terlalu pendek
    return address.trim().length >= 10;
}

/**
 * Validasi format email umum
 * @param {string} email - Alamat email pengguna
 * @returns {boolean} Mengembalikan true jika berformat email valid
 */
function validateEmail(email) {
    // Pola regex standar untuk mencocokkan format email (karakter@domain.ext)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validasi username login (minimal 3 karakter, hanya alfanumerik)
 * @param {string} username - Nama pengguna (username)
 * @returns {boolean} Mengembalikan true jika valid
 */
function validateUsername(username) {
    // Karakter tidak boleh mengandung spasi atau simbol khusus (hanya huruf dan angka)
    return username.trim().length >= 3 && /^[a-zA-Z0-9]+$/.test(username);
}

/**
 * Validasi panjang kata sandi (minimal 5 karakter)
 * @param {string} password - Kata sandi (password)
 * @returns {boolean} Mengembalikan true jika kata sandi >= 5 karakter
 */
function validatePassword(password) {
    return password.length >= 5;
}

/**
 * Fungsi untuk menampilkan pesan error berwarna merah di bawah elemen input yang bermasalah
 * @param {HTMLElement} inputEl - Elemen input HTML
 * @param {string} message - Teks pesan kesalahan yang ingin ditampilkan
 */
function showFieldError(inputEl, message) {
    // Bersihkan dulu pesan kesalahan lama jika ada agar tidak menumpuk
    clearFieldError(inputEl);
    
    // Mengubah warna batas luar input menjadi merah
    inputEl.style.borderColor = '#E74C3C';
    // Menambahkan efek bayangan merah lembut di sekitar input
    inputEl.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.15)';
    
    // Membuat elemen div pembungkus pesan error secara dinamis
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    // Menentukan style css untuk tata letak tulisan merah
    errorDiv.style.cssText = 'color: #E74C3C; font-size: 0.8rem; margin-top: 5px; display: flex; align-items: center; gap: 5px;';
    // Mengisi konten pesan beserta ikon peringatan tanda seru
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    // Memasukkan elemen error ke dalam struktur HTML di bawah elemen input terkait
    inputEl.parentElement.appendChild(errorDiv);
}

/**
 * Fungsi untuk menghapus indikator visual error dan pesan kesalahan pada elemen input
 * @param {HTMLElement} inputEl - Elemen input HTML
 */
function clearFieldError(inputEl) {
    // Mengembalikan warna bingkai (border) input ke kondisi semula
    inputEl.style.borderColor = '';
    // Menghapus bayangan merah di sekitar input
    inputEl.style.boxShadow = '';
    
    // Mencari apakah ada elemen pesan error kelas 'field-error' di bawah parent input
    const existingError = inputEl.parentElement.querySelector('.field-error');
    if (existingError) {
        // Hapus elemen tersebut dari halaman
        existingError.remove();
    }
}

/**
 * Fungsi utama untuk memvalidasi seluruh input pada formulir Checkout Belanja
 * @returns {boolean} Mengembalikan true jika seluruh data checkout valid
 */
function validateCheckoutForm() {
    let isValid = true;
    
    // Mengambil elemen input nama, nomor telepon, dan alamat
    const nama = document.getElementById('nama');
    const telepon = document.getElementById('telepon');
    const alamat = document.getElementById('alamat');
    
    // Validasi input nama
    if (nama && !validateName(nama.value)) {
        showFieldError(nama, 'Nama minimal 3 karakter');
        isValid = false;
    } else if (nama) {
        clearFieldError(nama);
    }
    
    // Validasi input telepon/WhatsApp
    if (telepon && !validatePhone(telepon.value)) {
        showFieldError(telepon, 'Nomor WhatsApp tidak valid (contoh: 08123456789)');
        isValid = false;
    } else if (telepon) {
        clearFieldError(telepon);
    }
    
    // Validasi input alamat
    if (alamat && !validateAddress(alamat.value)) {
        showFieldError(alamat, 'Alamat minimal 10 karakter');
        isValid = false;
    } else if (alamat) {
        clearFieldError(alamat);
    }
    
    return isValid;
}

/**
 * Fungsi utama untuk memvalidasi input pada formulir Login
 * @returns {boolean} Mengembalikan true jika data username & password memenuhi ketentuan
 */
function validateLoginForm() {
    let isValid = true;
    
    // Mengambil elemen input username dan password
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    
    // Validasi input username
    if (username && !validateUsername(username.value)) {
        showFieldError(username, 'Username minimal 3 karakter (alfanumerik)');
        isValid = false;
    } else if (username) {
        clearFieldError(username);
    }
    
    // Validasi input password
    if (password && !validatePassword(password.value)) {
        showFieldError(password, 'Password minimal 5 karakter');
        isValid = false;
    } else if (password) {
        clearFieldError(password);
    }
    
    return isValid;
}

// Menjalankan event listener setelah struktur HTML selesai dimuat
document.addEventListener('DOMContentLoaded', () => {
    // Mencari seluruh elemen input yang memiliki kelas '.form-control'
    document.querySelectorAll('.form-control').forEach(input => {
        // Ketika pengguna mulai mengetik ulang di kolom tersebut
        input.addEventListener('input', () => {
            // Hapus pesan error secara otomatis secara real-time agar halaman kembali bersih
            clearFieldError(input);
        });
    });
});

